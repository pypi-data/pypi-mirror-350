from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from typing_extensions import Sequence, Annotated

from core.base.schema import BaseState


class ReflectionState(BaseState):
    """The state of the reflection component graph."""

    original_input: str
    """原始输入"""

    revise_list: Annotated[Sequence[BaseMessage], add_messages]

    revised_message: str
    '''经过reflection后的输入，重新提交给llm'''

    revise: str
    '''reflection message, 如果llm不在返回revise，就停止'''

    loop_counter: int
    '''reflection 次数, 达到计数器后就停止'''

    result: str
    '''最终结果'''
