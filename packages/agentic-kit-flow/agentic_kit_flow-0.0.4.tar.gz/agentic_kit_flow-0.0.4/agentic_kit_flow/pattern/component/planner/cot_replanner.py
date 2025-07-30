from typing import List

from agentic_kit_core.utils.prompt import check_prompt_required_filed
from agentic_kit_core.utils.tools import get_tools_desc_for_prompt_zh
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from tenacity import retry, stop_after_attempt

from .base import PlannerBase, planner_retry_failed_callback
from .parser import PlanParserYaml
from .schema import RePlannerCotState

class CotRePlanner(PlannerBase):
    """Chain-of-Thought replanner"""

    prompt_required_field: list[str] = ['task', 'tools', 'init_steps', 'past_step_results']

    default_prompt = '''
# 你是一个任务规划专家
1. 对于以下任务，请制定逐步解决问题的计划。
2. 对于每个计划，指出需要使用哪些外部工具以及工具输入来获取证据。
3. 你可以将证据或结果存储到变量#E中，以便后续工具调用。（计划，#E1，计划，#E2，计划，……）
4. 对于那些不需要借助外部工具tool来解决的问题，你可以自己回答
5. 每个步骤step要尽量的详细和尽量小工作量
6. 每个步骤step要尽量的详细描述任务内容，需要调用的工具tool和调用参数

# 以下是你要制定计划的<任务task>：
{task}
</任务task>

# 可供调用的工具可以是以下几种之一，工具调用请严格遵守参数要求：
{tools}

# 你的<原始计划>是:
{init_steps}
</原始计划>

# <已执行完成的步骤和工作>如下，其中包含中间过程的解析和结果:
{past_step_results}
</已执行完成的步骤和工作>

# 生成要求：
1. 请根据整体目标<任务>，<原始计划>和<已执行完成的步骤和工作>，来判断是否需要进一步的工作来完成整体目标。
2. 如果还需要进一步的工作，请继续制定逐步解决问题的计划。对于每个计划，指出需要使用哪些外部工具以及工具输入来获取证据。你可以将证据存储到变量#E中，以便后续工具调用。（计划，#E1，计划，#E2，计划，……）
3. 新生成的计划不能与已完成的计划重复.
4. 如果已经<已执行完成的步骤和工作>已经得到了最终结果，无需进一步的工作来完成整体目标。
5. 输出格式参考已完成步骤的格式，并可以转化成yaml，不许用()
6. <#E>替换称上一个步骤中的result
7. 新生成的计划请延续之前的step_name序号继续排列
8. 不需要单独生成最终确认结果的step步骤。
9. 不要生成最终确认step

# 回答输出格式要求：
## 您必须仅输出整个计划，格式为符合以下模式的 YAML 字典：
plans:
  - step_name: "Step#1"
    plan: "first plan"
    tool: "tool_name[tool_input]"
    tool_args: "tool's args schema" 
    tool_name: "tool_name"
    is_last_step: false
    result_name: "#E1"
  - step_name: "Step#2"
    plan: "second plan"
    tool: "tool_name[tool_input]"
    tool_args: "tool's args schema"
    tool_name: "tool_name"
    result_name: "#E2"
    is_last_step: true
## 不要用反引号 ... 包裹您的计划 YAML，也不要为其添加 YAML 标签。
## 不要对输出应用任何格式化，除非是指令中指定的格式以及以下示例中所展示的格式。

# 举例：
按照以下示例生成您的计划并遵守其格式——
## 示例1——正常流程：
* 任务：托马斯（Thomas）、托比（Toby）和丽贝卡（Rebecca）在一周内总共工作了157小时。托马斯工作了x小时。托比工作的时间比托马斯的两倍少10小时，而丽贝卡工作的时间比托比少8小时。丽贝卡工作了多少小时？
* 输出：
    plans:
      - plan: "鉴于托马斯工作了x小时，将问题转化为代数表达式，并通过WolframAlpha求解."
        tool: "WolframAlpha[Solve x + (2x − 10) + ((2x − 10) − 8) = 157]"
        tool_args: x=10
        tool_name: "WolframAlpha"
        step_name: "Step#1"
        result_name: "#E1"
        is_last_step: False
      - plan: "找出托马斯工作了多少小时。"
        tool: "LLM[What is x]"
        tool_args: x=10
        tool_name: "LLM"
        step_name: "Step#2"
        result_name: "#E2"
        is_last_step: False
      - plan: "找出托马斯工作的小时数。"
        tool: "LLM[What is x]"
        tool_args: x=10
        tool_name: "LLM"
        step_name: "Step#3"
        result_name: "#E3"
        is_last_step: False
      - plan: "计算丽贝卡工作的小时数。"
        tool: "Calculator[(2 ∗ 5 − 10) − 8]"
        tool_args: x=10
        tool_name: "Calculator"
        step_name: "Step#4"
        result_name: "#E4"
        is_last_step: True

## 示例2——无需生成执行计划：
* 任务：托马斯（Thomas）、托比（Toby）和丽贝卡（Rebecca）在一周内总共工作了157小时。托马斯工作了x小时。托比工作的时间比托马斯的两倍少10小时，而丽贝卡工作的时间比托比少8小时。丽贝卡工作了多少小时？
* 输出：
```yaml
```

# 请开始!详细描述你的计划。每个计划后面只能跟随一个#E。
'''

    plan_parser = PlanParserYaml()

    # @retry(stop=stop_after_attempt(3), retry_error_callback=planner_retry_failed_callback)
    def invoke(self, state: RePlannerCotState):
        if 'task' not in state or 'tools' not in state or 'init_steps' not in state or 'past_step_results' not in state:
            raise Exception(f'Missing state fields: {state} should contain {self.prompt_required_field}')

        print(f'########## CotRePlanner 开始执行分析 [{state["task"]}] ##########')

        task = state["task"]
        tools = state["tools"]
        past_step_results = state["past_step_results"]
        _init_steps = [f'{step.step_name}:{step.plan}' for step in state["init_steps"]]
        print(f'past_step_results=\n{past_step_results}')
        init_steps_formatted = '\n'.join(_init_steps)
        print(f"init_steps=\n{init_steps_formatted}")
        response = self.llm_callable.invoke({
            'task': task,
            'tools': tools,
            'past_step_results': past_step_results,
            'init_steps': '\n'.join(_init_steps),
        })

        plans = response.content
        steps = self.plan_parser.parse(content=plans)
        if len(steps) == 0:
            return { 'steps': [], 'plans': [] }
        # for item in steps:
        #     print(item.model_dump_json())
        print('########## CotRePlanner 执行完毕，已生成详细step ##########\n\n\n')
        return {
            'task': task,
            'tools': tools,
            'past_step_results': past_step_results,
            'init_steps': '\n'.join(_init_steps),
            'steps': steps,
            'plans': plans
        }
