import os
import pytz
import asyncio
import os
import json
from datetime import datetime
from typing import ClassVar, Dict, List, Optional, Any

from langchain_core.messages import SystemMessage

from botrun_flow_lang.constants import LANG_EN, LANG_ZH_TW
from botrun_flow_lang.langgraph_agents.agents.util.img_util import analyze_imgs

from botrun_flow_lang.langgraph_agents.agents.util.local_files import (
    upload_and_get_tmp_public_url,
)

from botrun_flow_lang.langgraph_agents.agents.util.pdf_analyzer import analyze_pdf

from botrun_flow_lang.langgraph_agents.agents.util.perplexity_search import (
    respond_with_perplexity_search,
)
from botrun_flow_lang.models.nodes.utils import scrape_single_url

from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig

from langchain_core.tools import BaseTool

from langchain_core.tools import tool

from botrun_flow_lang.utils.botrun_logger import BotrunLogger

from botrun_flow_lang.langgraph_agents.agents.util.plotly_util import (
    generate_plotly_files,
)

from botrun_flow_lang.langgraph_agents.agents.util.mermaid_util import (
    generate_mermaid_files,
)

from botrun_flow_lang.langgraph_agents.agents.util.html_util import (
    generate_html_file,
)

from botrun_flow_lang.langgraph_agents.agents.tools.current_date_time import (
    CurrentDateTimeTool,
)
from botrun_flow_lang.langgraph_agents.agents.tools.web_search import WebSearchTool
from botrun_flow_lang.langgraph_agents.agents.tools.create_mermaid_diagram import (
    MermaidDiagramTool,
)
from botrun_flow_lang.langgraph_agents.agents.tools.create_plotly_chart import (
    PlotlyChartTool,
)

from botrun_flow_lang.langgraph_agents.agents.checkpointer.firestore_checkpointer import (
    AsyncFirestoreCheckpointer,
)

from langgraph.prebuilt import create_react_agent

from botrun_flow_lang.utils.clients.rate_limit_client import RateLimitClient

from dotenv import load_dotenv

import copy  # 用於深拷貝 schema，避免意外修改原始對象

# 假設 MultiServerMCPClient 和 StructuredTool 已經被正確導入
from langchain.tools import StructuredTool  # 或 langchain_core.tools
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

# logger = default_logger
logger = BotrunLogger()


# Define BotrunRateLimitException for user-visible rate limit errors
class BotrunRateLimitException(Exception):
    """
    Exception that should be displayed directly to the user.
    All error messages will be prefixed with '[Please tell user error]'
    """

    def __init__(self, message):
        self.message = f"[Please tell user error] {message}"
        super().__init__(self.message)


# Load Anthropic API keys from environment
# anthropic_api_keys_str = os.getenv("ANTHROPIC_API_KEYS", "")
# anthropic_api_keys = [
#     key.strip() for key in anthropic_api_keys_str.split(",") if key.strip()
# ]

# Initialize the model with key rotation if multiple keys are available
# if anthropic_api_keys:
#     model = RotatingChatAnthropic(
#         model_name="claude-3-7-sonnet-latest",
#         keys=anthropic_api_keys,
#         temperature=0,
#         max_tokens=8192,
#     )
# 建立 AWS Session
# session = boto3.Session(
#     aws_access_key_id="",
#     aws_secret_access_key="",
#     region_name="us-west-2",
# )


# # 使用該 Session 初始化 Bedrock 客戶端
# bedrock_runtime = session.client(
#     service_name="bedrock-runtime",
# )
# model = ChatBedrockConverse(
#     model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
#     client=bedrock_runtime,
#     temperature=0,
#     max_tokens=8192,
# )
# else:
# Fallback to traditional initialization if no keys are specified
def get_react_agent_model_name(model_name: str = ""):
    final_model_name = model_name
    if final_model_name == "":
        final_model_name = "claude-sonnet-4-20250514"
    logger.info(f"final_model_name: {final_model_name}")
    return final_model_name


ANTHROPIC_MAX_TOKENS = 64000


def get_react_agent_model(model_name: str = ""):
    final_model_name = get_react_agent_model_name(model_name)
    if final_model_name.startswith("gemini-"):
        # 放到要用的時候才 init，不然loading 會花時間
        from langchain_google_genai import ChatGoogleGenerativeAI

        model = ChatGoogleGenerativeAI(model=final_model_name, temperature=0)
        logger.info(f"model ChatGoogleGenerativeAI {final_model_name}")
    elif final_model_name.startswith("claude-"):
        anthropic_api_keys_str = os.getenv("ANTHROPIC_API_KEYS", "")
        anthropic_api_keys = [
            key.strip() for key in anthropic_api_keys_str.split(",") if key.strip()
        ]
        if anthropic_api_keys:
            # 放到要用的時候才 import，不然loading 會花時間
            from botrun_flow_lang.langgraph_agents.agents.util.model_utils import (
                RotatingChatAnthropic,
            )

            model = RotatingChatAnthropic(
                model_name=final_model_name,
                keys=anthropic_api_keys,
                temperature=0,
                max_tokens=ANTHROPIC_MAX_TOKENS,
            )
            logger.info(f"model RotatingChatAnthropic {final_model_name}")
        elif os.getenv("OPENROUTER_API_KEY") and os.getenv("OPENROUTER_BASE_URL"):
            # 放到要用的時候才 init，不然loading 會花時間
            from langchain_openai import ChatOpenAI

            openrouter_model_name = "anthropic/claude-sonnet-4"
            # openrouter_model_name = "openai/o4-mini-high"
            # openrouter_model_name = "openai/gpt-4.1"
            model = ChatOpenAI(
                openai_api_key=os.getenv("OPENROUTER_API_KEY"),
                openai_api_base=os.getenv("OPENROUTER_BASE_URL"),
                model_name=openrouter_model_name,
                temperature=0,
                max_tokens=ANTHROPIC_MAX_TOKENS,
                model_kwargs={
                    # "headers": {
                    #     "HTTP-Referer": getenv("YOUR_SITE_URL"),
                    #     "X-Title": getenv("YOUR_SITE_NAME"),
                    # }
                },
            )
            logger.info(f"model OpenRouter {openrouter_model_name}")
        else:
            # 放到要用的時候才 init，不然loading 會花時間
            from langchain_anthropic import ChatAnthropic

            model = ChatAnthropic(
                model=final_model_name,
                temperature=0,
                max_tokens=ANTHROPIC_MAX_TOKENS,
                # model_kwargs={
                # "extra_headers": {
                # "anthropic-beta": "token-efficient-tools-2025-02-19",
                # "anthropic-beta": "output-128k-2025-02-19",
                # }
                # },
            )
            logger.info(f"model ChatAnthropic {final_model_name}")
    return model


# model = ChatOpenAI(model="gpt-4o", temperature=0)
# model = ChatGoogleGenerativeAI(model="gemini-2.0-pro-exp-02-05", temperature=0)
# model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)


# For this tutorial we will use custom tool that returns pre-defined values for weather in two cities (NYC & SF)


@tool
def scrape(url: str, config: RunnableConfig):
    """
    Use this to scrape the web.
    as it provides better results for video content.

    Args:
        url: the url to scrape
    """
    try:
        logger.info(f"scrape {url}")
        return asyncio.run(scrape_single_url(url))
    except Exception as e:
        logger.error(
            f"scrape {url} error: {e}",
            error=str(e),
            exc_info=True,
        )
        return f"Error: {e}"


@tool
def compare_date_time(user_specified_date_time: str, current_date_time: str):
    """
    比較使用者指定的日期時間與當前時間，判斷是過去還是未來。

    Important: 當使用者想要比較特定日期時間與現在的關係時，請使用此函數。
    適用情境包括：
    1. 使用者提供特定日期時間，想知道與現在的相對關係
    2. 使用者詢問某個日期時間是否已經過去或尚未到來
    3. 使用者需要判斷某個時間點相對於現在的狀態

    Args:
        user_specified_date_time: 使用者指定的日期時間，格式必須為 "YYYY-MM-DD HH:MM Asia/Taipei"
                      例如："2023-12-31 23:59 Asia/Taipei"
        current_date_time: 當前日期時間，通常由 current_date_time() 函數提供
                         格式同樣為 "YYYY-MM-DD HH:MM Asia/Taipei"

    Examples of when to use compare_date_time:
    - "2025-01-01 00:00 是過去還是未來？"
    - "判斷 2023-05-20 15:30 與現在的關係"
    - "2024-12-25 18:00 這個時間點已經過去了嗎？"
    - "比較 2022-10-01 08:00 和現在時間"

    Returns:
        str: 比較結果，格式為 "使用者指定的時間是{過去/未來}"
    """
    try:
        logger.info(
            f"compare_date_time user_specified_date_time: {user_specified_date_time} current_date_time: {current_date_time}"
        )
        # 解析使用者提供的日期時間
        user_dt = datetime.strptime(
            user_specified_date_time.split(" Asia/Taipei")[0], "%Y-%m-%d %H:%M"
        )
        user_dt = pytz.timezone("Asia/Taipei").localize(user_dt)

        # 解析當前時間
        now = datetime.strptime(
            current_date_time.split(" Asia/Taipei")[0], "%Y-%m-%d %H:%M"
        )
        now = pytz.timezone("Asia/Taipei").localize(now)

        # 計算時間差（秒）
        time_diff = (user_dt - now).total_seconds()

        # 判斷是過去還是未來
        if time_diff < 0:
            result = "過去"
        else:
            result = "未來"
        logger.info(f"使用者指定的時間是{result}")
        return f"使用者指定的時間是{result}"
    except Exception as e:
        return f"Error: {e}"


@tool
def chat_with_pdf(pdf_url: str, user_input: str, config: RunnableConfig):
    """
    Use this to chat with a PDF file.
    User can ask about any text, pictures, charts, and tables in PDFs that is provided. Some sample use cases:
    - Analyzing financial reports and understanding charts/tables
    - Extracting key information from legal documents
    - Translation assistance for documents
    - Converting document information into structured formats

    Data Visualization Integration:
    When the user's input indicates a need for comparison or data visualization (e.g., "compare the quarterly profits",
    "show the trend of sales"), this function can return data in a format suitable for Plotly visualization.
    The returned data will be a dictionary with a special key "__plotly_data__" containing:
    {
        "__plotly_data__": {
            "data": [...],  # Plotly data array
            "layout": {...}  # Plotly layout object
        }
    }
    You can then pass this data to create_plotly_chart to generate an interactive chart.

    If you have a local PDF file, you can use generate_tmp_public_url tool to get a public URL first:
    1. Call generate_tmp_public_url with your local PDF file path
    2. Use the returned URL as the pdf_url parameter for this function

    Args:
        pdf_url: the URL to the PDF file (can be generated using generate_tmp_public_url for local files)
        user_input: the user's input

    Returns:
        str: Analysis result or Plotly-compatible data structure if visualization is needed
    """
    logger.info(f"chat_with_pdf pdf_url: {pdf_url} user_input: {user_input}")
    if not pdf_url.startswith("http"):
        pdf_url = upload_and_get_tmp_public_url(
            pdf_url,
            config.get("configurable", {}).get("botrun_flow_lang_url", ""),
            config.get("configurable", {}).get("user_id", ""),
        )
    return analyze_pdf(pdf_url, user_input)


@tool
def generate_image(user_input: str, config: RunnableConfig):
    """
    Use this to generate high-quality images using DALL-E 3.

    Capabilities:
    - Creates photorealistic images and art
    - Handles complex scenes and compositions
    - Maintains consistent styles
    - Follows detailed prompts with high accuracy
    - Supports various artistic styles and mediums

    Best practices for prompts:
    - Be specific about style, mood, lighting, and composition
    - Include details about perspective and setting
    - Specify artistic medium if desired (e.g., "oil painting", "digital art")
    - Mention color schemes or specific colors
    - Describe the atmosphere or emotion you want to convey

    Limitations:
    - Cannot generate images of public figures or celebrities
    - Avoids harmful, violent, or adult content
    - May have inconsistencies with hands, faces, or text
    - Cannot generate exact copies of existing artworks or brands
    - Limited to single image generation per request
    - Subject to daily usage limits

    Rate Limit Handling:
    - If you encounter an error message starting with "[Please tell user error]",
      you must report this error message directly to the user as it indicates
      they have reached their daily image generation limit.

    Args:
        user_input: Detailed description of the image you want to generate.
                   Be specific about style, content, and composition.

    Returns:
        str: URL to the generated image, or error message if generation fails
    """
    try:
        # Get user_id from DICT_VAR
        logger.info(f"generate_image user_input: {user_input}")
        user_id = config.get("configurable", {}).get("user_id", "")
        if not user_id:
            logger.error("User ID not available for rate limit check")
            raise Exception("User ID not available for rate limit check")

        # Check rate limit before generating image
        rate_limit_client = RateLimitClient()
        rate_limit_info = asyncio.run(rate_limit_client.get_rate_limit(user_id))

        # Check if user can generate an image
        drawing_info = rate_limit_info.get("drawing", {})
        can_use = drawing_info.get("can_use", False)

        if not can_use:
            daily_limit = drawing_info.get("daily_limit", 0)
            current_usage = drawing_info.get("current_usage", 0)
            logger.error(
                f"User {user_id} has reached daily limit of {daily_limit} image generations. Current usage: {current_usage}. Please try again tomorrow."
            )
            raise BotrunRateLimitException(
                f"You have reached your daily limit of {daily_limit} image generations. Current usage: {current_usage}. Please try again tomorrow."
            )
        # 放到要用的時候才 import，不然loading 會花時間
        from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
        from langchain_community.callbacks import get_openai_callback

        # Proceed with image generation using DALL-E API Wrapper
        dalle_wrapper = DallEAPIWrapper(
            api_key=os.getenv("OPENAI_API_KEY"), model="dall-e-3"
        )

        # DallEAPIWrapper doesn't provide token usage directly, so we use OpenAI callback
        with get_openai_callback() as cb:
            image_url = dalle_wrapper.run(user_input)
            # For DALL-E, token usage is estimated based on prompt length
            # Note: This is an approximation as DALL-E doesn't report exact token usage
            logger.info(
                f"generate_image=======> Estimated prompt tokens: {cb.prompt_tokens}, completion tokens: {cb.completion_tokens}"
            )

        logger.info(f"generate_image generated============> {image_url}")

        # Update usage counter after successful generation
        asyncio.run(rate_limit_client.update_drawing_usage(user_id))

        return image_url
    except Exception as e:
        # Check if this is a user-visible exception
        logger.error(
            f"generate_image error: {e}",
            error=str(e),
            exc_info=True,
        )

        if str(e).startswith("[Please tell user error]"):
            return str(e)  # Return the error message as is
        return f"Error: {e}"


@tool
def chat_with_imgs(img_urls: list[str], user_input: str, config: RunnableConfig):
    """
    Use this to analyze and understand multiple images using Claude's vision capabilities.

    If you have local image files, you can use generate_tmp_public_url tool multiple times to get public URLs first:
    1. Call generate_tmp_public_url for each local image file
    2. Collect all returned URLs into a list
    3. Use the list of URLs as the img_urls parameter for this function

    Data Visualization Integration:
    When the user's input indicates a need for comparison or data visualization (e.g., "compare the values in these charts",
    "extract and plot the data from these images"), this function can return data in a format suitable for Plotly visualization.
    The returned data will be a dictionary with a special key "__plotly_data__" containing:
    {
        "__plotly_data__": {
            "data": [...],  # Plotly data array
            "layout": {...}  # Plotly layout object
        }
    }
    You can then pass this data to create_plotly_chart to generate an interactive chart.

    Supported image formats:
    - JPEG, PNG, GIF, WebP
    - Maximum file size: 5MB per image
    - Recommended size: No more than 1568 pixels in either dimension
    - Very small images (under 200 pixels) may degrade performance
    - Can analyze up to 20 images per request

    Capabilities:
    - Analyzing charts, graphs, and diagrams
    - Reading and understanding text in images
    - Describing visual content and scenes
    - Comparing multiple images in a single request
    - Answering questions about image details
    - Identifying relationships between images
    - Extracting data from charts for visualization

    Limitations:
    - Cannot identify or name specific people
    - May have reduced accuracy with low-quality or very small images
    - Limited spatial reasoning abilities
    - Cannot verify if images are AI-generated
    - Not designed for medical diagnosis or healthcare applications

    Args:
        img_urls: List of URLs to the image files (can be generated using generate_tmp_public_url for local files)
        user_input: Question or instruction about the image content(s)

    Returns:
        str: Claude's analysis of the image(s) based on the query, or Plotly-compatible data structure if visualization is needed
    """
    logger.info(f"chat_with_imgs img_urls: {img_urls} user_input: {user_input}")
    new_img_urls = []
    for img_url in img_urls:
        if not img_url.startswith("http"):
            img_url = upload_and_get_tmp_public_url(
                img_url,
                config.get("configurable", {}).get("botrun_flow_lang_url", ""),
                config.get("configurable", {}).get("user_id", ""),
            )
        new_img_urls.append(img_url)
    return analyze_imgs(new_img_urls, user_input)


@tool
def generate_tmp_public_url(file_path: str, config: RunnableConfig) -> str:
    """
    The user will provide you with a local file path. Please use the generate_tmp_public_url tool to create a temporary public URL that allows the user to download this file.
    If the user provides multiple local file paths, call this tool multiple times and collect the return values from each call.

    Args:
        file_path: The path to the local file you want to make publicly accessible

    Returns:
        str: A public URL that can be used to access the file for 7 days

    Raises:
        FileNotFoundError: If the specified file does not exist
    """
    logger.info(f"generate_tmp_public_url file_path: {file_path}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    return upload_and_get_tmp_public_url(
        file_path,
        config.get("configurable", {}).get("botrun_flow_lang_url", ""),
        config.get("configurable", {}).get("user_id", ""),
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


@tool
def create_html_page(
    html_content: str, title: str = None, config: RunnableConfig = None
) -> str:
    """
    Create a custom HTML page and return its URL.
    This URL should be provided to the user, as they will need to access it to view the HTML content in their web browser.

    This tool supports complete HTML documents, including JavaScript and CSS, which can be used to create complex interactive pages.

    Prioritize using the following frameworks for writing HTML and planning CSS versions:
    ```html
    <!-- Tailwind CSS -->
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">

    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <!-- DataTables -->
    <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>

    <!-- Alpine.js -->
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    ```

    To create more attractive, visually appealing pages, consider the following components and libraries:

    Tailwind component libraries (enhance UI design):
    ```html
    <!-- daisyUI - Tailwind CSS component library -->
    <link href="https://cdn.jsdelivr.net/npm/daisyui@3.5.0/dist/full.css" rel="stylesheet">
    ```

    Animation effects (increase visual appeal):
    ```html
    <!-- Animate.css - easy-to-use animation library -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">

    <!-- GSAP - professional-grade animation effects -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.4/gsap.min.js"></script>
    ```

    Advanced visual effects (for special cases):
    ```html
    <!-- Three.js - 3D visual effects -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    ```

    More modern chart libraries:
    ```html
    <!-- ApexCharts - more modern chart effects -->
    <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
    ```

    Table styling:
    ```html
    <!-- DataTables Bootstrap 5 styles -->
    <link href="https://cdn.datatables.net/1.11.5/css/dataTables.bootstrap5.min.css" rel="stylesheet">
    <script src="https://cdn.datatables.net/1.11.5/js/dataTables.bootstrap5.min.js"></script>
    ```

    IMPORTANT: ALWAYS use the frameworks and libraries listed above instead of writing custom CSS or JavaScript. Only in extremely rare cases where the provided libraries cannot meet a specific requirement should you consider writing custom code. This ensures consistency, maintainability, and best practices in design.

    Important note: These tools and libraries are optional and should be selectively used based on specific needs. Not every page needs to use all elements or animation effects. Choose which components and effects to use based on the content characteristics and user needs, avoiding over-design or unnecessary complexity. For example:
    - Simple information displays may only need basic Tailwind styles
    - Not all content needs animation effects; too many animations can distract users
    - daisyUI components should only be used when complex UI elements are needed
    - Chart libraries should be chosen based on data complexity; use Chart.js for simple data and consider ApexCharts for complex data

    Scenarios for using create_html_page:
    - Need to display custom HTML content
    - Need to embed complex interactive content
    - Need to create custom formatted reports or documents
    - Need to use third-party JavaScript libraries
    - Need to display tables, images, and multimedia content
    - Need to create structured and easy-to-read content presentation
    - Need to use CSS styles to create attractive interfaces
    - Need to embed special charts or visual elements

    Input Options:
    You can pass either:
    1. A complete HTML document with doctype, html, head, and body tags
    2. An HTML fragment that will be automatically wrapped in a basic HTML structure

    Supported HTML Features:
    - Complete HTML documents with your own structure
    - Custom JavaScript for interactive elements
    - Custom CSS for styling and layout
    - External libraries and frameworks (via CDN)
    - Tables, lists, and other structural elements
    - Embedded images and multimedia (via URLs)
    - Form elements (though they won't submit data)
    - Responsive design elements
    - Unicode and international text support

    Security Considerations:
    - HTML content is sandboxed in the browser
    - Cannot access user's device or data
    - External resources must be from trusted sources
    - No server-side processing capability
    - No personal data should be included in the HTML

    Example of complete HTML document with recommended frameworks:
    ```html
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Interactive Report</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

        <link href="https://cdn.jsdelivr.net/npm/daisyui@3.5.0/dist/full.css" rel="stylesheet">

        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.4/gsap.min.js"></script>

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <!-- <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script> -->

        <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet">
        <script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>

        <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    </head>
    <body class="bg-gray-50">
        <div class="container mx-auto px-4 py-8 max-w-4xl">
            <h1 class="text-4xl font-bold text-gray-800 mb-6">Performance Analysis Report</h1>
            <p class="mb-6 text-lg text-gray-600">This report provides an analysis of the company's sales data over the past three months.</p>

            <div class="bg-white p-6 rounded-lg shadow-lg mb-8">
                <h2 class="text-xl font-semibold mb-4">Sales Data Chart</h2>
                <div id="salesChart" class="h-80 w-full"></div>
            </div>

            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    const ctx = document.getElementById('salesChart').getContext('2d');
                    new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: ['January', 'February', 'March'],
                            datasets: [{
                                label: 'Sales (Thousands)',
                                data: [1200, 1900, 1500],
                                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                legend: {
                                    position: 'top',
                                }
                            }
                        }
                    });

                    // Optional: Simple animation effect
                    // gsap.from('.bg-white', {
                    //     y: 30,
                    //     opacity: 0,
                    //     duration: 0.8,
                    //     delay: 0.3
                    // });
                });
            </script>
        </div>
    </body>
    </html>
    ```

    Example of HTML fragment with Tailwind and daisyUI classes (will be auto-wrapped):
    ```html
    <div class="p-6 bg-blue-50 rounded-lg shadow-md">
      <h1 class="text-3xl text-gray-800 font-bold mb-4">Client Report</h1>
      <p class="mb-4 text-gray-600">This report contains important information.</p>

      <!-- Optional: Using daisyUI components -->
      <!-- <div class="tabs tabs-boxed mb-4">
        <a class="tab tab-active">Data Analysis</a>
        <a class="tab">Detailed Information</a>
        <a class="tab">Summary</a>
      </div> -->

      <!-- Basic DataTable implementation -->
      <div class="overflow-x-auto">
        <table id="dataTable" class="display w-full">
          <thead>
            <tr>
              <th>Item</th>
              <th>Quantity</th>
              <th>Unit Price</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Product A</td>
              <td>10</td>
              <td>$100</td>
              <td>$1,000</td>
            </tr>
            <tr>
              <td>Product B</td>
              <td>5</td>
              <td>$200</td>
              <td>$1,000</td>
            </tr>
          </tbody>
        </table>
      </div>

      <script>
        // Wait for page to load
        $(document).ready(function() {
          // Basic DataTable settings
          $('#dataTable').DataTable({
            responsive: true
          });

          // Optional: Animation effects
          // If GSAP is included, consider adding the following animation
          // if (typeof gsap !== 'undefined') {
          //   gsap.from('tr', {
          //     y: 20,
          //     opacity: 0,
          //     stagger: 0.1,
          //     delay: 0.3,
          //     duration: 0.3
          //   });
          // }
        });
      </script>
    </div>
    ```

    Args:
        html_content: Complete HTML document or fragment. Can include JavaScript, CSS, and other elements.
        title: Optional title for the HTML page.

    Returns:
        str: URL for the HTML page. This URL should be provided to the user,
             as they will need to access it to view the content in their web browser.
    """
    try:
        logger.info(f"create_html_page html_content: {html_content} title: {title}")
        html_url = generate_html_file(
            html_content,
            config.get("configurable", {}).get("botrun_flow_lang_url", ""),
            config.get("configurable", {}).get("user_id", ""),
            title,
        )
        logger.info(f"create_html_page generated============> {html_url}")
        return html_url
    except Exception as e:
        logger.error(
            f"create_html_page error: {e}",
            error=str(e),
            exc_info=True,
        )
        return f"Error creating HTML page URL: {str(e)}"


# DICT_VAR = {}

# Define the graph

now = datetime.now()
dates = format_dates(now)
western_date = dates["western_date"]
taiwan_date = dates["taiwan_date"]


zh_tw_system_prompt = """
    以下為回應時需注意的準則，請你務必遵守，你會遵守<使用工具 (tools) 需注意的事項>、以及<回應時需注意的準則>。
<回應時需注意的準則>
- 如果 tool 的文件叫你調用其它 tool，請你一定要直接調用，不要叫使用者調用。
- 如果使用者的問題中有指定日期時間，不要預設它是未來或過去，一定要先使用 current_date_time 和 compare_date_time 這兩個工具，以取得現在的日期時間並判斷使用者指定的日期時間是過去或未來，然後再進行後續的動作。比較日期時，注意<時間解讀說明>。
- 如果你要傳給使用者任何的 URL，請確保 URL 是從 tool 回傳的，或是從歷史記錄中找到的，千萬不可自己創造 URL 回傳給使用者。
- 如果A工具回傳的是 URL，B工具的參數需要用到A工具回傳的URL，請直接使用A工具回傳的URL，不要自己創造URL。
- 如果要傳給工具的內容是使用者提問，要注意原始使用者有沒有特別寫：千萬、注意、一定要、不要、務必…等等的字眼，如果有，請你也要將這些字眼包的使用者提問含在user_input中。
</回應時需注意的準則>
<時間解讀說明>
current_date_time 的回傳值，可以幫助判斷使用者查詢是關於過去的歷史資訊，還是關於未來的預測資訊。
這個函數會回傳此時此刻的精確日期時間。例如：
回傳 "2023-03-19 13:23 Asia/Taipei" 代表現在是2023年3月19日 13點23分台北時間。
當比較使用者查詢的日期時：
- 如果使用者問的是 "2023年3月10日23:00到2023年3月11日23:00"，這個日期發生在過去
- 如果使用者問的是 "2023年3月20日23:00到2023年3月21日23:00"，這個日期發生在未來
- 如果使用者問題是 "2023年3月10-11日"，這個日期發生在過去
</時間解讀說明>
<使用工具 (tools) 需注意的事項>
- web_search:
    在所有一般搜尋情況下使用此工具，除非使用者明確提出「深入研究」、「深度研究」、「深入搜尋」、「深度搜尋」等要求。
    
    當使用 web_search 工具時，請先確認前面的 system prompt 以及使用者的提問請求是否包含下列資訊：
    - 搜尋語言
    - 搜尋網站來源
    如果包含上述資訊，請將這些資訊附加於 user_input 結尾，並註明優先搜尋這些語言或網站的資料。

- generate_image: 
    當使用 generate_image 工具時，你必須在回應中包含圖片網址。
    請按照以下格式回應(從 @begin img開始，到 @end 結束，中間包含圖片網址)：
    @begin img("{image_url}") @end

- chat_with_pdf:
    使用者的問題或指令。如果問題中包含以下關鍵字，要在 user_input 中包含以下字句：
    - 「圖表」、「統計圖」、「視覺化」：幫我生成適合的統計圖表，並提供相關 plotly 的資料給我
    - 「趨勢」、「走向」：幫我生成折線圖，並提供相關 plotly 的資料給我
    - 「比較」、「對照」：幫我生成長條圖或圓餅圖，並提供相關 plotly 的資料給我
    - 「分布」、「分散」：幫我生成散點圖或熱力圖，並提供相關 plotly 的資料給我
    - 「時間序列」：幫我生成時間軸圖，並提供相關 plotly 的資料給我
    - 「地理資訊」：幫我生成地圖，並提供相關 plotly 的資料給我
    - 「多維度分析」：幫我生成 3D 圖或氣泡圖，並提供相關 plotly 的資料給我
    - 「流程圖」、「流程」：幫我生成 flowchart，並提供相關 mermaid 的資料給我
    - 「架構圖」、「架構」：幫我生成 flowchart，並提供相關 mermaid 的資料給我
    - 「關係圖」、「關係」：幫我生成 flowchart 或 ER diagram，並提供相關 mermaid 的資料給我
    - 「時序圖」、「序列圖」：幫我生成 sequence diagram，並提供相關 mermaid 的資料給我
    - 「狀態圖」、「狀態」：幫我生成 state diagram，並提供相關 mermaid 的資料給我
    - 「類別圖」、「類別」：幫我生成 class diagram，並提供相關 mermaid 的資料給我
    - 「甘特圖」、「時程圖」：幫我生成 gantt chart，並提供相關 mermaid 的資料給我

- create_plotly_chart:
    當使用 create_plotly_chart 工具時，你必須在回應中包含create_plotly_chart回傳的URL網址。
    請按照以下格式回應：
    [{plotly_chart_title}] ({plotly_chart_url})
    <範例1>
    使用者提問：
    請幫我分析這個PDF的內容，並產出一個圖表給我看
    回應：
    {分析的內容文字}
    我為你製作了一個圖表，請看這個網址：
    [{plotly_chart_title}] ({plotly_chart_url})
    </範例1>
    <範例2>
    使用者提問：
    請幫我深度分析這個檔案內容，並產出讓使用者好懂的比較圖
    回應：
    {分析的內容文字}
    我為你製作了一個圖表，請看這個網址：
    [{plotly_chart_title}] ({plotly_chart_url})
    </範例2>

- create_mermaid_diagram:
    當使用 create_mermaid_diagram 工具時，你必須在回應中包含create_mermaid_diagram回傳的URL網址。
    請按照以下格式回應：
    [{mermaid_diagram_title}] ({mermaid_diagram_url})
    <範例1>
    使用者提問：
    請幫我分析這個PDF的內容，根據開會決議，產出一個行動流程圖
    回應：
    {分析的內容文字}
    我為你製作了一個流程圖，請看這個網址：
    [{mermaid_diagram_title}] ({mermaid_diagram_url})
    </範例1>
    <範例2>
    使用者提問：
    請幫我深度分析這個檔案內容，根據新的伺服器架構，產出一個架構圖
    回應：
    {分析的內容文字}
    我為你製作了一個架構圖，請看這個網址：
    [{mermaid_diagram_title}] ({mermaid_diagram_url})
    </範例2>
</使用工具 (tools) 需注意的事項>
    """

en_system_prompt = """
    Please follow these guidelines when responding. You must adhere to both the <Tool Usage Guidelines> and <Response Guidelines>.
<Response Guidelines>
- If a tool's documentation instructs you to call another tool, always call it directly rather than asking the user to do so.
- If the user's question specifies a date and time, don't assume whether it's in the future or past. Always use the current_date_time and compare_date_time tools first to determine the current date/time and whether the user's specified date/time is in the past or future, then proceed accordingly. When comparing dates, pay attention to the <Time Interpretation Guidelines>.
- When providing URLs to users, ensure they come from tool responses or historical records. Never create URLs yourself.
- If tool A returns a URL that tool B requires as a parameter, use tool A's URL directly without modification.
- When forwarding user queries to tools, note if the original query contains emphatic words like "must," "note," "definitely," "don't," "absolutely," etc. If so, include these emphatic elements in the user_input.
</Response Guidelines>
<Time Interpretation Guidelines>
The return value from current_date_time helps determine whether user queries relate to historical information or future predictions.
This function returns the exact current date and time. For example:
A return of "2023-03-19 13:23 Asia/Taipei" means it's currently March 19, 2023, 1:23 PM Taipei time.
When comparing dates in user queries:
- If a user asks about "March 10, 2023, 23:00 to March 11, 2023, 23:00," this date occurred in the past
- If a user asks about "March 20, 2023, 23:00 to March 21, 2023, 23:00," this date will occur in the future
- If a user asks about "March 10-11, 2023," this date occurred in the past
</Time Interpretation Guidelines>
<Tool Usage Guidelines>
- web_search:
    Use this tool for all general search situations, unless the user explicitly requests "in-depth research," "deep research," "in-depth search," or "deep search."
    
    When using the web_search tool, first check if the preceding system prompt and user query contain the following information:
    - Search language
    - Search website sources
    If they include this information, append it to the end of user_input, noting to prioritize data in these languages or from these websites.

- generate_image: 
    When using the generate_image tool, you must include the image URL in your response.
    Please respond using this format (from @begin img to @end, including the image URL):
    @begin img("{image_url}") @end

- chat_with_pdf:
    The user's question or instruction. If the question contains the following keywords, include these phrases in user_input:
    - "chart," "graph," "visualization": Generate appropriate statistical charts and provide related plotly data
    - "trend," "direction": Generate a line chart and provide related plotly data
    - "compare," "contrast": Generate a bar chart or pie chart and provide related plotly data
    - "distribution," "dispersion": Generate a scatter plot or heat map and provide related plotly data
    - "time series": Generate a timeline chart and provide related plotly data
    - "geographic information": Generate a map and provide related plotly data
    - "multidimensional analysis": Generate a 3D chart or bubble chart and provide related plotly data
    - "flowchart," "flow": Generate a flowchart and provide related mermaid data
    - "architecture diagram," "architecture": Generate a flowchart and provide related mermaid data
    - "relationship diagram," "relationship": Generate a flowchart or ER diagram and provide related mermaid data
    - "sequence diagram," "sequence": Generate a sequence diagram and provide related mermaid data
    - "state diagram," "state": Generate a state diagram and provide related mermaid data
    - "class diagram," "class": Generate a class diagram and provide related mermaid data
    - "Gantt chart," "timeline": Generate a Gantt chart and provide related mermaid data

- create_plotly_chart:
    When using the create_plotly_chart tool, you must include the URL returned by create_plotly_chart in your response.
    Please respond using this format:
    [{plotly_chart_title}] ({plotly_chart_url})
    <Example 1>
    User query:
    Please analyze the content of this PDF and create a chart for me to view
    Response:
    {Analysis text content}
    I've created a chart for you, please view it at this URL:
    [{plotly_chart_title}] ({plotly_chart_url})
    </Example 1>
    <Example 2>
    User query:
    Please deeply analyze this file's content and create an easy-to-understand comparison chart
    Response:
    {Analysis text content}
    I've created a chart for you, please view it at this URL:
    [{plotly_chart_title}] ({plotly_chart_url})
    </Example 2>

- create_mermaid_diagram:
    When using the create_mermaid_diagram tool, you must include the URL returned by create_mermaid_diagram in your response.
    Please respond using this format:
    [{mermaid_diagram_title}] ({mermaid_diagram_url})
    <Example 1>
    User query:
    Please analyze this PDF's content and create an action flowchart based on the meeting resolution
    Response:
    {Analysis text content}
    I've created a flowchart for you, please view it at this URL:
    [{mermaid_diagram_title}] ({mermaid_diagram_url})
    </Example 1>
    <Example 2>
    User query:
    Please deeply analyze this file's content and create an architecture diagram based on the new server architecture
    Response:
    {Analysis text content}
    I've created an architecture diagram for you, please view it at this URL:
    [{mermaid_diagram_title}] ({mermaid_diagram_url})
    </Example 2>
</Tool Usage Guidelines>
    """


def transform_anthropic_incompatible_schema(
    schema_dict: dict,
) -> tuple[dict, bool, str]:
    """
    轉換可能與 Anthropic 不相容的頂層 schema 結構。

    Args:
        schema_dict: 原始 schema 字典。

    Returns:
        tuple: (轉換後的 schema 字典, 是否進行了轉換, 附加到 description 的提示信息)
    """
    if not isinstance(schema_dict, dict):
        return schema_dict, False, ""

    keys_to_check = ["anyOf", "allOf", "oneOf"]
    problematic_key = None
    for key in keys_to_check:
        if key in schema_dict:
            problematic_key = key
            break

    if problematic_key:
        print(f"  發現頂層 '{problematic_key}'，進行轉換...")
        transformed = True
        new_schema = {"type": "object", "properties": {}, "required": []}
        description_notes = f"\n[開發者註記：此工具參數原使用 '{problematic_key}' 結構，已轉換。請依賴參數描述判斷必要輸入。]"

        # 1. 合併 Properties
        # 先加入頂層的 properties (如果存在)
        if "properties" in schema_dict:
            new_schema["properties"].update(copy.deepcopy(schema_dict["properties"]))
        # 再合併來自 problematic_key 內部的 properties
        for sub_schema in schema_dict.get(problematic_key, []):
            if isinstance(sub_schema, dict) and "properties" in sub_schema:
                # 注意：如果不同 sub_schema 有同名 property，後者會覆蓋前者
                new_schema["properties"].update(copy.deepcopy(sub_schema["properties"]))

        # 2. 處理 Required
        top_level_required = set(schema_dict.get("required", []))

        if problematic_key == "allOf":
            # allOf: 合併所有 required
            combined_required = top_level_required
            for sub_schema in schema_dict.get(problematic_key, []):
                if isinstance(sub_schema, dict) and "required" in sub_schema:
                    combined_required.update(sub_schema["required"])
            # 只保留實際存在於合併後 properties 中的 required 欄位
            new_schema["required"] = sorted(
                [req for req in combined_required if req in new_schema["properties"]]
            )
            description_notes += " 所有相關參數均需考慮。]"  # 簡單提示
        elif problematic_key in ["anyOf", "oneOf"]:
            # anyOf/oneOf: 只保留頂層 required，並在描述中說明選擇性
            new_schema["required"] = sorted(
                [req for req in top_level_required if req in new_schema["properties"]]
            )
            # 嘗試生成更具體的提示 (如果 sub_schema 結構簡單)
            options = []
            for sub_schema in schema_dict.get(problematic_key, []):
                if isinstance(sub_schema, dict) and "required" in sub_schema:
                    options.append(f"提供 '{', '.join(sub_schema['required'])}'")
            if options:
                description_notes += (
                    f" 通常需要滿足以下條件之一：{'; 或 '.join(options)}。]"
                )
            else:
                description_notes += " 請注意參數間的選擇關係。]"

        print(
            f"  轉換後 schema: {json.dumps(new_schema, indent=2, ensure_ascii=False)}"
        )
        return new_schema, transformed, description_notes
    else:
        return schema_dict, False, ""


# --- Schema 轉換輔助函數 (從 _get_mcp_tools_async 提取) ---
def _process_mcp_tools_for_anthropic(langchain_tools: List[Any]) -> List[Any]:
    """處理 MCP 工具列表，轉換不相容的 Schema 並記錄日誌"""
    if not langchain_tools:
        logger.info("[_process_mcp_tools_for_anthropic] 警告 - 未找到任何工具。")
        return []

    logger.info(
        f"[_process_mcp_tools_for_anthropic] --- 開始處理 {len(langchain_tools)} 個原始 MCP 工具 ---"
    )

    processed_tools = []
    for mcp_tool in langchain_tools:
        # 只處理 StructuredTool 或類似的有 args_schema 的工具
        if not hasattr(mcp_tool, "args_schema") or not mcp_tool.args_schema:
            logger.debug(
                f"[_process_mcp_tools_for_anthropic] 工具 '{mcp_tool.name}' 沒有 args_schema，直接加入。"
            )
            processed_tools.append(mcp_tool)
            continue

        original_schema_dict = {}
        try:
            # 嘗試獲取 schema 字典 (根據 Pydantic 版本可能不同)
            if hasattr(mcp_tool.args_schema, "model_json_schema"):  # Pydantic V2
                original_schema_dict = mcp_tool.args_schema.model_json_schema()
            elif hasattr(mcp_tool.args_schema, "schema"):  # Pydantic V1
                original_schema_dict = mcp_tool.args_schema.schema()
            elif isinstance(mcp_tool.args_schema, dict):  # 已經是字典？
                original_schema_dict = mcp_tool.args_schema
            else:
                logger.warning(
                    f"[_process_mcp_tools_for_anthropic] 無法獲取工具 '{mcp_tool.name}' 的 schema 字典 ({type(mcp_tool.args_schema)})，跳過轉換。"
                )
                processed_tools.append(mcp_tool)
                continue

            # 進行轉換檢查
            logger.debug(
                f"[_process_mcp_tools_for_anthropic] 檢查工具 '{mcp_tool.name}' 的 schema..."
            )
            new_schema_dict, transformed, desc_notes = (
                transform_anthropic_incompatible_schema(
                    copy.deepcopy(original_schema_dict)  # 使用深拷貝操作
                )
            )

            if transformed:
                mcp_tool.description += desc_notes
                logger.info(
                    f"[_process_mcp_tools_for_anthropic] 工具 '{mcp_tool.name}' 的描述已更新。"
                )
                if isinstance(mcp_tool.args_schema, dict):
                    logger.debug(
                        f"[_process_mcp_tools_for_anthropic] args_schema 是字典，直接替換工具 '{mcp_tool.name}' 的 schema。"
                    )
                    mcp_tool.args_schema = new_schema_dict
                else:
                    # 如果 args_schema 是 Pydantic 模型，直接修改可能無效或困難
                    # 附加轉換後的字典可能是一種備選方案，但 Langchain/LangGraph 可能不直接使用它
                    # 最好的方法是確保 get_tools 返回的工具的 args_schema 可以被修改，
                    # 或者在創建工具時就使用轉換後的 schema。
                    # 如果不能直接修改，附加屬性是一種標記方式，但可能需要在工具調用處處理。
                    logger.warning(
                        f"[_process_mcp_tools_for_anthropic] args_schema 不是字典 ({type(mcp_tool.args_schema)})，僅添加 _transformed_args_schema_dict 屬性到工具 '{mcp_tool.name}'。這可能不足以解決根本問題。"
                    )
                    setattr(mcp_tool, "_transformed_args_schema_dict", new_schema_dict)
            processed_tools.append(mcp_tool)

        except Exception as e_schema:
            logger.error(
                f"[_process_mcp_tools_for_anthropic] 處理工具 '{mcp_tool.name}' schema 時發生錯誤: {e_schema}",
                exc_info=True,
            )
            processed_tools.append(mcp_tool)  # 保留原始工具

    logger.info(
        f"[_process_mcp_tools_for_anthropic] --- 完成工具處理，返回 {len(processed_tools)} 個工具 ---"
    )
    return processed_tools


async def create_react_agent_graph(
    system_prompt: str = "",
    botrun_flow_lang_url: str = "",
    user_id: str = "",
    model_name: str = "",
    lang: str = LANG_EN,
    mcp_client: Optional[MultiServerMCPClient] = None,  # <--- 接收客戶端實例
):
    """
    Create a react agent graph with optional system prompt

    Args:
        system_prompt: The system prompt to use for the agent
        botrun_flow_lang_url: URL for botrun flow lang
        user_id: User ID
        model_name: Model name to use
        lang: Language code (e.g., "en", "zh-TW")
        mcp_config: MCP servers config
    """

    tools = [
        # 使用特定語言的工具
        CurrentDateTimeTool.for_language(lang),
        WebSearchTool.for_language(lang),
        compare_date_time,
        scrape,
    ]
    if botrun_flow_lang_url and user_id:
        # DICT_VAR["botrun_flow_lang_url"] = botrun_flow_lang_url
        # DICT_VAR["user_id"] = user_id
        tools.append(chat_with_pdf)
        tools.append(chat_with_imgs)
        tools.append(generate_image)
        tools.append(generate_tmp_public_url)
        tools.append(create_html_page)
        tools.append(MermaidDiagramTool.for_language(lang))
        tools.append(PlotlyChartTool.for_language(lang))
        # print("tools============>", tools)

    mcp_tools = []
    if mcp_client:
        logger.info("偵測到活動的 MCP Client，嘗試獲取 MCP 工具...")
        try:
            # 直接使用活動的 client 獲取工具
            raw_mcp_tools = mcp_client.get_tools()  # 假設這是同步或異步方法
            # 如果 get_tools 是異步的: raw_mcp_tools = await mcp_client.get_tools()

            if raw_mcp_tools:
                logger.info(f"從 MCP Client 獲取了 {len(raw_mcp_tools)} 個原始工具。")
                # 處理 Schema (使用提取的輔助函數)
                mcp_tools = _process_mcp_tools_for_anthropic(raw_mcp_tools)
                if mcp_tools:
                    tools.extend(mcp_tools)
                    logger.info(f"已加入 {len(mcp_tools)} 個處理後的 MCP 工具。")
                    logger.debug(
                        f"加入的 MCP 工具名稱: {[tool.name for tool in mcp_tools]}"
                    )
                else:
                    logger.warning("MCP 工具處理後列表為空。")
            else:
                logger.info("MCP Client 返回了空的工具列表。")

        except Exception as e_get:
            logger.error(
                f"從 MCP Client 獲取或處理工具時發生錯誤: {e_get}", exc_info=True
            )
            # 即使出錯，也可能希望繼續執行（不帶 MCP 工具）
    else:
        logger.info("未提供 MCP Client，跳過 MCP 工具。")

    lang_specific_prompt = (
        zh_tw_system_prompt if lang == LANG_ZH_TW else en_system_prompt
    )
    new_system_prompt = system_prompt + "\n\n" + lang_specific_prompt

    system_message = SystemMessage(
        content=[
            {
                "text": new_system_prompt,
                "type": "text",
                "cache_control": {"type": "ephemeral"},
            }
        ]
    )

    # 目前先使用了 https://docs.anthropic.com/en/docs/build-with-claude/tool-use/token-efficient-tool-use
    # 這一段會遇到
    #       File "/Users/seba/Projects/botrun_flow_lang/.venv/lib/python3.11/site-packages/langgraph/prebuilt/tool_node.py", line 218, in __init__
    #     tool_ = create_tool(tool_)
    #             ^^^^^^^^^^^^^^^^^^
    #   File "/Users/seba/Projects/botrun_flow_lang/.venv/lib/python3.11/site-packages/langchain_core/tools/convert.py", line 334, in tool
    #     raise ValueError(msg)
    # ValueError: The first argument must be a string or a callable with a __name__ for tool decorator. Got <class 'dict'>
    # 所以先不使用這一段，這一段是參考 https://python.langchain.com/docs/integrations/chat/anthropic/#tools
    # 也許未來可以引用
    # if get_react_agent_model_name(model_name).startswith("claude-"):
    #     new_tools = []
    #     for tool in tools:
    #         new_tool = convert_to_anthropic_tool(tool)
    #         new_tool["cache_control"] = {"type": "ephemeral"}
    #         new_tools.append(new_tool)
    #     tools = new_tools
    env_name = os.getenv("ENV_NAME", "botrun-flow-lang-dev")
    return create_react_agent(
        get_react_agent_model(model_name),
        tools=tools,
        prompt=system_message,
        # checkpointer=MemorySaver(),
        checkpointer=AsyncFirestoreCheckpointer(env_name=env_name),
    )


# Default graph instance with empty prompt
if False:
    graph = create_react_agent_graph()
# LangGraph Studio 測試用，把以下 un-comment 就可以測試
# graph = create_react_agent_graph(
#     system_prompt="",
#     botrun_flow_lang_url="https://botrun-flow-lang-fastapi-dev-36186877499.asia-east1.run.app",
#     user_id="sebastian.hsu@gmail.com",
# )
