import unittest

from agentic_kit_eda.toolkit.mcp_toolkit import McpToolkit

from agentic_kit_flow.pattern.tool_use.tool_call_graph import ToolCallSingleTaskGraph
from tests.env import llm


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_create_mcp_toolkit(self):
        MCP_SERVER_SSE_URL = "http://221.229.0.177:8881/mcp/sample"
        connnection = {
            'transport': 'streamable_http',
            'url': MCP_SERVER_SSE_URL
        }

        tk = await McpToolkit.acreate(connection=connnection, name='ds', description='ds tools')
        print(tk.get_tools())

        tool_call_graph = ToolCallSingleTaskGraph.create(llm=llm, tools=tk.get_tools(), is_async=True)
        res = await tool_call_graph.graph.ainvoke({
            'task': '请计算100+200=?',
        }, config={'thread_id': 'abcd'})
        print('dump res --------')
        print(res)

        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
