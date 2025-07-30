from .base import PlannerBase


class CotPlanner(PlannerBase):
    """Chain-of-Thought planner"""

    prompt_required_field: list[str] = ['task', 'tools']
