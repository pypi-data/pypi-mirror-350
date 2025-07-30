from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.constants import END
from langgraph.graph import StateGraph
from typing_extensions import List, Literal, TypedDict

from .schema import ReflectionState
from core.base.graph import PatternMultiLlmGraphBase


class BasicReflection(PatternMultiLlmGraphBase):
    generate_llm: BaseChatModel
    '''生成模型'''

    generate_prompt: str

    reflection_llm: BaseChatModel
    '''自省模型'''

    state_cls = None

    reflection_prompt: str

    def __init__(self, llms: TypedDict[str, BaseChatModel], **kwargs):
        super().__init__(**kwargs)

        generate_llm = llms.get('generate_llm', None)
        reflection_llm = llms.get('reflection_llm', None)
        generate_prompt = kwargs.get('generate_prompt', None)
        reflection_prompt = kwargs.get('reflection_prompt', None)
        assert generate_llm is not None
        assert reflection_llm is not None
        assert generate_prompt is not None
        assert reflection_prompt is not None
        self.generate_llm = generate_llm
        self.generate_prompt = generate_prompt
        self.reflection_llm = reflection_llm
        self.reflection_prompt = reflection_prompt

        self._init_graph()

    def _init_graph(self):
        def generation_node(state: ReflectionState) -> ReflectionState:
            res = {'messages': [generate_callable.invoke(state['messages'])]}
            return res

        def reflection_node(state: ReflectionState) -> ReflectionState:
            # Other messages we need to adjust
            cls_map = {'ai': HumanMessage, 'human': AIMessage}

            # First message is the original user request. We hold it the same for all nodes
            translated = [state['messages'][0]] + [
                cls_map[msg.type](content=msg.content) for msg in state['messages'][1:]
            ]
            res = reflect_callable.invoke({'messages': translated})

            # this will be treated as a feedback for the generator
            return {
                'messages': [HumanMessage(content=res.content)],
                'loop_counter': state['loop_counter'] - 1
            }

        def should_continue(state: List[BaseMessage]) -> Literal['reflect', END]:
            if state['loop_counter'] <= 0:
                # End after 'loop_counter' iterations
                return END
            return 'reflect'

        builder = StateGraph(ReflectionState)
        builder.add_node('generate', generation_node)
        builder.add_node('reflect', reflection_node)
        builder.set_entry_point('generate')
        builder.add_conditional_edges('generate', should_continue)
        builder.add_edge('reflect', 'generate')
        self.graph = builder.compile()

        # builder = StateGraph(self.state_cls)
        # builder.add_node('llm_call', self._llm_call)
        # builder.add_conditional_edges('llm_call', self._should_continue)
        # builder.set_entry_point('llm_call')
        # self.graph = builder.compile()

    @classmethod
    def create(cls, llms: TypedDict[str, BaseChatModel], **kwargs):
        agent = cls(llms=llms, **kwargs)

        _generate_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    'system', agent.generate_prompt,
                ),
                MessagesPlaceholder(variable_name='messages'),
            ]
        )
        generate_callable = _generate_prompt | agent.generate_llm

        _reflection_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    'system', agent.reflection_prompt,
                ),
                MessagesPlaceholder(variable_name='messages'),
            ]
        )
        reflect_callable = _reflection_prompt | agent.reflection_llm

        # def generation_node(state: ReflectionState) -> ReflectionState:
        #     res = {'messages': [generate_callable.invoke(state['messages'])]}
        #     return res
        #
        # def reflection_node(state: ReflectionState) -> ReflectionState:
        #     # Other messages we need to adjust
        #     cls_map = {'ai': HumanMessage, 'human': AIMessage}
        #
        #     # First message is the original user request. We hold it the same for all nodes
        #     translated = [state['messages'][0]] + [
        #         cls_map[msg.type](content=msg.content) for msg in state['messages'][1:]
        #     ]
        #     res = reflect_callable.invoke({'messages': translated})
        #
        #     # this will be treated as a feedback for the generator
        #     return {
        #         'messages': [HumanMessage(content=res.content)],
        #         'loop_counter': state['loop_counter'] - 1
        #     }
        #
        # builder = StateGraph(ReflectionState)
        # builder.add_node('generate', generation_node)
        # builder.add_node('reflect', reflection_node)
        # builder.set_entry_point('generate')
        #
        # def should_continue(state: List[BaseMessage]) -> Literal['reflect', END]:
        #     if state['loop_counter'] <= 0:
        #         # End after 'loop_counter' iterations
        #         return END
        #     return 'reflect'
        #
        # builder.add_conditional_edges('generate', should_continue)
        # builder.add_edge('reflect', 'generate')
        # agent._graph = builder.compile()

        return agent

#
# if __name__=='__main__':
#
#     import os
#     import sys
#
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     parent_dir = os.path.dirname(base_dir)
#     sys.path.append(parent_dir)
#     pparent_dir = os.path.dirname(parent_dir)
#     sys.path.append(pparent_dir)
#
#     from core.brain.brain_prebuilt import gpt4o_brain
#
#     _generate_prompt: str = '''
#             You are an AI assistant researcher tasked with researching on a variety of topics in a short summary of 5 paragraphs.
#             Generate the best research possible as per user request.
#             If the user provides critique, respond with a revised version of your previous attempts.
#         '''
#
#     _reflection_prompt: str = '''
#             You are a senior researcher.
#             Provide detailed recommendations, including requests for length, depth, style, etc.
#             to an asistant researcher to help improve this researches
#         '''
#
#     graph = BasicReflection.make_node(
#         generate_llm=gpt4o_brain,
#         reflection_llm=gpt4o_brain,
#         generate_prompt=_generate_prompt,
#         reflection_prompt=_reflection_prompt
#     )
#     for event in graph.stream(
#             {
#                 'messages': [
#                     HumanMessage(
#                         content='1+2+3+100等于多少'
#                     )
#                 ],
#                 'loop_counter': 2
#             },
#             stream_mode='values',
#     ):
#         print(event)
#         print('---')
