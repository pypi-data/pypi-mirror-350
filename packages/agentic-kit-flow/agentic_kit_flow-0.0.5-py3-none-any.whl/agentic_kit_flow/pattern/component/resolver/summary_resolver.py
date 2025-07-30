from agentic_kit_core.utils.prompt import check_prompt_required_filed
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from .base import ResolverBase
from .schema import ResolverState

default_simple_resolver_prompt = '''
# 原始总任务是：
{task}


# 执行计划：为了解决这个问题，我们制定了逐步执行计划和检索每个计划的响应。谨慎使用它们，因为长时间的证据可能会包含不相关的信息。
{steps}

# 执行过程：逐步执行的过程和结果如下
{step_results}

# 要求：
1. 现在根据<原始任务>，<执行计划>，<执行过程>，汇总最终执行结果.
2. 用答案回应直接，没有额外的单词。
3. 仅使用以上信息生成最终响应，你不应生成任何额外的结果。
'''


class SummaryResolver(ResolverBase):
    """总结聚合 resolver"""
    def invoke(self, state: ResolverState):
        print('########## SumResolver 开始执行 ##########')
        assert len(state['steps']) > 0
        assert len(state['step_results']) > 0

        result = self.llm_callable.invoke({
            'task': state['task'],
            'steps': '\n'.join([item.plan for item in state['steps']]),
            'step_results': '\n'.join(state['step_results'])
        })
        print(f'''########## [{state['task']}] 得到最终结果是: [{result.content}] ##########''')
        print('########## SumResolver 执行完毕 ##########\n\n\n')
        return {'final_result': result.content}

    @classmethod
    def create(cls, llm: BaseChatModel, **kwargs):
        prompt = kwargs.get('prompt', default_simple_resolver_prompt)
        assert prompt is not None
        # note: prompt中必须包含的字段
        assert check_prompt_required_filed(prompt=prompt, required_field=['{task}', '{steps}', '{step_results}']) is True

        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system", prompt
                )
            ]
        )
        resolver = cls(llm=llm, prompt_template=prompt_template, **kwargs)
        return resolver
