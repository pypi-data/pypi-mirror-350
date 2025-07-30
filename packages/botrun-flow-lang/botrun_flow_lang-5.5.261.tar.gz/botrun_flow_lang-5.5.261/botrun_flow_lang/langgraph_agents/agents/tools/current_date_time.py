import pytz
from datetime import datetime
from typing import ClassVar, Dict

from langchain_core.tools import BaseTool

from langchain_core.runnables import RunnableConfig

from botrun_flow_lang.constants import LANG_EN, LANG_ZH_TW


class CurrentDateTimeTool(BaseTool):

    # 類屬性定義
    tool_name: ClassVar[str] = "current_date_time"

    # 定義多語言描述
    descriptions: ClassVar[Dict[str, str]] = {
        LANG_EN: """
    Use this to get the current date and time in local timezone.

    Important: You MUST call this current_date_time function when:
    1. User's query contains time-related words such as:
    - today, now, current
    - this week, next week
    - this month, last month
    - this year, last year, next year
    - recent, lately
    - future, upcoming
    - past, previous
    2. User asks about current events or latest information
    3. User wants to know time-sensitive information
    4. Queries involving relative time expressions

    Examples of when to use current_date_time:
    - "What's the weather today?"
    - "This month's stock market performance"
    - "Any recent news?"
    - "Economic growth from last year until now"
    - "Upcoming events for next week"
    - "This month's sales data"

    Returns:
        str: Current date and time in format "YYYY-MM-DD HH:MM Asia/Taipei"
    """,
        LANG_ZH_TW: """
    Use this to get the current date and time in local timezone.

    Important: You MUST call this current_date_time function when:
    1. User's query contains time-related words such as:
       - 今天、現在、目前
       - 本週、這週、下週
       - 本月、這個月、上個月
       - 今年、去年、明年
       - 最近、近期
       - 未來、將來
       - 過去、以前
    2. User asks about current events or latest information
    3. User wants to know time-sensitive information
    4. Queries involving relative time expressions

    Examples of when to use current_date_time:
    - "今天的天氣如何？"
    - "本月的股市表現"
    - "最近有什麼新聞？"
    - "去年到現在的經濟成長"
    - "未來一週的活動預告"
    - "這個月的銷售數據"

    Returns:
        str: Current date and time in format "YYYY-MM-DD HH:MM Asia/Taipei"
    """,
    }

    # Pydantic 模型字段
    name: str = "current_date_time"
    description: str = descriptions[LANG_EN]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def for_language(cls, lang: str = LANG_EN):
        """創建特定語言版本的工具實例"""
        # 獲取指定語言的描述，如果不存在則使用默認英文描述
        description = cls.descriptions.get(lang, cls.descriptions.get(LANG_EN))
        return cls(name=cls.tool_name, description=description)

    def _run(self, config: RunnableConfig) -> str:
        from botrun_flow_lang.utils.botrun_logger import BotrunLogger

        logger = BotrunLogger()
        try:
            local_tz = pytz.timezone("Asia/Taipei")
            local_time = datetime.now(local_tz)
            logger.info(
                f"current_date_time============> {local_time.strftime('%Y-%m-%d %H:%M %Z')}"
            )
            return local_time.strftime("%Y-%m-%d %H:%M %Z")
        except Exception as e:
            return f"Error: {e}"
