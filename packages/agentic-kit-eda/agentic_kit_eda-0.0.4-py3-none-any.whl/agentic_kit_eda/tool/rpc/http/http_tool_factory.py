from .http_tool import GetTool, PostTool, PutTool, PatchTool, DeleteTool
from .http_tool_async import GetToolAsync, PostToolAsync, PatchToolAsync, DeleteToolAsync, PutToolAsync
from .schema import ApiDef


class HttpToolFactory:
    @classmethod
    def create_tool(cls, tool_def: ApiDef):
        if tool_def.method == 'get':
            if tool_def.is_async:
                tool = GetToolAsync(tool_def=tool_def)
            else:
                tool = GetTool(tool_def=tool_def)
        elif tool_def.method == 'post':
            if tool_def.is_async:
                tool = PostToolAsync(tool_def=tool_def)
            else:
                tool = PostTool(tool_def=tool_def)
        elif tool_def.method == 'put':
            if tool_def.is_async:
                tool = PutToolAsync(tool_def=tool_def)
            else:
                tool = PutTool(tool_def=tool_def)
        elif tool_def.method == 'delete':
            if tool_def.is_async:
                tool = DeleteToolAsync(tool_def=tool_def)
            else:
                tool = DeleteTool(tool_def=tool_def)
        elif tool_def.method == 'patch':
            if tool_def.is_async:
                tool = PatchToolAsync(tool_def=tool_def)
            else:
                tool = PatchTool(tool_def=tool_def)
        else:
            tool = None
        return tool
