from agentic_kit_core.base.schema import BaseState
from langchain_core.messages import AIMessage
from typing_extensions import Union

from ...schema import PlanModel


class PlannerStateBase(BaseState):
    task: Union[str, list[str]]
    '''[input]初始任务'''

    result: AIMessage
    '''[output]生成的plan'''


class PlannerWithToolsState(PlannerStateBase):
    tools: str
    '''[input]tool的描述'''


class PlannerCotState(PlannerWithToolsState):
    steps: list[PlanModel]
    '''[output]生成的plan'''

    plans: str
    '''[output]生成的plan'''


class RePlannerCotState(PlannerCotState):
    init_steps: list[PlanModel]
    '''原始任务列表'''

    past_step_results: str
    '''已完成步骤的结果'''
