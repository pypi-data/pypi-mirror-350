from agentic_kit_core.utils.prompt import check_prompt_required_filed
from agentic_kit_core.utils.tools import find_tool_by_name
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from tenacity import retry, stop_after_attempt
from typing_extensions import List

from .base import ExecutorBase, executor_retry_failed_callback
from .schema import StepExecutorState
from ..utils.tool_call import do_tool_call

default_step_executor_prompt = \
'''
# 你是一个工具tool调用助手，通过给出的工具tool调用提示，来调用对应的用具。
# 调用提示中可能包含一些前置信息或其他工具tool的调用结果，在类似<#E>这样的字段中，表示前置信息或其他工具tool的调用结果。

# 前置信息是：
{ex_info}

# 当前的工具tool调用任务是: 
{task}，

# 工具tool的信息如下：
1. 调用的工具tool的名称是：{tool_name}，
2. 工具tool具体功能描述是{tool_desc},
3. 工具tool参数是：{tool_args}
4. 步骤序号是: {step_name},

# 要求：
1. 请使用正确的参数调用tool
'''


class StepExecutor(ExecutorBase):
    """单步执行"""

    @retry(stop=stop_after_attempt(3), retry_error_callback=executor_retry_failed_callback)
    def invoke(self, state: StepExecutorState):
        print('########## StepExecutor 开始执行调用tools ##########')
        ex_info = state.get('ex_info', '')
        step = state['step']
        print('前置信息是: [%s]' % ex_info)

        tool = find_tool_by_name(tool_name=step.tool_name, tools=self.tools)
        print(f'执行{step.step_name}:{step.plan} [{step.is_last_step}]')
        if tool:
            ai_response = self.llm_callable_with_tools.invoke({
                'ex_info': ex_info,
                'task': step.plan,
                'tool_name': step.tool_name,
                'tool_args': step.tool_args,
                'step_name': step.step_name,
                'tool_desc': tool.description,
            })
            # print(ai_response)

            is_success, tool_call_response = do_tool_call(ai_message=ai_response, tools=self.tools)
            if is_success is False:
                # note: exception for retry
                raise Exception('retry')

            result = [item[1] for item in tool_call_response]
            step_result = self.get_step_result(step=step, tool_call_response=tool_call_response)

            print('########## StepExecutor 执行完毕 ##########\n\n\n')
            return {
                'result': result,
                'call_log': [ai_response, result],
                'step_result': step_result,
            }
        else:
            # note:  不需要tool调用
            print('########## StepExecutor 执行完毕 ##########\n\n\n')
            return {
                'result': step.plan,
                'call_log': [step.plan],
                'step_result': step.plan,
            }

    @classmethod
    def create(cls, llm: BaseChatModel, tools: List[BaseTool], **kwargs):
        prompt = kwargs.get('prompt', default_step_executor_prompt)
        assert prompt is not None
        # note: prompt中必须包含的字段
        assert check_prompt_required_filed(prompt=prompt,
                                           required_field=['{task}', '{tool_name}', '{tool_desc}', '{tool_args}',
                                                           '{step_name}', '{ex_info}']) is True

        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system", prompt
                )
            ]
        )
        executor = cls(llm=llm, prompt_template=prompt_template, tools=tools, **kwargs)
        return executor
