from langchain_core.tools import tool
from typing_extensions import Annotated, Union



@tool(
    parse_docstring=True,
    return_direct=False
)
def calculator_sub_tool(
    x: Annotated[Union[int, float], '减法计算需要传入的数值，可以是整型或者浮点型'],
    y: Annotated[Union[int, float], '减法计算需要传入的数值，可以是整型或者浮点型'],
) -> Union[int, float, str]:
    """
    这个工具是减法计算器，可以计算两个数的差值。

    Args:
        x: 减法计算需要传入的数值，可以是整型或者浮点型.
        y: 减法计算需要传入的数值，可以是整型或者浮点型.

    Returns:
         Union[int, float] 两个数值相减的差值

    """
    print('=====calculator_sub_tool=======')
    print(f'cal = {x} - {y}')
    return x - y
