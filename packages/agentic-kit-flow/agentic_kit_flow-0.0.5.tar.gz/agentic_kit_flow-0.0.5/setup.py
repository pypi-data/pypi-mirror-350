from setuptools import setup, find_packages

setup(
    name='agentic-kit-flow',
    version="0.0.5",
    author="manson",
    author_email="manson.li3307@gmail.com",
    description='About agent flow&pattern based on Langgraph',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',  # 添加开发状态分类器
        'Intended Audience :: Developers',  # 添加目标受众分类器
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.10',
    # todo: update requirements
    install_requires=[
        "agentic_kit_core",
        "langchain_community",
        "langchain_core",
        "langgraph",
        "pydantic",
        "python_redis_lock",
        "setuptools",
        "starlette",
        "typing_extensions",
        "websocket_client"
    ],
    keywords=['AI', 'LLM', 'Agent'],
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '.csv']
    },
)
