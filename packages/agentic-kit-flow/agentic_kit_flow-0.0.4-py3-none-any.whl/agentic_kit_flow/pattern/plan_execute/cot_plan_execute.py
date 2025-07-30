from typing import Literal

from langchain_core.language_models import BaseChatModel
from langgraph.constants import END, START
from langgraph.graph import StateGraph

from agentic_kit_flow.pattern.component.executor.step_executor import StepExecutor
from agentic_kit_flow.pattern.component.planner import SequenceCotPlanner, CotRePlanner
from agentic_kit_flow.pattern.component.resolver import SummaryResolver
from agentic_kit_flow.pattern.plan_execute.base import PlanExecuteBase
from agentic_kit_flow.pattern.plan_execute.schema import PlanExecuteState


class CotPlanExecuteGraph(PlanExecuteBase):
    def _init_graph(self):
        """初始化graph： CompiledStateGraph"""

        def should_continue(state: PlanExecuteState) -> Literal['executor', 'resolver']:
            if len(state['revised_steps']) == 0 or state['should_finish'] is True:
                return 'resolver'
            return 'executor'

        def planner_node(state: PlanExecuteState):
            res = self.planner.invoke({
                'task': state['task']
            })
            return {
                'init_steps': res['steps'],
                'init_step': res['steps'][0] if len(res['steps']) > 0 else None,
            }

        def executor_node(state: PlanExecuteState):
            current_step = None
            if 'past_step_results' not in state or len(state['past_step_results']) == 0:
                # 第一步
                current_step = state['init_step']
            else:
                if len(state['revised_steps']) > 0:
                    current_step = state['revised_steps'][0]
                else:
                    current_step = None

            if current_step:
                res = self.executor.invoke({
                    'ex_info': '\n'.join(state['past_step_results']),
                    'step': current_step
                })

                if res:
                    return {
                        'past_steps': [current_step],
                        'past_step_results': [res['step_result']],
                        'call_log': res['call_log'],
                        'should_finish': True if current_step.is_last_step else False
                    }
                else:
                    return {
                        'past_steps': [current_step],
                        'past_step_results': [current_step.plan],
                        'should_finish': True if current_step.is_last_step else False
                    }
            else:
                return {
                    'should_finish': True
                }

        def replanner_node(state: PlanExecuteState):
            if state['should_finish']:
                return {
                    'revised_steps': [],
                }

            task = state['task']
            past_step_results = state['past_step_results']
            init_steps = state['init_steps']
            res = self.replanner.invoke(
                {
                    'task': task,
                    'past_step_results': past_step_results,
                    'init_steps': init_steps
                }
            )

            return {
                'revised_steps': res['steps'],
                'should_finish': True if len(res['steps']) == 0 else False
            }

        def resolver_node(state: PlanExecuteState):
            res = self.resolver.invoke(
                {
                    'task': state['task'],
                    'steps': state['past_steps'],
                    'step_results': state['past_step_results'],
                }
            )

            return {
                'final_result': res['final_result']
            }

        graph_builder = StateGraph(PlanExecuteState)
        graph_builder.add_node('planer', planner_node)
        graph_builder.add_node('executor', executor_node)
        graph_builder.add_node('replanner', replanner_node)
        graph_builder.add_node('resolver', resolver_node)

        graph_builder.add_edge('planer', 'executor')
        graph_builder.add_edge('executor', 'replanner')
        graph_builder.add_conditional_edges('replanner', should_continue)
        graph_builder.add_edge('resolver', END)
        graph_builder.add_edge(START, 'planer')

        self.graph = graph_builder.compile()

    @classmethod
    def create(cls, llm: BaseChatModel, **kwargs):
        tools = kwargs.get('tools', [])
        assert tools is not None
        assert len(tools) > 0

        planner = SequenceCotPlanner.create(llm=llm, tools=tools)
        replanner = CotRePlanner.create(llm=llm, tools=tools)
        executor = StepExecutor.create(llm=llm, tools=tools)
        resolver = SummaryResolver.create(llm=llm, tools=tools)

        pe = cls(llm=llm, planner=planner, replanner=replanner, executor=executor, resolver=resolver, **kwargs)
        return pe
