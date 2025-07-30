import unittest

from agentic_kit_flow.pattern.component.executor.sequence_executor import SequenceExecutor
from agentic_kit_flow.pattern.component.planner import SequenceCotPlanner
from agentic_kit_flow.pattern.component.resolver import SummaryResolver
from tests.env import llm, tools


class MyTestCase(unittest.TestCase):
    def test_simple_resolver(self):
        task = "我是一名工人，每个小时的工资是29.9元。上个月我工作了37个小时，这个月我工作了24.5个小时。上个月我购买了一台车花费了291元，请问我现在剩余多少钱?"
        planner = SequenceCotPlanner.create(llm=llm, tools=tools)
        result = planner.invoke({
            'task': task
        })
        # print(result)
        for item in result['steps']:
            print(item)
        # print(result['plans'])

        executor = SequenceExecutor.create(llm=llm, tools=tools)
        exe_result = executor.invoke({
            'steps': result['steps']
        })
        print('exe result ============ ')
        for item in exe_result['step_results']:
            print(item)
        print('--------')
        for item in exe_result['results']:
            print(item)
        print('--------')
        for item in exe_result['call_log']:
            print(item)

        resolver = SummaryResolver.create(llm=llm, tools=tools)
        final_result = resolver.invoke({
            'task': task,
            'steps': result['steps'],
            'step_results': exe_result['step_results'],
        })
        print('=========final result =========')
        print(final_result)

if __name__ == '__main__':
    unittest.main()
