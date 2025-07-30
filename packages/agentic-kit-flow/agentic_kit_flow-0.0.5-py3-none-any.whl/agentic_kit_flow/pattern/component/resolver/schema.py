from typing import Union

from agentic_kit_core.base.schema import BaseState

from ...schema import PlanModel


class ResolverState(BaseState):
    task: Union[str, list[str]]

    steps: list[PlanModel]

    step_results: list[str]

    final_result: str
