import unittest

from agentic_kit_eda.toolkit.mcp_toolkit import McpToolkit


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_create_mcp_toolkit(self):
        MCP_SERVER_SSE_URL = "http://221.229.0.177:8881/mcp/sample"
        tk = await McpToolkit.acreate(connection={
            "transport": 'streamable_http',
            "url": MCP_SERVER_SSE_URL,
        }, name='ds', description='ds tools')
        print(tk)

        args = {
            'a': 2,
            'b': 3,
        }
        for tool in tk.get_tools():
            res = await tool.ainvoke(args)
            print(res)

        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
