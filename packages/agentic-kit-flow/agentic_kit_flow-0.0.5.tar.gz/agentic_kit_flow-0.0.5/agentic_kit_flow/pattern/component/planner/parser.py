from abc import abstractmethod, ABC

from agentic_kit_core.utils.parser import parse_yaml_llm_response

from ...schema import PlanModel


class PlanParserBase(ABC):
    @abstractmethod
    def parse(self, content: str) -> list[PlanModel]:
        raise NotImplemented


class PlanParserYaml(PlanParserBase):
    """yaml格式的解析器"""

    key: str = 'plans'

    def __init__(self, key: str = 'plans'):
        assert key is not None and key != ''
        self.key = key

    def parse(self, content: str) -> list[PlanModel]:
        try:
            plan_list = []
            res = parse_yaml_llm_response(content)
            if res is None:
                print('empty plans:\n%s' % content)
                return []
            plans = res.get(self.key, None)
            if not plans:
                print('empty plans:\n%s' % content)
                return []
            for item in plans:
                plan = PlanModel(**item)
                plan_list.append(plan)
            return plan_list
        except Exception as e:
            print(e)
            print('parse error:\n%s' % content)
            return []
