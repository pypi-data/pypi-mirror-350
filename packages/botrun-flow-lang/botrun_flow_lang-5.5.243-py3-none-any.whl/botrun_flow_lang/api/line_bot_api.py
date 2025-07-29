import os
import json
import time
import sys
import logging
import traceback
from collections import defaultdict, deque
from typing import Tuple
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import AsyncMessagingApi
from botrun_flow_lang.langgraph_agents.agents.agent_runner import agent_runner
from botrun_flow_lang.langgraph_agents.agents.search_agent_graph import (
    SearchAgentGraph,
    DEFAULT_SEARCH_CONFIG,
)
from botrun_flow_lang.langgraph_agents.agents.checkpointer.firestore_checkpointer import (
    AsyncFirestoreCheckpointer,
)
from botrun_flow_lang.utils.google_drive_utils import (
    authenticate_google_services,
    get_google_doc_mime_type,
    get_google_doc_content_with_service,
)


# 設置日誌記錄
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# 常量定義
SUBSIDY_LINE_BOT_CHANNEL_SECRET = os.getenv("SUBSIDY_LINE_BOT_CHANNEL_SECRET", None)
SUBSIDY_LINE_BOT_CHANNEL_ACCESS_TOKEN = os.getenv(
    "SUBSIDY_LINE_BOT_CHANNEL_ACCESS_TOKEN", None
)
RATE_LIMIT_WINDOW = int(
    os.environ.get("SUBSIDY_LINEBOT_RATE_LIMIT_WINDOW", 60)
)  # 預設時間窗口為 1 分鐘 (60 秒)
RATE_LIMIT_COUNT = int(
    os.environ.get("SUBSIDY_LINEBOT_RATE_LIMIT_COUNT", 1)
)  # 預設在時間窗口內允許的訊息數量 1
LINE_MAX_MESSAGE_LENGTH = 5000

# 全局變數
# 用於追蹤正在處理訊息的使用者，避免同一使用者同時發送多條訊息造成處理衝突
_processing_users = set()
# 用於訊息頻率限制：追蹤每個使用者在時間窗口內發送的訊息時間戳記
# 使用 defaultdict(deque) 結構確保：1) 只記錄有發送訊息的使用者 2) 高效管理時間窗口內的訊息
_user_message_timestamps = defaultdict(deque)

# 初始化 FastAPI 路由器，設定 API 路徑前綴
router = APIRouter(prefix="/line_bot")

# 必要環境變數檢查
# 這裡先拿掉
# if SUBSIDY_LINE_BOT_CHANNEL_SECRET is None:
#     print("Specify SUBSIDY_LINE_BOT_CHANNEL_SECRET as environment variable.")
#     sys.exit(1)
# if SUBSIDY_LINE_BOT_CHANNEL_ACCESS_TOKEN is None:
#     print("Specify SUBSIDY_LINE_BOT_CHANNEL_ACCESS_TOKEN as environment variable.")
#     sys.exit(1)


def get_subsidy_api_system_prompt():
    """
    取得智津貼的系統提示
    優先從 Google 文件讀取，失敗時回退到本地檔案
    """
    try:
        # 檢查必要的環境變數是否存在
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_FOR_BOTRUN_DOC")
        file_id = os.getenv("SUBSIDY_BOTRUN_DOC_FILE_ID")
        
        if not credentials_path or not file_id:
            raise ValueError("Missing required environment variables")
            
        # 嘗試從 Google 文件讀取
        drive_service, _ = authenticate_google_services(credentials_path)
        mime_type = get_google_doc_mime_type(file_id)
        file_text = get_google_doc_content_with_service(
            file_id,
            mime_type,
            drive_service,
            with_decode=True
        )
        
        # 提取 system_prompt 內容
        import re
        match = re.search(r'<system_prompt>(.*?)</system_prompt>', file_text, re.DOTALL)
        if match:
            logger.info("[Line Bot Webhook: subsidy_webhook] Successfully extracted system prompt from Google Docs")
            return match.group(1).strip()
        logger.info("[Line Bot Webhook: subsidy_webhook] Failed to extract system prompt from Google Docs, return file text")

        return file_text
        
    except Exception as e:
        logger.warning(f"[Line Bot Webhook: subsidy_webhook] Failed to load prompt from Google Docs, falling back to local file. Error: {e}")
        # 如果從 Google 文件讀取失敗，則回退到本地檔案
        current_dir = Path(__file__).parent
        return (current_dir / "subsidy_api_system_prompt.txt").read_text(encoding="utf-8")


def get_subsidy_bot_search_config() -> dict:
    return {
        **DEFAULT_SEARCH_CONFIG,
        "search_prompt": get_subsidy_api_system_prompt(),
        "domain_filter": ["*.gov.tw", "-*.gov.cn"],
        "user_prompt_prefix": "你是台灣人，你不可以講中國用語也不可以用簡體中文，禁止！你的回答內容不要用Markdown格式。",
        "stream": False,
    }


@router.post("/subsidy/webhook")
async def subsidy_webhook(request: Request):
    from linebot.v3.exceptions import InvalidSignatureError
    from linebot.v3.webhook import WebhookParser
    from linebot.v3.messaging import AsyncApiClient, Configuration

    signature = request.headers["X-Line-Signature"]
    if SUBSIDY_LINE_BOT_CHANNEL_SECRET is None:
        raise HTTPException(
            status_code=500, detail="SUBSIDY_LINE_BOT_CHANNEL_SECRET is not set"
        )
    if SUBSIDY_LINE_BOT_CHANNEL_ACCESS_TOKEN is None:
        raise HTTPException(
            status_code=500, detail="SUBSIDY_LINE_BOT_CHANNEL_ACCESS_TOKEN is not set"
        )
    parser = WebhookParser(SUBSIDY_LINE_BOT_CHANNEL_SECRET)
    configuration = Configuration(access_token=SUBSIDY_LINE_BOT_CHANNEL_ACCESS_TOKEN)

    # get request body as text
    body = await request.body()
    body_str = body.decode("utf-8")
    body_json = json.loads(body_str)
    logging.info(
        "[Line Bot Webhook: subsidy_webhook] Received webhook: %s",
        json.dumps(body_json, indent=2, ensure_ascii=False),
    )

    try:
        events = parser.parse(body_str, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    start = time.time()
    env_name = os.getenv("ENV_NAME", "botrun-flow-lang-dev")
    subsidy_line_bot_graph = SearchAgentGraph(
        memory=AsyncFirestoreCheckpointer(env_name=env_name)
    ).graph
    logging.info(
        f"[Line Bot Webhook: subsidy_webhook] init graph took {time.time() - start:.3f}s"
    )

    responses = []
    async with AsyncApiClient(configuration) as async_api_client:
        line_bot_api = AsyncMessagingApi(async_api_client)
        for event in events:
            if not isinstance(event, MessageEvent):
                continue
            if not isinstance(event.message, TextMessageContent):
                continue

            response = await handle_message(
                event,
                line_bot_api,
                RATE_LIMIT_WINDOW,
                RATE_LIMIT_COUNT,
                subsidy_line_bot_graph,
            )
            responses.append(response)

    return {"responses": responses}


async def handle_message(
    event: MessageEvent,
    line_bot_api: AsyncMessagingApi,
    rate_limit_window: int,
    rate_limit_count: int,
    line_bot_graph: SearchAgentGraph,
):
    """處理 LINE Bot 的訊息事件

    處理使用者傳送的文字訊息，包括頻率限制檢查、訊息分段與回覆等操作

    Args:
        event (MessageEvent): LINE Bot 的訊息事件
        line_bot_api (AsyncMessagingApi): LINE Bot API 客戶端
        rate_limit_window (int): 訊息頻率限制時間窗口（秒）
        rate_limit_count (int): 訊息頻率限制數量
        line_bot_graph (SearchAgentGraph): LINE Bot 的 agent graph
    """
    start = time.time()
    logging.info(
        "[Line Bot Webhook: handle_message] Enter handle_message for event type: %s",
        event.type,
    )
    from linebot.v3.messaging import (
        ReplyMessageRequest,
        TextMessage,
    )

    # 已經移至常量部分定義
    user_id = event.source.user_id
    user_message = event.message.text

    if user_id in _processing_users:
        logging.info(
            f"[Line Bot Webhook: handle_message] 使用者 {user_id} 已有處理中的訊息，回覆等待提示"
        )
        reply_text = "您的上一條訊息正在處理中，請稍候再發送新訊息"
        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)],
            )
        )
        return {"message": reply_text}

    # 檢查使用者是否超過訊息頻率限制
    is_rate_limited, wait_seconds = check_rate_limit(
        user_id, rate_limit_window, rate_limit_count
    )
    if is_rate_limited:
        logging.info(
            f"[Line Bot Webhook: handle_message] 使用者 {user_id} 超過訊息頻率限制，需等待 {wait_seconds} 秒"
        )

        # 回覆頻率限制提示
        window_minutes = rate_limit_window // 60
        wait_minutes = max(1, wait_seconds // 60)
        reply_text = f"您發送訊息的頻率過高，{window_minutes}分鐘內最多可發送{rate_limit_count}則訊息。請等待約 {wait_minutes} 分鐘後再試。"
        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)],
            )
        )
        return {"message": reply_text}

    # 標記使用者為處理中
    _processing_users.add(user_id)

    try:
        logging.info(
            f"[Line Bot Webhook: handle_message] Received message from {user_id}: {user_message}"
        )
        reply_text = await get_reply_text(line_bot_graph, user_message, user_id)

        logging.info(
            f"[Line Bot Webhook: handle_message] Total response length: {len(reply_text)}"
        )

        # 將長訊息分段，每段不超過 LINE_MAX_MESSAGE_LENGTH
        message_chunks = []
        remaining_text = reply_text

        while remaining_text:
            # 如果剩餘文字長度在限制內，直接加入並結束
            if len(remaining_text) <= LINE_MAX_MESSAGE_LENGTH:
                message_chunks.append(remaining_text)
                logging.info(
                    f"[Line Bot Webhook: handle_message] Last chunk length: {len(remaining_text)}"
                )
                break

            # 確保分段大小在限制內
            safe_length = min(
                LINE_MAX_MESSAGE_LENGTH - 100, len(remaining_text)
            )  # 預留一些空間

            # 在安全長度內尋找最後一個完整句子
            chunk_end = safe_length
            for i in range(safe_length - 1, max(0, safe_length - 200), -1):
                if remaining_text[i] in "。！？!?":
                    chunk_end = i + 1
                    break

            # 如果找不到適合的句子結尾，就用空格或換行符號來分割
            if chunk_end == safe_length:
                for i in range(safe_length - 1, max(0, safe_length - 200), -1):
                    if remaining_text[i] in " \n":
                        chunk_end = i + 1
                        break
                # 如果還是找不到合適的分割點，就直接在安全長度處截斷
                if chunk_end == safe_length:
                    chunk_end = safe_length

            # 加入這一段文字
            current_chunk = remaining_text[:chunk_end]
            logging.info(
                f"[Line Bot Webhook: handle_message] Current chunk length: {len(current_chunk)}"
            )
            message_chunks.append(current_chunk)

            # 更新剩餘文字
            remaining_text = remaining_text[chunk_end:]

        logging.info(
            f"[Line Bot Webhook: handle_message] Number of chunks: {len(message_chunks)}"
        )
        for i, chunk in enumerate(message_chunks):
            logging.info(
                f"[Line Bot Webhook: handle_message] Chunk {i} length: {len(chunk)}"
            )

        messages = [TextMessage(text=chunk) for chunk in message_chunks]
        await line_bot_api.reply_message(
            ReplyMessageRequest(reply_token=event.reply_token, messages=messages)
        )
    except Exception as e:
        logging.error(
            f"[Line Bot Webhook: handle_message] 處理使用者 {user_id} 訊息時發生錯誤: {e}"
        )
        traceback.print_exc()
        reply_text = "很抱歉，處理您的訊息時遇到問題，請稍後再試"
        try:
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=reply_text)],
                )
            )
        except Exception as reply_error:
            logging.error(
                f"[Line Bot Webhook: handle_message] 無法發送錯誤回覆: {reply_error}"
            )
            traceback.print_exc()
    finally:
        logging.info(
            f"[Line Bot Webhook: handle_message] total elapsed {time.time() - start:.3f}s"
        )
        _processing_users.discard(user_id)
        logging.info(
            f"[Line Bot Webhook: handle_message] 使用者 {user_id} 的訊息處理完成"
        )

    return {"message": reply_text}


def check_rate_limit(user_id: str, window: int, count: int) -> Tuple[bool, int]:
    """檢查使用者是否超過訊息頻率限制

    檢查使用者在指定時間窗口內發送的訊息數量是否超過限制。
    同時清理過期的時間戳記，以避免記憶體無限增長。

    Args:
        user_id (str): 使用者的 LINE ID
        window (int): 時間窗口（秒）
        count (int): 訊息數量限制

    Returns:
        Tuple[bool, int]: (是否超過限制, 需要等待的秒數)
        如果未超過限制，第二個值為 0
    """
    current_time = time.time()
    user_timestamps = _user_message_timestamps[user_id]

    # 清理過期的時間戳記（超過時間窗口的）
    while user_timestamps and current_time - user_timestamps[0] > window:
        user_timestamps.popleft()

    # 如果清理後沒有時間戳記，則從字典中移除該使用者的記錄
    if not user_timestamps:
        del _user_message_timestamps[user_id]
        # 如果使用者沒有有效的時間戳記，則直接添加新的時間戳記
        _user_message_timestamps[user_id].append(current_time)
        return False, 0

    # 檢查是否超過限制
    if len(user_timestamps) >= count:
        # 計算需要等待的時間
        oldest_timestamp = user_timestamps[0]
        wait_time = int(window - (current_time - oldest_timestamp))
        return True, max(0, wait_time)

    # 未超過限制，添加當前時間戳記
    user_timestamps.append(current_time)

    return False, 0


async def get_reply_text(line_bot_graph, line_user_message: str, user_id: str) -> str:
    """
    使用 agent_runner 處理使用者訊息並回傳回覆內容

    Args:
        line_bot_graph (SearchAgentGraph): LINE Bot 的 agent graph
        line_user_message (str): 使用者傳送的 LINE 訊息內容
        user_id (str): 使用者的 LINE ID

    Returns:
        str: 回覆訊息
    """
    start_time = time.time()
    full_response = ""

    async for event_chunk in agent_runner(
        user_id,
        {"messages": [line_user_message]},
        line_bot_graph,
        extra_config=get_subsidy_bot_search_config(),
    ):
        full_response += event_chunk.chunk

    if "</think>" in full_response:
        full_response = full_response.split("</think>", 1)[1]

    # 將 related_questions 附加到回覆內容
    related_questions = []
    try:
        # 嘗試使用非同步方式取得 state（若 checkpointer 為非同步型別）
        try:
            state_obj = await line_bot_graph.aget_state({"configurable": {"thread_id": user_id}})
        except AttributeError:
            # 回退到同步方法
            state_obj = line_bot_graph.get_state({"configurable": {"thread_id": user_id}})

        # 根據返回型別（dict 或具備屬性）解析
        if isinstance(state_obj, dict):
            related_questions = state_obj.get("related_questions", [])
        elif hasattr(state_obj, "related_questions"):
            related_questions = getattr(state_obj, "related_questions", [])
        elif hasattr(state_obj, "values") and isinstance(state_obj.values, dict):
            related_questions = state_obj.values.get("related_questions", [])

        if related_questions:
            full_response += "\n\n以下是您可能想要了解的相關問題：\n"
            for idx, question in enumerate(related_questions, 1):
                full_response += f"{idx}. {question}\n"
    except Exception as e:
        logging.error(
            f"[Line Bot Webhook: get_reply_text] Failed to append related questions: {e}"
        )

    logging.info(
        f"[Line Bot Webhook: get_reply_text] total took {time.time() - start_time:.3f}s"
    )

    return full_response
