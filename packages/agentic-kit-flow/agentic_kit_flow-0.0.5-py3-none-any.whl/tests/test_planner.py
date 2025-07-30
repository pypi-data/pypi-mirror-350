import unittest

from agentic_kit_core.utils.tools import get_tools_desc_for_prompt_zh

from agentic_kit_flow.pattern.component.planner import FirstStepCotPlanner, CotRePlanner, SequenceCotPlanner, \
    PlanParserYaml, PlannerBase
from agentic_kit_flow.pattern.component.planner.common_planner import CommonPlanner, CommonToolPlanner
from tests.env import llm, tools


class MyTestCase(unittest.TestCase):
    def test_planner(self):
        planner = CommonToolPlanner.create(llm=llm, plan_parser=PlanParserYaml())
        result = planner.invoke({
            'task': "我是一名工人，每个小时的工资是10元。上个月我工作了30个小时，这个月我工作了60个小时。上个月我购买了一台车花费了200元，请问我现在剩余多少钱?",
            'tools': get_tools_desc_for_prompt_zh(tools)
        })
        print(result)

        # planner = CommonPlanner.create(llm=llm, plan_parser=PlanParserYaml())
        # result = planner.invoke({
        #     'task': "我是一名工人，每个小时的工资是10元。上个月我工作了30个小时，这个月我工作了60个小时。上个月我购买了一台车花费了200元，请问我现在剩余多少钱?",
        #     # 'tools': get_tools_desc_for_prompt_zh(tools)
        # })
        # print(result)

        # _prompt: str = '''
        # # 请根据以下任务制定计划:
        # {task}
        #
        # # 要求:
        # 1. 不需要生成工具调用，只生成计划文本
        # '''
        # planner = PlannerBase.create(llm=llm, plan_parser=PlanParserYaml(), prompt=_prompt)
        # result = planner.invoke({
        #     'task': "我是一名工人，每个小时的工资是10元。上个月我工作了30个小时，这个月我工作了60个小时。上个月我购买了一台车花费了200元，请问我现在剩余多少钱?",
        #     # 'tools': get_tools_desc_for_prompt_zh(tools)
        # })
        # print(result)

    def test_common_planner_with_tools(self):
        planner = CommonToolPlanner.create(llm=llm)
        result = planner.invoke({
            'task': "我是一名工人，每个小时的工资是10元。上个月我工作了30个小时，这个月我工作了60个小时。上个月我购买了一台车花费了200元，请问我现在剩余多少钱?",
            'tools': get_tools_desc_for_prompt_zh(tools)
        })
        print(result)

    def test_common_planner(self):
        planner = CommonPlanner.create(llm=llm)
        result = planner.invoke({
            'task': "我是一名工人，每个小时的工资是10元。上个月我工作了30个小时，这个月我工作了60个小时。上个月我购买了一台车花费了200元，请问我现在剩余多少钱?",
        })
        print(result)

    def test_squence_planner(self):
        planner = SequenceCotPlanner.create(llm=llm)
        result = planner.invoke({
            'task': "我是一名工人，每个小时的工资是10元。上个月我工作了30个小时，这个月我工作了60个小时。上个月我购买了一台车花费了200元，请问我现在剩余多少钱?",
            'tools': get_tools_desc_for_prompt_zh(tools)
        })
        print(result)
        print('------详细step-------')
        for item in result['steps']:
            print(item)
        print(result['plans'])

    def test_first_step_planner(self):
        planner = FirstStepCotPlanner.create(llm=llm)
        result = planner.invoke({
            'task': "我是一名工人，每个小时的工资是10元。上个月我工作了30个小时，这个月我工作了60个小时。上个月我购买了一台车花费了200元，请问我现在剩余多少钱?",
            'tools': get_tools_desc_for_prompt_zh(tools)
        })
        print(result)
        print('------详细step-------')
        for item in result['steps']:
            print(item)
        print(result['plans'])

    def test_re_planner(self):
        planner = SequenceCotPlanner.create(llm=llm)
        result = planner.invoke({
            'task': "我是一名工人，每个小时的工资是10元。上个月我工作了30个小时，这个月我工作了60个小时。上个月我购买了一台车花费了200元，请问我现在剩余多少钱?",
            'tools': get_tools_desc_for_prompt_zh(tools)
        })

        replanner = CotRePlanner.create(llm=llm)

        # 1. 未完成全部任务
        # result = replanner.invoke({
        #     'task': "我是一名工人，每个小时的工资是10元。上个月我工作了30个小时，这个月我工作了60个小时。上个月我购买了一台车花费了200元，请问我现在剩余多少钱?",
        #     'past_step_results': '''
        #     计算上个月的工资，使用乘法计算器计算每小时工资10元与工作小时数30的乘积。通过调用工具tool得到结果是：300。
        #     计算这个月的工资，使用乘法计算器计算每小时工资10元与工作小时数60的乘积。通过调用工具tool得到结果是：600。
        #     计算两个月的总工资，使用加法计算器将上个月和这个月的工资相加。通过调用工具tool得到结果是：900。
        #     ''',
        #     'init_steps': result['steps'],
        #     'tools': get_tools_desc_for_prompt_zh(tools)
        # })

        # 2. 已完成全部任务
        result = replanner.invoke({
            'task': "我是一名工人，每个小时的工资是10元。上个月我工作了30个小时，这个月我工作了60个小时。上个月我购买了一台车花费了200元，请问我现在剩余多少钱?",
            'past_step_results': '''
            Step#1: 计算上个月的工资，使用乘法计算器计算每小时工资10元与工作小时数30的乘积。通过调用工具tool得到结果是：300。
            Step#2: 计算这个月的工资，使用乘法计算器计算每小时工资10元与工作小时数60的乘积。通过调用工具tool得到结果是：600。
            Step#3: 计算两个月的总工资，使用加法计算器将上个月和这个月的工资相加。通过调用工具tool得到结果是：900。
            Step#4: 计算剩余的钱，使用减法计算器从总工资中减去购车费用200元, 通过调用工具tool得到结果是：700。
            ''',
            'init_steps': result['steps'],
            'tools': get_tools_desc_for_prompt_zh(tools)
        })

        print(result)
        print('------详细re step-------')
        for item in result['steps']:
            print(item)
        print(result['plans'])

if __name__ == '__main__':
    unittest.main()
