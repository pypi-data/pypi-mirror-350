from abc import ABC

from agentic_kit_core.base.component import InvokeComponentLLmPromptBase
from agentic_kit_core.utils.prompt import check_prompt_required_filed
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from tenacity import retry, stop_after_attempt

from .parser import PlanParserBase
from .schema import PlannerCotState


def planner_retry_failed_callback(retry_state):
    print('planner_retry_failed_callback: %s' % retry_state)
    return {'steps': [], 'plans': ''}


class PlannerBase(InvokeComponentLLmPromptBase, ABC):
    """plan生成的基类"""

    default_prompt: str = ''

    prompt_required_field: list[str]

    plan_parser: PlanParserBase

    def __init__(
        self,
        llm: BaseChatModel,
        prompt_template: ChatPromptTemplate,
        plan_parser: PlanParserBase = None,
        **kwargs
    ):
        super().__init__(llm=llm, prompt_template=prompt_template, **kwargs)
        self.plan_parser = plan_parser

    @classmethod
    def create(cls, llm: BaseChatModel, plan_parser: PlanParserBase = None, **kwargs):
        # note: 处理prompt
        prompt = kwargs.get('prompt', cls.default_prompt)
        # note: prompt中必须包含的字段
        assert check_prompt_required_filed(prompt=prompt, required_field=cls.prompt_required_field) is True

        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system", prompt
                )
            ]
        )
        planner = cls(llm=llm, prompt_template=prompt_template, plan_parser=plan_parser, **kwargs)
        return planner

    @retry(stop=stop_after_attempt(3), retry_error_callback=planner_retry_failed_callback)
    def invoke(self, state: PlannerCotState):
        print(f'########## CotPlanner 开始执行分析 [{state["task"]}] ##########')

        _input = {}
        for required_field in self.prompt_required_field:
            if required_field not in state:
                raise Exception(f'Missing {required_field} field: {state} should contain {self.prompt_required_field}')
            _input[required_field] = state[required_field]

        print(f'########## CotPlanner 开始执行分析 ##########')
        response = self.llm_callable.invoke(_input)

        if self.plan_parser:
            plans = response.content
            steps = self.plan_parser.parse(content=plans)
            if len(steps) == 0:
                # note: for retry
                raise Exception('empty plans, retry')
            for item in steps:
                print(item.model_dump_json())
            print('########## CotPlanner 执行完毕，已生成详细step ##########\n\n\n')
        else:
            plans = response.content
            steps = plans

        return {
            'result': response,
            'steps': steps,
            'plans': plans,
            **_input
        }
