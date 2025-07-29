import json
from typing import ClassVar, Dict, Optional

from langchain_core.tools import BaseTool
from langchain_core.runnables import RunnableConfig

from botrun_flow_lang.constants import LANG_EN, LANG_ZH_TW
from botrun_flow_lang.langgraph_agents.agents.util.plotly_util import (
    generate_plotly_files,
)


class PlotlyChartTool(BaseTool):
    # Class attributes
    tool_name: ClassVar[str] = "create_plotly_chart"

    # Multi-language descriptions
    descriptions: ClassVar[Dict[str, str]] = {
        LANG_EN: """
    Create an interactive Plotly visualization and return its URL.
    This URL should be provided to the user,
    as they will need to access it to view the interactive chart in their web browser.

    Scenarios for using create_plotly_chart:
    - Need to create data visualizations and charts
    - Need to show data trends (line charts)
    - Need to compare values (bar charts, pie charts)
    - Need to show distributions (scatter plots, heat maps)
    - Need to display time series data (timeline charts)
    - Need to show geographic information (maps)
    - Need to perform multidimensional data analysis (3D charts, bubble charts)
    - Need to show statistical distributions (box plots)
    - Need to show cumulative trends (area charts)
    - Need interactive data exploration

    Integration with Other Tools:
    This function can be used in conjunction with chat_with_imgs and chat_with_pdf when they return data
    suitable for visualization. When those tools detect a need for visualization, they will return a JSON string
    with a "__plotly_data__" key, which can be directly passed to this function.

    Example workflow:
    1. User asks to analyze and visualize data from images/PDFs
    2. chat_with_imgs or chat_with_pdf returns JSON string with "__plotly_data__" key
    3. Pass that string to this function to get an interactive visualization URL

    Supported Chart Types:
    - Line charts: For showing trends and time series data
    - Bar charts: For comparing values across categories
    - Pie charts: For showing proportions of a whole
    - Scatter plots: For showing relationships between variables
    - Heat maps: For showing patterns in matrix data
    - Box plots: For showing statistical distributions
    - Geographic maps: For showing spatial data
    - 3D plots: For showing three-dimensional data
    - Bubble charts: For showing three variables in 2D
    - Area charts: For showing cumulative totals over time

    The figure_data should be a JSON string containing plotly figure specifications with 'data' and 'layout'.
    Example:
    {
        'data': [{
            'type': 'scatter',
            'x': [1, 2, 3, 4],
            'y': [10, 15, 13, 17]
        }],
        'layout': {
            'title': 'My Plot'
        }
    }

    Args:
        figure_data: JSON string containing plotly figure specifications or output from chat_with_imgs/chat_with_pdf.
                    Will be parsed using json.loads().
        title: Optional title for the plot.

    Returns:
        str: URL for the interactive HTML visualization. This URL should be provided to the user,
             as they will need to access it to view the interactive chart in their web browser.
    """,
        LANG_ZH_TW: """
    Create an interactive Plotly visualization and return its URL.
    This URL should be provided to the user,
    as they will need to access it to view the interactive chart in their web browser.

    使用 create_plotly_chart 的情境：
    - 提到「圖表」、「統計圖」、「視覺化」等字眼
    - 需要呈現數據趨勢（折線圖）
    - 需要比較數值（長條圖、圓餅圖）
    - 需要展示分布情況（散點圖、熱力圖）
    - 需要顯示時間序列資料（時間軸圖）
    - 需要展示地理資訊（地圖）
    - 需要多維度資料分析（3D圖、氣泡圖）
    - 需要展示統計分布（箱型圖）
    - 需要展示累積趨勢（面積圖）
    - 需要互動式資料探索

    Integration with Other Tools:
    This function can be used in conjunction with chat_with_imgs and chat_with_pdf when they return data
    suitable for visualization. When those tools detect a need for visualization, they will return a JSON string
    with a "__plotly_data__" key, which can be directly passed to this function.

    Example workflow:
    1. User asks to analyze and visualize data from images/PDFs
    2. chat_with_imgs or chat_with_pdf returns JSON string with "__plotly_data__" key
    3. Pass that string to this function to get an interactive visualization URL

    Supported Chart Types:
    - Line charts: For showing trends and time series data
    - Bar charts: For comparing values across categories
    - Pie charts: For showing proportions of a whole
    - Scatter plots: For showing relationships between variables
    - Heat maps: For showing patterns in matrix data
    - Box plots: For showing statistical distributions
    - Geographic maps: For showing spatial data
    - 3D plots: For showing three-dimensional data
    - Bubble charts: For showing three variables in 2D
    - Area charts: For showing cumulative totals over time

    The figure_data should be a JSON string containing plotly figure specifications with 'data' and 'layout'.
    Example:
    {
        'data': [{
            'type': 'scatter',
            'x': [1, 2, 3, 4],
            'y': [10, 15, 13, 17]
        }],
        'layout': {
            'title': 'My Plot'
        }
    }

    Args:
        figure_data: JSON string containing plotly figure specifications or output from chat_with_imgs/chat_with_pdf.
                    Will be parsed using json.loads().
        title: Optional title for the plot. If provided, must be in Traditional Chinese.
               For example: "台灣人口統計圖表" instead of "Taiwan Population Chart"

    Returns:
        str: URL for the interactive HTML visualization. This URL should be provided to the user,
             as they will need to access it to view the interactive chart in their web browser.
    """,
    }

    # Pydantic model fields
    name: str = "create_plotly_chart"
    description: str = descriptions[LANG_EN]

    @classmethod
    def for_language(cls, lang: str = LANG_EN):
        """Create a language-specific instance of the tool"""
        # Get the description for the specified language, or use English as default
        description = cls.descriptions.get(lang, cls.descriptions.get(LANG_EN))
        return cls(name=cls.tool_name, description=description)

    def _run(
        self,
        figure_data: str,
        title: Optional[str] = None,
        config: RunnableConfig = None,
    ) -> str:
        """
        Generate a Plotly chart and return its URL
        """
        from botrun_flow_lang.utils.botrun_logger import BotrunLogger

        logger = BotrunLogger()
        logger.info(f"create_plotly_chart figure_data: {figure_data} title: {title}")
        try:
            # Parse the JSON string into a dictionary
            figure_dict = json.loads(figure_data)

            # If the input is from chat_with_imgs or chat_with_pdf, extract the plotly data
            if "__plotly_data__" in figure_dict:
                figure_dict = figure_dict["__plotly_data__"]

            html_url = generate_plotly_files(
                figure_dict,
                config.get("configurable", {}).get("botrun_flow_lang_url", ""),
                config.get("configurable", {}).get("user_id", ""),
                title,
            )
            logger.info(f"create_plotly_chart generated============> {html_url}")
            return html_url
        except Exception as e:
            logger.error(
                f"create_plotly_chart error: {e}",
                error=str(e),
                exc_info=True,
            )
            return f"Error creating visualization URL: {str(e)}"
