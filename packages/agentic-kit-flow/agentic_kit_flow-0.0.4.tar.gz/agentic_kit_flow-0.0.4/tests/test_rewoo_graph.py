import unittest

from agentic_kit_flow.pattern.rewoo import CotReWooGraph
from tests.env import llm, tools


class MyTestCase(unittest.TestCase):
    def test_cot_rewoo_graph(self):
        rewoo = CotReWooGraph.create(llm=llm, tools=tools)
        # task = "我是一名工人，每个小时的工资是29.9元。上个月我工作了37个小时，这个月我工作了24.5个小时。上个月我购买了一台车花费了291元，请问我现在剩余多少钱?"
        # task = "我弹奏了一首钢琴曲，内容是abc格式，如下: xxyyddaaa，帮我评价一下能够得多少分，然后根据我弹奏的内容再帮我续写一个钢琴曲，23秒，悲伤风格"
        task = "What is 10*5 then to the power of 2? do it step by step"

        print('########## 通过ReWooGraph执行任务 ##########')
        print(task)
        print('\n\n\n')
        res = rewoo.graph.invoke({
            "task": task,
        })
        print(f"通过ReWooGraph获得最终结果: \n{task}\n{res['final_result']}")

        # for s in g.graph.stream({
        #     "task": task,
        # }, stream_mode='updates'):
        #     print("---1")
        #     print(s)
        #     print("---2")


if __name__ == '__main__':
    unittest.main()
