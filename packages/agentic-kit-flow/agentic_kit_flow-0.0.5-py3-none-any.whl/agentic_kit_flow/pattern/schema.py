from typing import Union

from pydantic import BaseModel


class PlanModel(BaseModel):
    """cot step"""

    step_name: str

    plan: str

    tool: str = ''

    tool_args: Union[str, dict] = ''

    tool_name: str = ''

    result_name: str = ''

    is_last_step: bool = False
