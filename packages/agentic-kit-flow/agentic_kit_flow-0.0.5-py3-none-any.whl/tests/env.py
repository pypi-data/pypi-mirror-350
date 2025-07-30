import os

from langchain_community.chat_models import ChatTongyi

from tests.tools import calculator_add_tool, calculator_sub_tool, calculator_multiply_tool

api_key = os.getenv("QWEN_API_KEY", '')
llm = ChatTongyi(
    model_name='qwen-max-latest',
    api_key=api_key,
    top_p=0.1,
)

tools = [calculator_add_tool, calculator_sub_tool, calculator_multiply_tool]
