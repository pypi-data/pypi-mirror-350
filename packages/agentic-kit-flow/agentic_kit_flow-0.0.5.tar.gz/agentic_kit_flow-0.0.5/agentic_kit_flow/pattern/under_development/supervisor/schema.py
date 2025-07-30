from core.base.schema import BaseState

ROUTER_ACTION_FINISH = 'FINISH'


class RouterAction(BaseState):
    """Worker to route to next. If no workers needed, route to FINISH."""

    next: str
