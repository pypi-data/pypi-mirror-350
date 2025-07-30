from agentic_kit_core.utils.prompt import check_prompt_required_filed
from agentic_kit_core.utils.tools import find_tool_by_name
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from tenacity import retry, stop_after_attempt
from typing_extensions import List

from .base import ExecutorBase, executor_retry_failed_callback
from .schema import SequenceExecutorState
from ..utils.tool_call import do_tool_call

default_sequence_executor_prompt = \
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


class SequenceExecutor(ExecutorBase):

    @retry(stop=stop_after_attempt(3), retry_error_callback=executor_retry_failed_callback)
    def invoke(self, state: SequenceExecutorState):
        print('########## SequenceExecutor 开始执行调用tools ##########')
        ex_info = state.get('ex_info', '')
        steps = state['steps']
        print('前置信息是: [%s]' % ex_info)

        step_results = []
        results = []
        call_log = []

        for step in steps:
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

                step_result = self.get_step_result(step=step, tool_call_response=tool_call_response)
                step_results.append(step_result)

                ex_info = f'''{ex_info}\n{step_result}'''
                # print(ex_info)

                _results = [item[1] for item in tool_call_response]
                results.extend(_results)

                call_log.append(ai_response)
                call_log.extend(_results)
            else:
                # note: 无tool调用
                step_result = step.plan
                step_results.append(step_result)
                ex_info = f'''{ex_info}\n{step_result}'''
                results.append(step_result)
                call_log.append(step_result)


        print('########## SequenceExecutor 执行完毕 ##########\n\n\n')
        return {'results': results, 'call_log': call_log, 'step_results': step_results}


    @classmethod
    def create(cls, llm: BaseChatModel, tools: List[BaseTool], **kwargs):
        prompt = kwargs.get('prompt', default_sequence_executor_prompt)
        assert prompt is not None
        # note: prompt中必须包含的字段
        assert check_prompt_required_filed(prompt=prompt, required_field=['{task}', '{tool_name}', '{tool_desc}', '{tool_args}', '{step_name}', '{ex_info}']) is True

        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system", prompt
                )
            ]
        )
        executor = cls(llm=llm, prompt_template=prompt_template, tools=tools, **kwargs)
        return executor
