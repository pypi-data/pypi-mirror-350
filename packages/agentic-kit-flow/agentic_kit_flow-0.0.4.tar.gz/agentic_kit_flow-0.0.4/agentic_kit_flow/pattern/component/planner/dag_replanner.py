from typing import List

from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool

from .base import PlannerBase
from .schema import RePlannerCotState


class DagRePlanner(PlannerBase):
    """生成dag结构的计划，有向无环图"""

    def invoke(self, state: RePlannerCotState):
        pass

    @classmethod
    def create(cls, llm: BaseChatModel, tools: List[BaseTool], **kwargs):
        pass

    # TODO

