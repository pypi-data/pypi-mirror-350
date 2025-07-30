from abc import abstractmethod

from agentic_kit_core.base.component import InvokeComponentBase
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import ToolMessage, ToolCall
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from typing_extensions import List

from .schema import PlanModel, ExecutorStateBase


class ExecutorBase(InvokeComponentBase):

    def __init__(
        self,
        llm: BaseChatModel,
        tools: List[BaseTool],
        prompt_template: ChatPromptTemplate,
        **kwargs
    ):
        super().__init__(llm=llm, tools=tools, prompt_template=prompt_template, **kwargs)

    @abstractmethod
    def invoke(self, state: ExecutorStateBase):
        raise NotImplemented

    @classmethod
    def get_step_result(cls, step: PlanModel, tool_call_response: list[(ToolCall, ToolMessage)]):
        """获取单步结果格式化字符串"""
        _pure_results = [item[1].content for item in tool_call_response]
        joined_results = '\n'.join(_pure_results)
        step_result = fr'''{step.step_name}:{step.plan}。得到的结果是：[{joined_results}]。结果变量{step.result_name}赋值为{joined_results}'''
        return step_result


def executor_retry_failed_callback(retry_state):
    print('executor_retry_failed_callback: %s' % retry_state)
    return {'results': [], 'call_log': []}
