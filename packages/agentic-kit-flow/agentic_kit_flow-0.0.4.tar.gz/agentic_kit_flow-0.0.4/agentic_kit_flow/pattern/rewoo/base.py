from abc import ABC, abstractmethod

from agentic_kit_core.base.graph import PatternGraphBase

from agentic_kit_flow.pattern.component.executor import ExecutorBase
from agentic_kit_flow.pattern.component.planner import PlannerWithParserBase
from agentic_kit_flow.pattern.component.resolver import ResolverBase


class ReWooGraphBase(PatternGraphBase, ABC):
    planner: PlannerWithParserBase

    executor: ExecutorBase

    resolver: ResolverBase

    def __init__(self,
                 planner: PlannerWithParserBase,
                 executor: ExecutorBase,
                 resolver: ResolverBase,
                 **kwargs
                 ):
        assert planner is not None
        assert executor is not None
        assert resolver is not None

        super().__init__(**kwargs)

        self.planner = planner
        self.executor = executor
        self.resolver = resolver

        self._init_graph()

    @abstractmethod
    def _init_graph(self):
        raise NotImplemented
