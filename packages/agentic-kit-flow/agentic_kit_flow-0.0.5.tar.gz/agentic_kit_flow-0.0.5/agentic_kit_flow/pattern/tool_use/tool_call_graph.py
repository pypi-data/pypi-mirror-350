from abc import ABC

from agentic_kit_core.base.graph import PatternToolGraphBase
from agentic_kit_core.utils.prompt import check_prompt_required_filed
from agentic_kit_core.utils.tools import get_tools_desc_for_prompt_zh
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END
from langgraph.graph import StateGraph
from tenacity import retry, stop_after_attempt
from typing_extensions import List

from .schema import ToolCallState
from ..component.tool_call.tool_call_component import ToolCallComponent

default_prompt = \
'''
# 你是一个工具tool调用助手，通过给出的工具tool调用提示，来调用对应的用具。
# 调用提示中可能包含一些前置信息或其他工具tool的调用结果，在类似<#E>这样的字段中，表示前置信息或其他工具tool的调用结果。

## 前置信息或其他工具tool的调用结果是：{ex_info}

# 当前的工具tool调用任务是: {task}，
可供调用的工具tool和详细参数结构、描述，分别是：{tools},

# 生成规则：
1.请使用正确的参数调用工具tool，严格遵守匹配工具tool的参数类型，
2.可以选择1个或多个适合的工具tool来完成任务
3.如果没有合适的工具tool，就不要返回任何信息
4.请忽略上次调用的任何信息，重新生成回答
'''


def _tool_call_retry_failed_callback(retry_state):
    """return the result of the last call attempt"""
    print('---tool_call_retry_failed: %s' % retry_state)
    return {'results': [], 'call_log': []}


class ToolCallGraphBase(PatternToolGraphBase, ABC):
    def __init__(self, llm: BaseChatModel, tools: List, prompt_template: ChatPromptTemplate, is_async=False, **kwargs):
        print('ToolCallGraphBase.__init__: %s' % kwargs)
        super().__init__(llm=llm, tools=tools, prompt_template=prompt_template, **kwargs)

        self._init_graph(is_async)

    def _init_graph(self, is_async=False):
        """初始化graph： CompiledStateGraph"""
        checkpointer = MemorySaver()
        builder = StateGraph(ToolCallState)
        builder.add_node('tool_call', self.ainvoke if is_async else self.invoke)
        builder.add_edge('tool_call', END)
        builder.set_entry_point('tool_call')
        self.graph = builder.compile(checkpointer=checkpointer)

    @classmethod
    def create(cls, llm: BaseChatModel, tools: List[BaseTool], is_async=False, **kwargs):
        prompt = kwargs.get('prompt', default_prompt)
        assert check_prompt_required_filed(prompt=prompt, required_field=['{ex_info}', '{task}', '{tools}']) is True
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system", kwargs.get('prompt', prompt)
                )
            ]
        )

        agent = cls(llm=llm, tools=tools, prompt_template=prompt_template, is_async=is_async, **kwargs)
        return agent


class ToolCallSingleTaskGraph(ToolCallGraphBase):
    """single task tool call agent"""

    @retry(stop=stop_after_attempt(3), retry_error_callback=_tool_call_retry_failed_callback)
    def invoke(self, state: ToolCallState):
        print('########## ToolCallSingleTaskGraph 开始执行调用tools invoke ##########')
        tools_desc = get_tools_desc_for_prompt_zh(self.tools)
        ex_info = state.get('ex_info', '')
        task = state['task']
        print('上一步执行结果是: [%s]' % ex_info)
        print('执行task是: [%s]' % task)
        print('可供调用的是: %s' % tools_desc)

        response = self.llm_callable_with_tools.invoke({
            'ex_info': ex_info,
            'task': task,
            'tools': tools_desc,
        })
        print(response)

        component = ToolCallComponent.create(llm=self.llm, tools=self.tools)
        is_success, tool_call_response = component.invoke({'tool_call_message': response})

        if is_success is False:
            # note: exception for retry
            raise Exception('retry')
        results =  [item[1] for item in tool_call_response]
        return {'results': results, 'call_log': [response, *results]}

    @retry(stop=stop_after_attempt(3), retry_error_callback=_tool_call_retry_failed_callback)
    async def ainvoke(self, state: ToolCallState):
        print('########## ToolCallSingleTaskGraph 开始执行调用tools ainvoke ##########')
        tools_desc = get_tools_desc_for_prompt_zh(self.tools)
        ex_info = state.get('ex_info', '')
        task = state['task']
        print('上一步执行结果是: [%s]' % ex_info)
        print('执行task是: [%s]' % task)
        print('可供调用的是: %s' % tools_desc)

        response = self.llm_callable_with_tools.invoke({
            'ex_info': ex_info,
            'task': task,
            'tools': tools_desc,
        })
        print(response)

        component = ToolCallComponent.create(llm=self.llm, tools=self.tools)
        is_success, tool_call_response = await component.ainvoke({'tool_call_message': response})

        if is_success is False:
            # note: exception for retry
            raise Exception('retry')
        results = [item[1] for item in tool_call_response]
        return {'results': results, 'call_log': [response, *results]}


# class ToolCallMultiTasksGraph(ToolCallSingleTaskGraph):
#     """multi task tool call agent"""
#
#     @retry(stop=stop_after_attempt(3), retry_error_callback=_tool_call_retry_failed_callback)
#     def invoke(self, state: ToolCallState):
#         print('########## ToolCallMultiTasksGraph 开始执行调用tools ##########')
#         tools_desc = get_tools_desc_for_prompt_zh(self.tools)
#         ex_info = state.get('ex_info', '')
#         tasks = state['task']
#         print('上一步执行结果是: [%s]' % ex_info)
#         print('执行tasks是: [%s]' % tasks)
#         print('可供调用的是: %s' % tools_desc)
#
#         results = []
#         call_log = []
#
#         for task in tasks:
#             ai_response = self.llm_callable_with_tools.invoke({
#                 'ex_info': ex_info,
#                 'task': task,
#                 'tool': tools_desc,
#             })
#             print(ai_response)
#
#             is_success, tool_call_response = do_tool_call(ai_message=ai_response, tools=self.tools)
#             if is_success is False:
#                 # note: exception for retry
#                 raise Exception('retry')
#             _results =  [item[1] for item in tool_call_response]
#             results.extend(_results)
#             call_log.append(ai_response)
#             call_log.extend(_results)
#
#         return {'results': results, 'call_log': call_log}
