from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticToolsParser

from .responder import ResponderWithRetries


class Reviser(ResponderWithRetries):

    @classmethod
    def get_reviser(cls, llm: BaseChatModel, actor_prompt_template, tool):
        # note: 指定格式化输出
        actor_prompt_template.append(HumanMessage(content='\n\n<system>Reflect on the user\'s original question and the actions taken thus far. Respond using the {function_name} function.</reminder>'))
        actor_prompt_template = actor_prompt_template.partial(function_name=tool.__name__)

        revision_chain = actor_prompt_template | llm.bind_tools(tools=[tool])

        validator = PydanticToolsParser(tools=[tool])

        reviser = cls(
            runnable=revision_chain, validator=validator
        )

        return reviser
