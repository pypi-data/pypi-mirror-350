from agentic_kit_core.base.component import InvokeComponentLlmToolsBase
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from tenacity import retry, stop_after_attempt
from typing_extensions import List

from .schema import ToolCallState
from ..utils import do_tool_call, async_do_tool_call


def _tool_call_retry_failed_callback(retry_state):
    print('_tool_call_retry_failed_callback: %s' % retry_state)
    return {'is_success': False, 'tool_call_response': []}


class ToolCallComponent(InvokeComponentLlmToolsBase):
    """tool call基础组件"""

    @retry(stop=stop_after_attempt(3), retry_error_callback=_tool_call_retry_failed_callback)
    def invoke(self, state: ToolCallState):
        is_success, tool_call_response = do_tool_call(ai_message=state['tool_call_message'], tools=self.tools)
        return is_success, tool_call_response

    @retry(stop=stop_after_attempt(3), retry_error_callback=_tool_call_retry_failed_callback)
    async def ainvoke(self, state: ToolCallState):
        is_success, tool_call_response = await async_do_tool_call(ai_message=state['tool_call_message'], tools=self.tools)
        return is_success, tool_call_response

    @classmethod
    def create(cls, llm: BaseChatModel, tools: List[BaseTool], **kwargs):
        component = cls(llm=llm, tools=tools, **kwargs)
        return component
