from agentic_kit_core.base.schema import BaseState
from langchain_core.messages import ToolMessage, AnyMessage

from ...schema import PlanModel


class ExecutorStateBase(BaseState):
    ex_info: str

    call_log: list[AnyMessage]


class SequenceExecutorState(ExecutorStateBase):
    steps: list[PlanModel]

    step_results: list[str]

    results: list[ToolMessage]


class StepExecutorState(ExecutorStateBase):
    step: PlanModel

    step_result: str

    result: ToolMessage
