import json
import asyncio
from datetime import datetime
from typing import ClassVar, Dict

from langchain_core.tools import BaseTool
from langchain_core.runnables import RunnableConfig

from botrun_flow_lang.constants import LANG_EN, LANG_ZH_TW
from botrun_flow_lang.langgraph_agents.agents.util.perplexity_search import (
    respond_with_perplexity_search,
)


def format_dates(dt):
    """
    將日期時間格式化為西元和民國格式
    西元格式：yyyy-mm-dd hh:mm:ss
    民國格式：(yyyy-1911)-mm-dd hh:mm:ss
    """
    western_date = dt.strftime("%Y-%m-%d %H:%M:%S")
    taiwan_year = dt.year - 1911
    taiwan_date = f"{taiwan_year}-{dt.strftime('%m-%d %H:%M:%S')}"

    return {"western_date": western_date, "taiwan_date": taiwan_date}


class WebSearchTool(BaseTool):
    # 類屬性定義
    tool_name: ClassVar[str] = "web_search"

    # 定義多語言描述
    descriptions: ClassVar[Dict[str, str]] = {
        LANG_EN: """
    Use this to search the web when you need up-to-date information or when your knowledge is insufficient.
    This tool uses Perplexity to perform web searches and provides detailed answers with citations.

    Unless the user insists on multiple-round searches, this tool can search for multiple conditions at once, for example:
    - Good: web_search("Search for today's sports, financial, and political news")
    - Unnecessary: Making separate searches for sports, financial, and political news

    Time/Date Information Requirements:
    1. MUST preserve any specific dates or time periods mentioned in the user's query
    2. Include both the current time and any specific time references from the query

    Examples:
    - Basic query:
      User asks: "Population of Japan"
      web_search("Population of Japan")
      Returns: {
          "content": "According to the latest statistics, Japan's population is about 125 million...",
          "citations": [
              {"title": "Statistics Bureau of Japan", "url": "https://www.stat.go.jp/..."},
              {"title": "World Bank Data", "url": "https://data.worldbank.org/..."}
          ]
      }

    - Query with specific date:
      User asks: "Look up news from January 15, 2023"
      web_search("Look up news from January 15, 2023")
      Returns: {
          "content": "News from January 15, 2023 includes...",
          "citations": [
              {"title": "BBC News", "url": "https://www.bbc.com/..."},
              {"title": "Reuters", "url": "https://www.reuters.com/..."}
          ]
      }

    - Location-specific query:
      User asks: "Weather in Paris today"
      web_search("Weather in Paris today")
      Returns: {
          "content": "Today's weather in Paris shows...",
          "citations": [
              {"title": "Weather Service", "url": "https://www.weather.com/..."},
              {"title": "Meteorological Office", "url": "https://www.metoffice.gov.uk/..."}
          ]
      }

    Args:
        user_input: The search query or question you want to find information about.
                   MUST include any specific time periods or dates from the original query.
                   Examples of time formats to preserve:
                   - Specific dates: "2025/1/1", "2023-12-31", "January 15, 2023"
                   - Years: "2023"
                   - Quarters/Months: "Q1", "January", "First quarter"
                   - Time periods: "past three years", "next five years"
                   - Relative time: "yesterday", "next week", "last month"
    Returns:
        dict: A dictionary containing:
              - content (str): The detailed answer based on web search results
              - citations (list): A list of URLs, citations are important to provide to the user
    """,
        LANG_ZH_TW: """
    Use this to search the web when you need up-to-date information or when your knowledge is insufficient.
    This tool uses Perplexity to perform web searches and provides detailed answers with citations.

    除非使用者堅持要做多輪搜尋，不然這個工具能夠一次進行多個條件的搜尋，比如：
    一次進行多條件範例1：
    - 可以：
        - web_search("搜尋今天的體育、財經、政治新聞")
    - 不需要：
        - web_search("搜尋今天的體育新聞")
        - web_search("搜尋今天的財經新聞")
        - web_search("搜尋今天的政台新聞")

    Time/Date Information Requirements:
    1. MUST preserve any specific dates or time periods mentioned in the user's query
    2. Include both the current time and any specific time references from the query

    Examples:
    - Basic query:
      User asks: "台灣的人口數量"
      web_search("台灣的人口數量")
      Actual search: "台灣的人口數量"
      Returns: {
          "content": "根據最新統計，台灣人口約為2300萬...",
          "citations": [
              {"title": "內政部統計處", "url": "https://www.moi.gov.tw/..."},
              {"title": "國家發展委員會", "url": "https://www.ndc.gov.tw/..."}
          ]
      }

    - Query with specific date:
      User asks: "幫我查詢 2025/1/1 的新聞"
      web_search("幫我查詢 2025/1/1 的新聞")
      Returns: {
          "content": "關於2025年1月1日的新聞預測...",
          "citations": [
              {"title": "經濟日報", "url": "https://money.udn.com/..."},
              {"title": "中央社", "url": "https://www.cna.com.tw/..."}
          ]
      }

    Args:
        user_input: The search query or question you want to find information about.
                   MUST include any specific time periods or dates from the original query.
                   Examples of time formats to preserve:
                   - Specific dates: "2025/1/1", "2023-12-31"
                   - Years: "2023年"
                   - Quarters/Months: "第一季", "Q1", "一月"
                   - Time periods: "過去三年", "未來五年"
    Returns:
        dict: A dictionary containing:
              - content (str): The detailed answer based on web search results
              - citations (list): A list of URLs, citation對使用者很重要，務必提供給使用者
    """,
    }

    # Pydantic 模型字段
    name: str = "web_search"
    description: str = descriptions[LANG_EN]
    lang: str = LANG_EN

    @classmethod
    def for_language(cls, lang: str = LANG_EN):
        """創建特定語言版本的工具實例"""
        # 獲取指定語言的描述，如果不存在則使用默認英文描述
        description = cls.descriptions.get(lang, cls.descriptions.get(LANG_EN))
        return cls(name=cls.tool_name, description=description, lang=lang)

    def _run(self, user_input: str, config: RunnableConfig = None) -> dict:
        """
        執行Web搜索並返回結果
        """
        from botrun_flow_lang.utils.botrun_logger import BotrunLogger

        logger = BotrunLogger()
        logger.info(f"web_search user_input: {user_input}")
        now = datetime.now()
        dates = format_dates(now)
        western_date = dates["western_date"]
        taiwan_date = dates["taiwan_date"]
        logger.info(f"western_date: {western_date} taiwan_date: {taiwan_date}")
        if self.lang.startswith("zh"):
            final_input = f"現在的西元時間：{western_date}\n現在的民國時間：{taiwan_date}\n\n使用者的提問是：{user_input}"
        else:
            final_input = f"The current date: {western_date}\nThe user's question is: {user_input}"
        try:
            # 定義一個內部的非同步函數來處理搜尋結果
            async def process_search():
                search_result = {
                    "content": "",
                    "citations": [],
                }
                async for event in respond_with_perplexity_search(
                    final_input,
                    user_prompt_prefix="",
                    messages_for_llm=[],
                    domain_filter=[],
                    stream=False,
                    structured_output=True,
                ):
                    if event and isinstance(event.chunk, str):
                        search_result = json.loads(event.chunk)
                return search_result

            # 使用 asyncio.run 執行非同步函數
            search_result = asyncio.run(process_search())
        except Exception as e:
            import traceback

            traceback.print_exc()
            return f"Error during web search: {str(e)}"
        return (
            search_result
            if search_result
            else {"content": "No results found.", "citations": []}
        )
