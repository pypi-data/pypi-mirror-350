from abc import abstractmethod

from agentic_kit_core.base.component import InvokeComponentLLmPromptBase
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from typing_extensions import List

from .schema import ResolverState


class ResolverBase(InvokeComponentLLmPromptBase):
    def __init__(
            self,
            llm: BaseChatModel,
            prompt_template: ChatPromptTemplate,
            **kwargs
    ):
        super().__init__(llm=llm, prompt_template=prompt_template, **kwargs)

    @abstractmethod
    def invoke(self, state: ResolverState):
        raise NotImplemented
