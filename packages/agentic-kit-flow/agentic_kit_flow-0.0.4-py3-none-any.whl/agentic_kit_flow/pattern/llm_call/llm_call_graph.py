from typing import Literal

from agentic_kit_core.base.graph import PatternSingleLlmGraphBase
from agentic_kit_core.utils.prompt import check_prompt_required_filed
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langgraph.constants import END
from langgraph.graph import StateGraph
from tenacity import retry, stop_after_attempt

from .schema import LlmCallState


def llm_call_retry_failed_callback(retry_state):
    """return the result of the last call attempt"""
    print('---llm_call_retry_failed_callback: %s' % retry_state)
    return { 'results': [], 'messages': [], 'should_finish': True, 'loop_counter': 0 }


class LlmCallGraphBase(PatternSingleLlmGraphBase):
    default_prompt = '''
    # 要求：
    1. 不需要推理过程，请使用最简洁的内容返回最终答案。
    
    # 前置信息：
    {ex_info}
    
    # 请回答：
    {task}
    '''

    required_field = ['{task}', '{ex_info}']

    default_loop_counter = 1

    state_cls = LlmCallState

    def __init__(self, llm: BaseChatModel, prompt_template: ChatPromptTemplate, **kwargs):
        super().__init__(llm=llm, prompt_template=prompt_template, **kwargs)

        self._init_graph()

    def _should_continue(self, state: LlmCallState) -> Literal['llm_call', END]:
        if state.get('should_finish', False) or state.get('loop_counter', self.default_loop_counter) <= 0:
            return END
        else:
            return 'llm_call'

    def _init_graph(self):
        """初始化graph： CompiledStateGraph"""
        builder = StateGraph(self.state_cls)
        builder.add_node('llm_call', self._llm_call)
        builder.add_conditional_edges('llm_call', self._should_continue)
        builder.set_entry_point('llm_call')
        self.graph = builder.compile()

    @retry(stop=stop_after_attempt(3), retry_error_callback=llm_call_retry_failed_callback)
    def _llm_call(self, state: LlmCallState):
        print('########## LlmCallSingleTaskGraph 开始执行 ##########')
        ex_info = state.get('ex_info', '')
        task = state['task']
        print('上一步执行结果是: [%s]' % ex_info)
        print('执行task是: [%s]' % task)

        response = self.llm_callable.invoke({
            'ex_info': ex_info,
            'task': task,
        })
        print(response)
        print('########## LlmCallSingleTaskGraph 结束执行 ##########')
        loop_counter = state.get('loop_counter', self.default_loop_counter) - 1
        return {'results': [response.content], 'messages': [response], 'ex_info': f'{ex_info}\n{response.content}', 'loop_counter': loop_counter}

    @classmethod
    def create(cls, llm: BaseChatModel, **kwargs):
        prompt = kwargs.get('prompt', cls.default_prompt)
        assert check_prompt_required_filed(prompt=prompt, required_field=cls.required_field) is True
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system", kwargs.get('prompt', prompt)
                )
            ]
        )

        agent = cls(llm=llm, prompt_template=prompt_template, **kwargs)
        return agent
