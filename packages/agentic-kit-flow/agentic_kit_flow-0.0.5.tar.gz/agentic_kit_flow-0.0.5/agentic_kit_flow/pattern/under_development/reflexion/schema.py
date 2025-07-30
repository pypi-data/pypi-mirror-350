from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, Field
from typing_extensions import Sequence, Annotated

from core.base.schema import BaseState


class ReflexionState(BaseState):
    '''The state of the refection component graph.'''

    messages: Annotated[Sequence[BaseMessage], add_messages]

    loop_counter: int = 3

    responder_attempt: int = 3


class ReflexionCritique(BaseModel):
    """reflection需要包含的信息，缺失或多余的信息"""
    missing: str = Field(description="Critique of what is missing.")
    superfluous: str = Field(description="Critique of what is superfluous")


class AnswerQuestion(BaseModel):
    """Answer the question. Provide an answer, reflection, and then follow up with search queries to improve the answer."""
    answer: str = Field(description="~250 word detailed answer to the question.")
    reflexion_critique: ReflexionCritique = Field(description="Your reflection on the initial answer.")
    search_queries: list[str] = Field(
        description="1-3 search queries for researching improvements to address the critique of your current answer."
    )


# Extend the initial answer schema to include references.
# Forcing citation in the model encourages grounded responses
class ReviseAnswer(AnswerQuestion):
    """Revise your original answer to your question. Provide an answer, reflection,

    cite your reflection with references, and finally
    add search queries to improve the answer."""

    references: list[str] = Field(
        description="Citations motivating your updated answer."
    )
