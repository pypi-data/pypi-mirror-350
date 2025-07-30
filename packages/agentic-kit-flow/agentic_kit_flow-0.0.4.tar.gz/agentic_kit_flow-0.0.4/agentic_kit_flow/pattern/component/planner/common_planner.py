from .base import PlannerBase


class CommonPlanner(PlannerBase):
    """通用planner"""

    default_prompt: str = '''
# 请根据以下任务制定计划: 
{task}

# 要求:
1. 不需要生成工具调用，只生成计划文本
'''

    prompt_required_field: list[str] = ['task']



class CommonToolPlanner(PlannerBase):
    """根据tools生成的planner"""

    default_prompt: str = '''
# 请根据以下任务制定计划: 
{task}

# 可用工具：
{tools}

# 要求：
1. 如果计划分成多个步骤，可以生成多个tool_call
'''

    prompt_required_field: list[str] = ['task', 'tools']
