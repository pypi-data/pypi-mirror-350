from abc import ABC, abstractmethod

from langchain_core.language_models import BaseChatModel


class SupervisorBase(ABC):
    prompt: str = None
    '''调用者需要自己定义路由提示词'''

    @classmethod
    def make_supervisor_node(cls, llm: BaseChatModel, router_desc: str, options: list[dict], **kwargs) -> str:
        """
        给某一些子任务创建一个supervisor node
        :param llm:
        :param router_desc: supervisor node的一些附加描述
        :param options: 可以路由的option list，每个option包括option名字和一些描述，结构是{'name': 'xxxx', 'desc': '功能描述'}
        :return:
        """
        return cls._make_supervisor_node(llm=llm, router_desc=router_desc, options=options, **kwargs)

    @classmethod
    @abstractmethod
    def _make_supervisor_node(cls, llm: BaseChatModel, router_desc: str, options: list[dict], **kwargs):
        raise NotImplemented
