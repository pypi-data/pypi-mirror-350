import operator
from typing import Any

from agentic_kit_core.base.schema import BaseState
from typing_extensions import Annotated

from ..schema import PlanModel


class PlanExecuteState(BaseState):
    task: str
    '''总任务'''

    init_steps: list[PlanModel]
    '''第一次生成后不变'''

    init_step: PlanModel
    '''第一步子任务'''

    final_result: str
    '''最终结果'''

    past_steps: Annotated[list[PlanModel], operator.add]
    '''executor返回的执行过的step'''

    past_step_results: Annotated[list[str], operator.add]
    '''executor返回的执行过的结果，循环递增传递给executor'''

    revised_steps: list[PlanModel]
    '''每次re-plan后，重新生成的steps，当len(revised_steps) == 0时，设置 <should_finish = True>'''

    should_finish: bool
    '''结束flag'''

    call_log: Annotated[list[Any], operator.add]
    '''调用log'''
