import unittest

from agentic_kit_core.utils.tools import get_tools_desc_for_prompt_zh

from agentic_kit_flow.pattern.component.executor import StepExecutor
from agentic_kit_flow.pattern.component.executor.sequence_executor import SequenceExecutor
from agentic_kit_flow.pattern.component.planner import SequenceCotPlanner
from tests.env import llm, tools


class MyTestCase(unittest.TestCase):
    def test_sequence_executor(self):
        task = "我是一名工人，每个小时的工资是29.9元。上个月我工作了37个小时，这个月我工作了24.5个小时。上个月我购买了一台车花费了291元，请问我现在剩余多少钱?"
        planner = SequenceCotPlanner.create(llm=llm)
        result = planner.invoke({
            'task': task,
            'tools': get_tools_desc_for_prompt_zh(tools)
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

    def test_step_executor(self):
        task = "我是一名工人，每个小时的工资是29.9元。上个月我工作了37个小时，这个月我工作了24.5个小时。上个月我购买了一台车花费了291元，请问我现在剩余多少钱?"
        planner = SequenceCotPlanner.create(llm=llm)
        result = planner.invoke({
            'task': task,
            'tools': get_tools_desc_for_prompt_zh(tools)
        })
        # print(result)
        for item in result['steps']:
            print(item)
        # print(result['plans'])

        executor = StepExecutor.create(llm=llm, tools=tools)
        exe_result = executor.invoke({
            'step': result['steps'][0]
        })
        print('exe result ============ %s' % exe_result)

if __name__ == '__main__':
    unittest.main()
