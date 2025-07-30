from langchain_core.language_models import BaseChatModel
from langgraph.constants import END, START
from langgraph.graph import StateGraph

from agentic_kit_flow.pattern.component.executor.sequence_executor import SequenceExecutor
from agentic_kit_flow.pattern.component.planner import SequenceCotPlanner
from agentic_kit_flow.pattern.component.resolver import SummaryResolver
from .base import ReWooGraphBase
from .schema import ReWooState


class CotReWooGraph(ReWooGraphBase):
    def _init_graph(self):
        """初始化graph： CompiledStateGraph"""
        graph_builder = StateGraph(ReWooState)
        graph_builder.add_node('planer', self.planner.invoke)
        graph_builder.add_node('executor', self.executor.invoke)
        graph_builder.add_node('resolver', self.resolver.invoke)
        graph_builder.add_edge('planer', 'executor')
        graph_builder.add_edge('executor', 'resolver')
        graph_builder.add_edge('resolver', END)
        graph_builder.add_edge(START, 'planer')
        self.graph = graph_builder.compile()

    @classmethod
    def create(cls, llm: BaseChatModel, **kwargs):
        tools = kwargs.get('tools', [])
        assert tools is not None
        assert len(tools) > 0

        planner = SequenceCotPlanner.create(llm=llm, tools=tools)
        executor = SequenceExecutor.create(llm=llm, tools=tools)
        resolver = SummaryResolver.create(llm=llm, tools=tools)

        rewoo = cls(llm=llm, planner=planner, executor=executor, resolver=resolver, **kwargs)
        return rewoo
