from langchain_core.tools import tool
from typing_extensions import Annotated, Union

@tool(
    parse_docstring=True,
    return_direct=False
)
def calculator_add_tool(
    x: Annotated[Union[int, float], '加法计算需要传入的数值，可以是整型或者浮点型'],
    y: Annotated[Union[int, float], '加法计算需要传入的数值，可以是整型或者浮点型'],
) -> Union[int, float]:
    """
    这个工具是加法计算器，可以计算两个数值的和。

    Args:
        x: 加法计算需要传入的数值，可以是整型或者浮点型.
        y: 加法计算需要传入的数值，可以是整型或者浮点型.

    Returns:
         Union[int, float] 两个数字相加的总和

    """
    print('=====calculator_add_tool=======')
    print(f'cal = {x} + {y}')
    return x + y
