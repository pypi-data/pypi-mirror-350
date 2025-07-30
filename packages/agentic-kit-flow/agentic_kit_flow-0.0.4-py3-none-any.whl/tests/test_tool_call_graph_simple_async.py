import unittest

from agentic_kit_eda.toolkit.mcp_toolkit import McpToolkit

from agentic_kit_flow.pattern.tool_use.tool_call_graph import ToolCallSingleTaskGraph
from tests.env import llm


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_create_mcp_toolkit(self):
        MCP_SERVER_SSE_URL = "http://221.229.0.177:8881/mcp/sample"
        tk = await McpToolkit.acreate(connection={
            "transport": 'streamable_http',
            "url": MCP_SERVER_SSE_URL,
        }, name='ds', description='ds tools')
        print(tk)

        tool_call_graph = ToolCallSingleTaskGraph.create(llm=llm, tools=tk.get_tools())
        res = await tool_call_graph.ainvoke({
            # 'task': '帮我通过api问答回答我的问题，请问"你是谁"',
            # 'task': '如果正常帮我通过api问答回答我的问题，使用的模型是："qwen-max^qwen-max^377@shubiaobiao^15"，请问"你是谁"',
            # 'task': '请帮我查看一下目前都支持哪些模型调用？',
            # 'task': '请查询一下"claude-3-opus^claude-3-opus^413@online^15"这个模型的详细信息？'
            # 'task': '请测试一下api服务是否正常'
            'task': '请计算100+200=?',
        })
        print('dump res --------')
        print(res)

        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
