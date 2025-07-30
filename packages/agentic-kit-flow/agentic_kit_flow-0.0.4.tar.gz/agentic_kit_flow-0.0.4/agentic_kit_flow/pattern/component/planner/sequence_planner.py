from .cot_planner import CotPlanner
from .parser import PlanParserYaml


class SequenceCotPlanner(CotPlanner):
    """生成完整串行计划"""

    default_prompt = '''
# 你是一个任务规划专家
1. 对于以下任务，请制定逐步解决问题的计划。
2. 对于每个计划，指出需要使用哪些外部工具以及工具输入来获取证据。
3. 你可以将证据或结果存储到变量#E中，以便后续工具调用。（计划，#E1，计划，#E2，计划，……）
4. 对于那些不需要借助外部工具tool来解决的问题，你可以自己回答
5. 每个步骤step要尽量的详细和尽量小工作量
6. 每个步骤step要尽量的详细描述任务内容，需要调用的工具tool和调用参数
7. 每个plan字段要尽量的详细描述任务内容，需要调用的工具tool和调用参数

# 可供调用的工具可以是以下几种之一，工具调用请严格遵守参数要求：
{tools}

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

# 以下是你要制定计划的任务：
{task}
'''

    plan_parser = PlanParserYaml()
