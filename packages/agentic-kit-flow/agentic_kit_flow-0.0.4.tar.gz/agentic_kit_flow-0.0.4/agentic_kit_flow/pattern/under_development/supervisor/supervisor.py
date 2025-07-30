from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langgraph.constants import END
from langgraph.types import Command
from typing_extensions import TypedDict, Literal

from utils.prompt import generate_system_prompt
from .base import SupervisorBase
from .schema import RouterAction, ROUTER_ACTION_FINISH


def _format_options(options: list[dict]) -> str:
    """格式化输出任务执行者的可选项"""
    options_desc = ''
    counter = 1
    for option in options:
        options_desc += f'\n{counter}.name是:{option.get("name")}，可完成的工作是:{option.get("desc")}'
        counter += 1
    return options_desc


class SupervisorNode(SupervisorBase):
    prompt: str = '''
        # 你是一位负责工作任务分发和监督的主管，你负责分发和监督的任务是：
            {router_desc}，如果超出你的工作范围，直接回复'FINISH'。
            
        # 你负责管理以下员工或者工作节点的任务分发，他们分别是：
            {options_desc}。
            
        # 请根据用户的请求，将用户请求做任务分解，将分解后的子任务分配给适合完成这项任务的员工或者工作节点。以下是要求：
            * 如果找到合适的员工和工作节点，请回复下一个员工的name。
            * 如果员工已经执行完成分配给他的任务，就回复他的结果和状态，并回复'FINISH'。
            * 如果任务的答案已经包含在消息列表中，直接回复'FINISH'。
            * 请你一步一步的分配任务，一个任务执行完以后再调用下一个任务。
            * 这次任务分配仅限于本段内容，忽略之前的任务。
    '''

    @classmethod
    def _make_supervisor_node(cls, llm: BaseChatModel, router_desc: str, options: list[dict], **kwargs):
        members = list(map(lambda option: option.get('name'), options))
        # system_prompt = _get_prompt_template(router_desc=router_desc, options=options)

        def router_node(state: TypedDict) -> Command[Literal[*members, "__end__"]]:
            """An LLM-based supervisor."""
            system_messages = generate_system_prompt(prompt=cls.prompt, router_desc=router_desc, options=options)
            messages = system_messages + state["messages"]

            response = llm.with_structured_output(RouterAction).invoke(messages)
            print(f'RouterManager supervisor node -- 基于以下message中选择了 ---> {response}')
            print('messages如下：')
            print(f'{messages}')
            print('messages -------------- print end')
            goto = response["next"]
            if goto == ROUTER_ACTION_FINISH:
                goto = END

            return Command(goto=goto)

        return router_node
