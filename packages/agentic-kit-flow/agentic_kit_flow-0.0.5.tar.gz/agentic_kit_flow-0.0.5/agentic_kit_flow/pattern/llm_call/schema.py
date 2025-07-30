import operator

from agentic_kit_core.base.schema import BaseState
from langchain_core.messages import AnyMessage
from typing_extensions import Union, Annotated


class LlmCallState(BaseState):
    task: Union[str, list[str]]

    ex_info: str

    results: Annotated[list[str], operator.add]

    messages: Annotated[list[AnyMessage], operator.add]

    should_finish: bool

    loop_counter: int
