import unittest

from agentic_kit_flow.pattern.tool_use.tool_call_graph import ToolCallSingleTaskGraph
from tests.env import llm, tools


class MyTestCase(unittest.TestCase):
    def test_tool_call_graph_single_task(self):
        tool_call_graph = ToolCallSingleTaskGraph.create(llm=llm, tools=tools)
        res = tool_call_graph.graph.invoke({
            # 'task': '帮我通过api问答回答我的问题，请问"你是谁"',
            # 'task': '如果正常帮我通过api问答回答我的问题，使用的模型是："qwen-max^qwen-max^377@shubiaobiao^15"，请问"你是谁"',
            # 'task': '请帮我查看一下目前都支持哪些模型调用？',
            # 'task': '请查询一下"claude-3-opus^claude-3-opus^413@online^15"这个模型的详细信息？'
            # 'task': '请测试一下api服务是否正常'
            'task': '请计算100+200=?',
        }, config={'configurable': {'thread_id': 'abcd1234'}})
        print('dump res --------')
        print(res)

        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
