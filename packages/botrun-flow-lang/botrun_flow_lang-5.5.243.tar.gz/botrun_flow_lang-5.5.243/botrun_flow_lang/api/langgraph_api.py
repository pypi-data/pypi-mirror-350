import logging
import uuid
import json
import random
import time
import re

from fastapi import APIRouter, HTTPException

from pydantic import BaseModel

from typing import Dict, Any, List, Optional

from fastapi.responses import StreamingResponse

from botrun_flow_lang.constants import ERR_GRAPH_RECURSION_ERROR, LANG_EN, LANG_ZH_TW

from botrun_flow_lang.langgraph_agents.agents.agent_runner import (
    agent_runner,
    langgraph_runner,
)

from botrun_flow_lang.langgraph_agents.agents.langgraph_react_agent import (
    create_react_agent_graph,
    get_react_agent_model_name,
)

from botrun_flow_lang.models.token_usage import TokenUsage

from botrun_flow_lang.utils.botrun_logger import BotrunLogger, default_logger

from botrun_flow_lang.langgraph_agents.agents.search_agent_graph import (
    SearchAgentGraph,
    # graph as search_agent_graph,
)

from botrun_flow_lang.utils.langchain_utils import (
    extract_token_usage_from_state,
    langgraph_event_to_json,
    litellm_msgs_to_langchain_msgs,
)

from contextlib import AsyncExitStack
from langchain_mcp_adapters.client import MultiServerMCPClient

router = APIRouter(prefix="/langgraph")


class LangGraphRequest(BaseModel):
    graph_name: str
    # todo LangGraph 應該要傳 thread_id，但是因為現在是 cloud run 的架構，所以 thread_id 不一定會讀的到 (auto scale)
    thread_id: Optional[str] = None
    user_input: Optional[str] = None
    messages: List[Dict[str, Any]] = []
    config: Optional[Dict[str, Any]] = None
    stream: bool = False
    # LangGraph 是否需要從 checkpoint 恢復
    need_resume: bool = False
    session_id: Optional[str] = None


class LangGraphResponse(BaseModel):
    """
    @param content: 這個是給評測用來評估結果用的
    @param state: 這個是graph的 final state，如果需要額外資訊可以使用
    @param token_usage: Token usage information for the entire graph execution
    """

    id: str
    object: str = "chat.completion"
    created: int
    model: str
    content: Optional[str] = None
    state: Optional[Dict[str, Any]] = None
    token_usage: Optional[TokenUsage] = None


class SupportedGraphsResponse(BaseModel):
    """Response model for listing supported graphs"""

    graphs: List[str]


PERPLEXITY_SEARCH_AGENT = "perplexity_search_agent"
CUSTOM_WEB_RESEARCH_AGENT = "custom_web_research_agent"
LANGGRAPH_REACT_AGENT = "langgraph_react_agent"
DEEP_RESEARCH_AGENT = "deep_research_agent"


SUPPORTED_GRAPH_NAMES = [
    PERPLEXITY_SEARCH_AGENT,
    LANGGRAPH_REACT_AGENT,
]


def get_supported_graphs():
    return {
        PERPLEXITY_SEARCH_AGENT: SearchAgentGraph().graph,
        LANGGRAPH_REACT_AGENT: create_react_agent_graph(),
        # CUSTOM_WEB_RESEARCH_AGENT: ai_researcher_graph,
        # DEEP_RESEARCH_AGENT: deep_research_graph,
    }


def contains_chinese_chars(text: str) -> bool:
    """Check if the given text contains any Chinese characters."""
    if not text:
        return False
    # This pattern matches Chinese characters (both simplified and traditional)
    pattern = re.compile(
        r"[\u4e00-\u9fff\u3400-\u4dbf\U00020000-\U0002a6df\U0002a700-\U0002ebef]"
    )
    return bool(pattern.search(text))


async def get_graph(
    graph_name: str,
    config: Optional[Dict[str, Any]] = None,
    stream: bool = False,
    messages: Optional[List[Dict]] = [],
    user_input: Optional[str] = None,
    mcp_client: Optional[MultiServerMCPClient] = None,
):
    if graph_name not in SUPPORTED_GRAPH_NAMES:
        raise ValueError(f"Unsupported graph from get_graph: {graph_name}")
    if graph_name == PERPLEXITY_SEARCH_AGENT:
        graph = SearchAgentGraph().graph
        graph_config = {
            "search_prompt": config.get("search_prompt", ""),
            "model_name": config.get("model_name", "sonar-reasoning-pro"),
            "related_prompt": config.get("related_question_prompt", ""),
            "search_vendor": config.get("search_vendor", "perplexity"),
            "domain_filter": config.get("domain_filter", []),
            "user_prompt_prefix": config.get("user_prompt_prefix", ""),
            "stream": stream,
        }
    elif graph_name == LANGGRAPH_REACT_AGENT:
        graph_config = config

        system_prompt = config.get("system_prompt", "")
        if messages:
            for message in messages:
                if message.get("role") == "system":
                    system_prompt = message.get("content", "")

        # Check for Chinese characters in system_prompt and user_input
        has_chinese = contains_chinese_chars(system_prompt)
        if not has_chinese and user_input:
            has_chinese = contains_chinese_chars(user_input)

        lang = LANG_ZH_TW if has_chinese else LANG_EN

        graph = await create_react_agent_graph(
            system_prompt=system_prompt,
            botrun_flow_lang_url=config.get("botrun_flow_lang_url", ""),
            user_id=config.get("user_id", ""),
            model_name=config.get("model_name", ""),
            lang=lang,
            mcp_client=mcp_client,
        )
    return graph, graph_config


def get_init_state(
    graph_name: str,
    user_input: str,
    config: Optional[Dict[str, Any]] = None,
    messages: Optional[List[Dict]] = [],
    enable_prompt_caching: bool = False,
):
    if graph_name == PERPLEXITY_SEARCH_AGENT:
        if len(messages) > 0:
            return {"messages": litellm_msgs_to_langchain_msgs(messages)}
        if config.get("user_prompt_prefix", ""):
            return {
                "messages": [
                    {
                        "role": "user",
                        "content": config.get("user_prompt_prefix", "")
                        + "\n\n"
                        + user_input,
                    }
                ]
            }

        return {"messages": [user_input]}
    elif graph_name == CUSTOM_WEB_RESEARCH_AGENT:
        if len(messages) > 0:
            return {
                "messages": litellm_msgs_to_langchain_msgs(messages),
                "model": config.get("model", "anthropic"),
            }
        return {
            "messages": [user_input],
            "model": config.get("model", "anthropic"),
        }
    elif graph_name == LANGGRAPH_REACT_AGENT:
        if len(messages) > 0:
            new_messages = []
            for message in messages:
                if message.get("role") != "system":
                    new_messages.append(message)
            return {
                "messages": litellm_msgs_to_langchain_msgs(
                    new_messages, enable_prompt_caching
                )
            }
        else:
            return {
                "messages": [user_input],
            }
    elif graph_name == DEEP_RESEARCH_AGENT:
        if len(messages) > 0:
            return {
                "messages": litellm_msgs_to_langchain_msgs(messages),
                "topic": user_input,
            }
        return {
            "messages": [user_input],
            "topic": user_input,
        }
    raise ValueError(f"Unsupported graph from get_init_state: {graph_name}")


def get_content(graph_name: str, state: Dict[str, Any]):
    if graph_name == PERPLEXITY_SEARCH_AGENT:
        return state["messages"][-3].content
    elif graph_name == CUSTOM_WEB_RESEARCH_AGENT:
        content = state["answer"].get("markdown", "")
        content = content.replace("\\n", "\n")
        if state["answer"].get("references", []):
            references = "\n\n參考資料：\n"
            for reference in state["answer"]["references"]:
                references += f"- [{reference['title']}]({reference['url']})\n"
            content += references
        return content
    elif graph_name == DEEP_RESEARCH_AGENT:
        sections = state["sections"]
        sections_str = "\n\n".join(
            f"章節: {section.name}\n"
            f"描述: {section.description}\n"
            f"需要研究: {'是' if section.research else '否'}\n"
            for section in sections
        )
        sections_str = "預計報告結構：\n\n" + sections_str
        return sections_str
    else:
        messages = state["messages"]
        # Find the last human message
        last_human_idx = -1
        for i, msg in enumerate(messages):
            if msg.type == "human":
                last_human_idx = i

        # Combine all AI messages after the last human message
        ai_contents = ""
        for msg in messages[last_human_idx + 1 :]:
            if msg.type == "ai":
                if isinstance(msg.content, list):
                    ai_contents += msg.content[0].get("text", "")
                else:
                    ai_contents += msg.content

        return ai_contents


@router.post("/run")
async def run_langgraph(request: LangGraphRequest):
    """
    執行指定的 LangGraph，支援串流和非串流模式

    Args:
        request: 包含 graph_name 和輸入數據的請求

    Returns:
        串流模式: StreamingResponse
        非串流模式: LangGraphResponse
    """
    try:
        graph, graph_config = await get_graph(
            request.graph_name, request.config, request.stream
        )
        init_state = get_init_state(
            request.graph_name, request.user_input, request.config
        )

        if request.stream:
            return StreamingResponse(
                langgraph_stream_response_generator(request.thread_id, init_state, graph),
                media_type="text/event-stream",
            )

        # 非串流模式的原有邏輯
        async for event in agent_runner(
            request.thread_id, init_state, graph, extra_config=graph_config
        ):
            pass

        config = {"configurable": {"thread_id": request.thread_id}}
        state = graph.get_state(config)
        content = get_content(request.graph_name, state.values)
        token_usage = extract_token_usage_from_state(state.values)
        return LangGraphResponse(
            id=request.thread_id,
            created=int(time.time()),
            model=request.graph_name,
            content=content,
            state=state.values,
            token_usage=token_usage,
        )

    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"執行 LangGraph 時發生錯誤: {str(e)}"
        )


async def process_langgraph_request(
    request: LangGraphRequest,
    retry: bool = False, # Keep retry logic for non-streaming path if needed
    logger: logging.Logger = default_logger,
) -> Any: # Return type can be LangGraphResponse or StreamingResponse
    """處理 LangGraph 請求的核心邏輯"""
    # Import heavy dependencies here if needed, or keep them top-level if frequently used
    from langgraph.errors import GraphRecursionError
    import anthropic

    # --- Streaming Case ---
    if request.stream:
        logger.info(f"Processing STREAM request for graph: {request.graph_name}")
        # Use the new wrapper generator that handles resource management
        return StreamingResponse(
            managed_langgraph_stream_wrapper(request, logger),
            media_type="text/event-stream",
        )

    # --- Non-Streaming Case ---
    logger.info(f"Processing NON-STREAM request for graph: {request.graph_name}")
    try:
        async with AsyncExitStack() as stack:
            mcp_client = None
            # Ensure config and mcp_config exist
            config = request.config or {}
            mcp_config = config.get("mcp_config")

            if mcp_config and MultiServerMCPClient:
                logger.info("MCP config detected, initializing MultiServerMCPClient for non-stream...")
                try:
                    client_instance = MultiServerMCPClient(mcp_config)
                    mcp_client = await stack.enter_async_context(client_instance)
                    logger.info("MultiServerMCPClient initialized and managed by stack for non-stream.")
                except Exception as e_client:
                    logger.error(f"Error initializing MCPClient for non-stream: {e_client}", exc_info=True)
                    raise HTTPException(status_code=500, detail=f"MCP Client Initialization Error: {e_client}")
            else:
                 logger.info("No MCP config found or MCP client library unavailable.")


            # --- Graph and State Initialization (Inside the stack for non-streaming) ---
            graph, graph_config = await get_graph(
                request.graph_name,
                request.config,
                False, # stream=False
                request.messages,
                request.user_input,
                mcp_client=mcp_client, # Pass the managed client
            )

            # Determine model name for init_state caching logic if needed
            # user_input_model_name = request.config.get("model_name", "")
            # enable_caching = get_react_agent_model_name(user_input_model_name).startswith("claude-")

            init_state = get_init_state(
                request.graph_name,
                request.user_input,
                request.config,
                request.messages,
                False # enable_prompt_caching=enable_caching
            )

            thread_id = request.thread_id if request.thread_id else str(uuid.uuid4())
            logger.info(f"Running non-stream with thread_id: {thread_id}")

            # --- Run the agent (non-streaming) ---
            logger.info("Executing agent_runner for non-stream request...")
            # The agent_runner itself iterates, but we wait for it to complete
            async for _ in agent_runner( # We don't need the intermediate events here
                thread_id,
                init_state,
                graph,
                request.need_resume,
                extra_config=graph_config,
            ):
                pass # Just consume the events

            logger.info(f"agent_runner completed for thread_id: {thread_id}. Fetching final state.")

            # --- Get Final State and Prepare Response ---
            config_for_state = {"configurable": {"thread_id": thread_id}}
            state = await graph.aget_state(config_for_state)

            try:
                 state_values_json = langgraph_event_to_json(state.values)
                 logger.info(f"Final state fetched for {thread_id}: {state_values_json[:500]}...") # Log truncated state
            except Exception as e_log:
                 logger.error(f"Error serializing final state for logging: {e_log}")
                 logger.info(f"Final state keys for {thread_id}: {list(state.values.keys())}")


            content = get_content(request.graph_name, state.values)

            model_name_config = request.config.get("model_name", "") if request.config else ""
            final_model_name = model_name_config # Default to config model name
            if request.graph_name == LANGGRAPH_REACT_AGENT:
                 final_model_name = get_react_agent_model_name(model_name_config)

            token_usage = extract_token_usage_from_state(state.values, final_model_name)

            return LangGraphResponse(
                id=thread_id,
                created=int(time.time()),
                model=request.graph_name, # Or final_model_name? Check requirements
                content=content,
                state=state.values, # Consider serializing state here if needed client-side
                token_usage=token_usage,
            )

    except anthropic.RateLimitError as e:
        if retry:
            logger.error("Retry failed with Anthropic RateLimitError (non-stream)", exc_info=True)
            raise HTTPException(status_code=429, detail=f"Rate limit exceeded after retry: {e}") # 429 is more appropriate

        logger.warning(f"Anthropic RateLimitError occurred (non-stream): {e}. Retrying...")
        retry_delay = random.randint(7, 20)
        time.sleep(retry_delay) # Note: time.sleep blocks async. Consider asyncio.sleep(retry_delay) if this becomes an issue.
        logger.info(f"Retrying non-stream request after {retry_delay}s delay...")
        return await process_langgraph_request(request, retry=True, logger=logger) # Recursive call for retry

    except GraphRecursionError as e:
        logger.error(f"GraphRecursionError (non-stream): {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Graph execution exceeded maximum depth: {e}")

    except Exception as e:
        import traceback
        tb_str = traceback.format_exc()
        logger.error(f"Unhandled exception in process_langgraph_request (non-stream): {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error during graph execution: {e}")


@router.post("/invoke")
async def invoke(request: LangGraphRequest):
    """
    執行指定的 LangGraph，支援串流和非串流模式

    Args:
        request: 包含 graph_name 和輸入數據的請求

    Returns:
        串流模式: StreamingResponse
        非串流模式: LangGraphResponse
    """
    session_id = request.session_id
    user_id = request.config.get("user_id", "")

    # *** Create a NEW BotrunLogger for this specific request ***
    # This ensures Cloud Logging and session/user context
    logger = BotrunLogger(session_id=session_id, user_id=user_id)

    logger.info(
        "invoke LangGraph API",
        request=request.model_dump(),
    )

    # Pass the request-specific BotrunLogger down
    return await process_langgraph_request(request, logger=logger)


# NEW: Wrapper generator for managing resources during streaming
async def managed_langgraph_stream_wrapper(request: LangGraphRequest, logger: logging.Logger):
    """
    Manages AsyncExitStack and MCPClient lifecycle for streaming responses.
    Initializes graph and then yields events from langgraph_stream_response_generator.
    """
    # 放到要用的時候才 init，不然loading 會花時間
    from langgraph.errors import GraphRecursionError
    import anthropic # Keep relevant imports if needed for error handling here

    try:
        async with AsyncExitStack() as stack:
            mcp_client = None
            # Ensure config and mcp_config exist before access
            config = request.config or {}
            mcp_config = config.get("mcp_config")
            print(f"mcp_config: {mcp_config}")

            if mcp_config and MultiServerMCPClient:
                logger.info("MCP config detected, initializing MultiServerMCPClient for stream...")
                try:
                    client_instance = MultiServerMCPClient(mcp_config)
                    mcp_client = await stack.enter_async_context(client_instance)
                    logger.info("MultiServerMCPClient initialized and managed by stack for stream.")
                except Exception as e_client:
                    logger.error(f"Error initializing MCPClient for stream: {e_client}", exc_info=True)
                    # Decide how to handle client init error: yield an error event or raise?
                    # Yielding an error event might be better for streaming UX.
                    error_payload = json.dumps({"error": f"MCP Client Initialization Error: {e_client}"})
                    yield f"data: {error_payload}\n\n"
                    return # Stop the generator if MCP client fails

            # --- Graph and State Initialization (Inside the stack) ---
            logger.info("Getting graph and initial state for stream...")
            graph, graph_config = await get_graph(
                request.graph_name,
                request.config,
                request.stream, # Pass stream=True
                request.messages,
                request.user_input,
                mcp_client=mcp_client, # Pass the managed client instance
            )

            # Determine model name for init_state caching logic if needed
            # user_input_model_name = request.config.get("model_name", "")
            # enable_caching = get_react_agent_model_name(user_input_model_name).startswith("claude-") # Example

            init_state = get_init_state(
                request.graph_name,
                request.user_input,
                request.config,
                request.messages,
                False # enable_prompt_caching=enable_caching # Pass caching flag if used
            )

            thread_id = request.thread_id if request.thread_id else str(uuid.uuid4())
            logger.info(f"Streaming with thread_id: {thread_id}")

            # --- Yield from the actual stream response generator ---
            # Pass the configured graph and other necessary parameters
            async for event in langgraph_stream_response_generator(
                thread_id,
                init_state,
                graph,
                request.need_resume,
                logger,
                graph_config,
            ):
                yield event # Yield the formatted event string

    except anthropic.RateLimitError as e:
        # Handle rate limit errors specifically for streaming if needed
        # Note: Retry logic might be complex to implement correctly within a generator.
        #       Consider if retry should happen at a higher level or if yielding an error is sufficient.
        logger.error(f"Anthropic RateLimitError during stream setup/execution: {e}", exc_info=True)
        error_payload = json.dumps({"error": f"Rate Limit Error: {e}", "retry_possible": False}) # Indicate no auto-retry here
        yield f"data: {error_payload}\n\n"
        yield "data: [DONE]\n\n" # Ensure stream terminates correctly

    except GraphRecursionError as e:
        # Handle recursion errors specifically (can happen during graph execution)
        logger.error(f"GraphRecursionError during stream: {e} for thread_id: {thread_id}", error=str(e), exc_info=True)
        try:
            error_msg = json.dumps({"error": ERR_GRAPH_RECURSION_ERROR, "detail": str(e)})
            yield f"data: {error_msg}\n\n"
        except Exception as inner_e:
            logger.error(f"Error serializing GraphRecursionError for stream: {inner_e}", exc_info=True)
            yield f"data: {json.dumps({'error': ERR_GRAPH_RECURSION_ERROR})}\n\n"
        yield "data: [DONE]\n\n" # Ensure stream terminates correctly

    except Exception as e:
        # Catch-all for other errors during setup or streaming
        import traceback
        tb_str = traceback.format_exc()
        logger.error(f"Unhandled exception in managed_langgraph_stream_wrapper: {e}", exc_info=True, traceback=tb_str)
        error_payload = json.dumps({"error": f"Streaming Error: {e}", "detail": tb_str})
        yield f"data: {error_payload}\n\n"
        yield "data: [DONE]\n\n" # Ensure stream terminates correctly


# RENAMED: Original langgraph_stream_response, now focused on generation
async def langgraph_stream_response_generator(
    thread_id: str,
    init_state: Dict,
    graph: Any, # Receives the already configured graph
    need_resume: bool = False,
    logger: logging.Logger = default_logger,
    extra_config: Optional[Dict] = None,
):
    """
    Generates LangGraph stream events using langgraph_runner.
    Handles formatting ('data: ...') and '[DONE]' signal.
    Exception handling specific to langgraph_runner execution.
    """
    from langgraph.errors import GraphRecursionError # Keep specific error import here

    try:
        logger.info(
            "Starting langgraph_runner iteration",
            thread_id=thread_id,
            need_resume=need_resume,
        )
        final_event = None
        first_event = True # To potentially log first event differently if needed
        async for event in langgraph_runner(
            thread_id, init_state, graph, need_resume, extra_config
        ):
            final_event = event # Keep track of the last event
            event_json_str = langgraph_event_to_json(event) # Serialize event safely
            if first_event:
                 # Optional: Different logging for the very first event chunk
                 logger.debug(f"First stream event for {thread_id}: {event_json_str[:200]}...") # Log truncated first event
                 first_event = False

            # print statement for local debugging if needed
            # from datetime import datetime
            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), event_json_str)

            yield f"data: {event_json_str}\n\n"

        # Log details about the final event if needed
        if final_event:
            logger.info(
                "Finished langgraph_runner iteration",
                thread_id=thread_id,
                final_event_type=final_event.get('event'),
                # final_event_data=langgraph_event_to_json(final_event) # Log full final event if useful
            )
        else:
            logger.warning(
                "langgraph_runner finished without yielding any events",
                 thread_id=thread_id,
            )

        yield "data: [DONE]\n\n" # Signal end of stream

    # Error handling remains here as these errors occur during langgraph_runner
    except GraphRecursionError as e:
        logger.error(
            f"GraphRecursionError in stream generator: {e} for thread_id: {thread_id}",
            error=str(e),
            exc_info=True,
        )
        try:
            error_msg = json.dumps({"error": ERR_GRAPH_RECURSION_ERROR, "detail": str(e)})
            yield f"data: {error_msg}\n\n"
        except Exception as inner_e:
            logger.error(f"Error serializing GraphRecursionError msg: {inner_e}", exc_info=True)
            yield f"data: {json.dumps({'error': ERR_GRAPH_RECURSION_ERROR})}\n\n"
        # Ensure [DONE] is sent even after handled error to terminate client side
        yield "data: [DONE]\n\n"

    except Exception as e:
        # Catch errors specifically from langgraph_runner or event processing
        import traceback
        tb_str = traceback.format_exc()
        logger.error(
            f"Exception in stream generator: {e} for thread_id: {thread_id}",
            error=str(e),
            exc_info=True,
            traceback=tb_str
        )
        error_response = {"error": f"Stream Generation Error: {e}", "detail": tb_str}
        yield f"data: {json.dumps(error_response)}\n\n"
        # Ensure [DONE] is sent even after handled error
        yield "data: [DONE]\n\n"


@router.get("/list", response_model=SupportedGraphsResponse)
async def list_supported_graphs():
    """
    列出所有支援的 LangGraph names

    Returns:
        包含所有支援的 graph names 的列表
    """
    return SupportedGraphsResponse(graphs=list(SUPPORTED_GRAPH_NAMES))
