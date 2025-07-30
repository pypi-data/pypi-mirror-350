import os
from typing import ClassVar, Dict, Optional

from langchain_core.tools import BaseTool
from langchain_core.runnables import RunnableConfig

from botrun_flow_lang.constants import LANG_EN, LANG_ZH_TW
from botrun_flow_lang.langgraph_agents.agents.util.mermaid_util import (
    generate_mermaid_files,
)


class MermaidDiagramTool(BaseTool):
    # Class attributes
    tool_name: ClassVar[str] = "create_mermaid_diagram"

    # Multi-language descriptions
    descriptions: ClassVar[Dict[str, str]] = {
        LANG_EN: """
    Create an interactive Mermaid diagram visualization and return its URL.
    This URL should be provided to the user,
    as they will need to access it to view the interactive diagram in their web browser.

    Scenarios for using create_mermaid_diagram:
    - Need to visualize flowcharts, architecture diagrams, or relationship diagrams
    - Need to show system architecture (flowchart)
    - Need to explain operational processes (flowchart)
    - Need to show sequence interactions (sequence diagram)
    - Need to show state transitions (state diagram)
    - Need to show class relationships (class diagram)
    - Need to show entity relationships (ER diagram)
    - Need to show project timelines (gantt chart)
    - Need to show user journeys (journey)
    - Need to show requirement relationships (requirement diagram)
    - Need to show resource allocation (pie chart)

    Supported Diagram Types:
    1. Flowcharts (graph TD/LR):
       - System architectures
       - Process flows
       - Decision trees
       - Data flows

    2. Sequence Diagrams (sequenceDiagram):
       - API interactions
       - System communications
       - User interactions
       - Message flows

    3. Class Diagrams (classDiagram):
       - Software architecture
       - Object relationships
       - System components
       - Code structure

    4. State Diagrams (stateDiagram-v2):
       - System states
       - Workflow states
       - Process states
       - State transitions

    5. Entity Relationship Diagrams (erDiagram):
       - Database schemas
       - Data relationships
       - System entities
       - Data models

    6. User Journey Diagrams (journey):
       - User experiences
       - Customer flows
       - Process steps
       - Task sequences

    7. Gantt Charts (gantt):
       - Project timelines
       - Task schedules
       - Resource allocation
       - Milestone tracking

    8. Pie Charts (pie):
       - Data distribution
       - Resource allocation
       - Market share
       - Component breakdown

    9. Requirement Diagrams (requirementDiagram):
       - System requirements
       - Dependencies
       - Specifications
       - Constraints

    Example Mermaid syntax for a simple flowchart:
    ```
    graph TD
        A[Start] --> B{Data Available?}
        B -->|Yes| C[Process Data]
        B -->|No| D[Get Data]
        C --> E[End]
        D --> B
    ```

    Args:
        mermaid_data: String containing the Mermaid diagram definition
        title: Optional title for the diagram

    Returns:
        str: URL for the interactive HTML visualization. This URL should be provided to the user,
             as they will need to access it to view the interactive diagram in their web browser.
    """,
        LANG_ZH_TW: """
    Create an interactive Mermaid diagram visualization and return its URL.
    This URL should be provided to the user,
    as they will need to access it to view the interactive diagram in their web browser.

    使用 create_mermaid_diagram 的情境：
    - 提到「流程圖」、「架構圖」、「關係圖」等字眼
    - 需要展示系統架構（flowchart）
    - 需要說明操作流程（flowchart）
    - 需要展示時序互動（sequence diagram）
    - 需要展示狀態轉換（state diagram）
    - 需要展示類別關係（class diagram）
    - 需要展示實體關係（ER diagram）
    - 需要展示專案時程（gantt chart）
    - 需要展示使用者旅程（journey）
    - 需要展示需求關係（requirement diagram）
    - 需要展示資源分配（pie chart）

    Supported Diagram Types:
    1. Flowcharts (graph TD/LR):
       - System architectures
       - Process flows
       - Decision trees
       - Data flows

    2. Sequence Diagrams (sequenceDiagram):
       - API interactions
       - System communications
       - User interactions
       - Message flows

    3. Class Diagrams (classDiagram):
       - Software architecture
       - Object relationships
       - System components
       - Code structure

    4. State Diagrams (stateDiagram-v2):
       - System states
       - Workflow states
       - Process states
       - State transitions

    5. Entity Relationship Diagrams (erDiagram):
       - Database schemas
       - Data relationships
       - System entities
       - Data models

    6. User Journey Diagrams (journey):
       - User experiences
       - Customer flows
       - Process steps
       - Task sequences

    7. Gantt Charts (gantt):
       - Project timelines
       - Task schedules
       - Resource allocation
       - Milestone tracking

    8. Pie Charts (pie):
       - Data distribution
       - Resource allocation
       - Market share
       - Component breakdown

    9. Requirement Diagrams (requirementDiagram):
       - System requirements
       - Dependencies
       - Specifications
       - Constraints

    Example Mermaid syntax for a simple flowchart:
    ```
    graph TD
        A[開始] --> B{是否有資料?}
        B -->|是| C[處理資料]
        B -->|否| D[取得資料]
        C --> E[結束]
        D --> B
    ```

    Args:
        mermaid_data: String containing the Mermaid diagram definition
        title: Optional title for the diagram. If provided, must be in Traditional Chinese.
               For example: "系統流程圖" instead of "System Flowchart"

    Returns:
        str: URL for the interactive HTML visualization. This URL should be provided to the user,
             as they will need to access it to view the interactive diagram in their web browser.
    """,
    }

    # Pydantic model fields
    name: str = "create_mermaid_diagram"
    description: str = descriptions[LANG_EN]

    @classmethod
    def for_language(cls, lang: str = LANG_EN):
        """Create a language-specific instance of the tool"""
        # Get the description for the specified language, or use English as default
        description = cls.descriptions.get(lang, cls.descriptions.get(LANG_EN))
        return cls(name=cls.tool_name, description=description)

    def _run(
        self,
        mermaid_data: str,
        title: Optional[str] = None,
        config: RunnableConfig = None,
    ) -> str:
        """
        Generate a Mermaid diagram and return its URL
        """
        from botrun_flow_lang.utils.botrun_logger import BotrunLogger

        logger = BotrunLogger()
        logger.info(
            f"create_mermaid_diagram mermaid_data: {mermaid_data} title: {title}"
        )
        try:
            html_url = generate_mermaid_files(
                mermaid_data,
                config.get("configurable", {}).get("botrun_flow_lang_url", ""),
                config.get("configurable", {}).get("user_id", ""),
                title,
            )
            logger.info(f"create_mermaid_diagram generated============> {html_url}")
            return html_url
        except Exception as e:
            logger.error(
                f"create_mermaid_diagram error: {e}",
                error=str(e),
                exc_info=True,
            )
            return f"Error creating diagram URL: {str(e)}"
