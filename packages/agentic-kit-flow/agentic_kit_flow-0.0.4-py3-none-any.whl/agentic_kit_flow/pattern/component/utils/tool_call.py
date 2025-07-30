from agentic_kit_core.utils.tools import find_tool_by_name
from langchain_core.messages import ToolCall, AIMessage, ToolMessage
from langchain_core.tools import BaseTool
from typing_extensions import List


def do_tool_call(ai_message: AIMessage, tools: List[BaseTool]) -> (bool, list[(ToolCall, ToolMessage)]):
    """将AiMessage转化为tool call，根据tool_call信息进行调用"""
    res = []
    is_success = False
    if isinstance(ai_message, AIMessage) and ai_message.tool_calls:
        print(f'准备调用tool calls: [{len(ai_message.tool_calls)}]个tool call')
        for tool_call in ai_message.tool_calls:
            print(f'执行调用: {tool_call}')
            selected_tool = find_tool_by_name(tool_name=tool_call['name'], tools=tools)
            if selected_tool is None:
                print(f'执行调用失败，找不到tool: {tool_call}')
                break

            tool_call_resp = selected_tool.invoke(tool_call)
            if isinstance(tool_call_resp, ToolMessage) and tool_call_resp.status == 'success':
                print(tool_call_resp)
                print(tool_call_resp)
                print(tool_call_resp)
                print(f'1执行调用成功: {tool_call_resp.content}')
                res.append((tool_call, tool_call_resp))
            else:
                print(f'执行调用失败，失败结果: {res}')

        # note: 确保AiMessage包含tool_calls，并且每个tool_calls都调用成功
        is_success = len(ai_message.tool_calls) > 0 and len(ai_message.tool_calls) == len(res)

    return is_success, res


async def async_do_tool_call(ai_message: AIMessage, tools: List[BaseTool]) -> (bool, list[(ToolCall, ToolMessage)]):
    """将AiMessage转化为tool call，根据tool_call信息进行调用"""
    res = []
    is_success = False
    if isinstance(ai_message, AIMessage) and ai_message.tool_calls:
        print(f'准备调用tool calls: [{len(ai_message.tool_calls)}]个tool call')
        for tool_call in ai_message.tool_calls:
            print(f'执行调用: {tool_call}')
            selected_tool = find_tool_by_name(tool_name=tool_call['name'], tools=tools)
            if selected_tool is None:
                print(f'执行调用失败，找不到tool: {tool_call}')
                break

            tool_call_resp = await selected_tool.ainvoke(tool_call)
            if isinstance(tool_call_resp, ToolMessage) and tool_call_resp.status == 'success':
                print(f'2执行调用成功: {tool_call_resp.content}')
                print(type(tool_call_resp.content))
                res.append((tool_call, tool_call_resp))
            else:
                print(f'执行调用失败，失败结果: {res}')

        # note: 确保AiMessage包含tool_calls，并且每个tool_calls都调用成功
        is_success = len(ai_message.tool_calls) > 0 and len(ai_message.tool_calls) == len(res)

    return is_success, res
