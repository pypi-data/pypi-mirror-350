from agentic_kit_eda.tool.rpc.http.http_tool_factory import HttpToolFactory
from agentic_kit_eda.tool.rpc.http.schema import ApiDef
from .flat_toolkit import FlatToolkit


class HttpToolkit(FlatToolkit):

    def dump(self):
        print('----dump HttpToolkit----')
        super().dump()

    @classmethod
    def create(cls, api_list: list[ApiDef], name: str, description: str, **kwargs):
        assert api_list is not None
        assert len(api_list) > 0

        tk = cls(name=name, description=description)
        for api in api_list:
            http_tool = HttpToolFactory.create_tool(tool_def=api)
            tk.add_tool(http_tool)
        return tk
