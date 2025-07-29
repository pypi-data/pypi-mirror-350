from typing import AsyncGenerator, Dict, List, Optional, Union

from pydantic import BaseModel


class StepsUpdateEvent(BaseModel):
    """
    for step in steps:
        print("Description:", step.get("description", ""))
        print("Status:", step.get("status", ""))
        print("Updates:", step.get("updates", ""))
    """

    steps: List = []


class OnNodeStreamEvent(BaseModel):
    chunk: str


MAX_RECURSION_LIMIT = 25


# graph 是 CompiledStateGraph，不傳入型別的原因是，loading import 需要 0.5秒
async def langgraph_runner(
    thread_id: str,
    init_state: dict,
    graph,
    need_resume: bool = False,
    extra_config: Optional[Dict] = None,
) -> AsyncGenerator:
    invoke_state = init_state
    config = {
        "configurable": {"thread_id": thread_id},
        "recursion_limit": MAX_RECURSION_LIMIT,
    }
    if extra_config:
        config["configurable"].update(extra_config)
    if need_resume:
        state_history = []
        async for state in graph.aget_state_history(config):
            state_history.append(state)

        # 如果 state_history 的長度超過 MAX_RECURSION_LIMIT，動態調整 recursion_limit
        if len(state_history) > MAX_RECURSION_LIMIT:
            # 計算超出的倍數
            multiplier = (len(state_history) - 1) // MAX_RECURSION_LIMIT
            # 設定新的 recursion_limit 為 (multiplier + 1) * MAX_RECURSION_LIMIT
            config["recursion_limit"] = (multiplier + 1) * MAX_RECURSION_LIMIT

    async for event in graph.astream_events(
        invoke_state,
        config,
        version="v2",
    ):
        # state = await graph.aget_state(config)
        # print(state.config)

        yield event


# graph 是 CompiledStateGraph，不傳入型別的原因是，loading import 需要 0.5秒
async def agent_runner(
    thread_id: str,
    init_state: dict,
    graph,
    need_resume: bool = False,
    extra_config: Optional[Dict] = None,
) -> AsyncGenerator[Union[StepsUpdateEvent, OnNodeStreamEvent], None]:
    invoke_state = init_state
    config = {
        "configurable": {"thread_id": thread_id},
        "recursion_limit": MAX_RECURSION_LIMIT,
    }
    if extra_config:
        config["configurable"].update(extra_config)
    if need_resume:
        state_history = []
        async for state in graph.aget_state_history(config):
            state_history.append(state)

        # 如果 state_history 的長度超過 MAX_RECURSION_LIMIT，動態調整 recursion_limit
        if len(state_history) > MAX_RECURSION_LIMIT:
            # 計算超出的倍數
            multiplier = (len(state_history) - 1) // MAX_RECURSION_LIMIT
            # 設定新的 recursion_limit 為 (multiplier + 1) * MAX_RECURSION_LIMIT
            config["recursion_limit"] = (multiplier + 1) * MAX_RECURSION_LIMIT

    async for event in graph.astream_events(
        invoke_state,
        config,
        version="v2",
    ):
        if event["event"] == "on_chain_end":
            pass
            # print(event)
        if event["event"] == "on_chat_model_end":
            pass
            # for step_event in handle_copilotkit_intermediate_state(event):
            #     yield step_event
        if event["event"] == "on_chat_model_stream":
            data = event["data"]
            if (
                data["chunk"].content
                and isinstance(data["chunk"].content[0], dict)
                and data["chunk"].content[0].get("text", "")
            ):
                yield OnNodeStreamEvent(chunk=data["chunk"].content[0].get("text", ""))
            elif data["chunk"].content and isinstance(data["chunk"].content, str):
                yield OnNodeStreamEvent(chunk=data["chunk"].content)


# def handle_copilotkit_intermediate_state(event: dict):
#     print("Handling copilotkit intermediate state")
#     copilotkit_intermediate_state = event["metadata"].get(
#         "copilotkit:emit-intermediate-state"
#     )
#     print(f"Intermediate state: {copilotkit_intermediate_state}")
#     if copilotkit_intermediate_state:
#         for intermediate_state in copilotkit_intermediate_state:
#             if intermediate_state.get("state_key", "") == "steps":
#                 for tool_call in event["data"]["output"].tool_calls:
#                     if tool_call.get("name", "") == intermediate_state.get("tool", ""):
#                         steps = tool_call["args"].get(
#                             intermediate_state.get("tool_argument")
#                         )
#                         print(f"Yielding steps: {steps}")
#                         yield StepsUpdateEvent(steps=steps)
#     print("--------------------------------")
