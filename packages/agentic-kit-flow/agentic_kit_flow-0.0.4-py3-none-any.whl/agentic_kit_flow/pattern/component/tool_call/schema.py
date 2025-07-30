from agentic_kit_core.base.schema import BaseState
from langchain_core.messages import ToolMessage, AIMessage


class ToolCallState(BaseState):
    tool_call_message: AIMessage
    '''[input]llm返回的tool call消息'''

    tool_call_results: list[ToolMessage]
    '''[output]tool call结果列表'''

    is_success: bool
    '''[output]tool call成功标记'''
