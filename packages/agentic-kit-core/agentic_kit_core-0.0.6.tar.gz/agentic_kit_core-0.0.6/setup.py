from pathlib import Path

from setuptools import setup, find_packages

setup(
    name='agentic-kit-core',
    version="0.0.6",
    author="manson",
    author_email="manson.li3307@gmail.com",
    description='Agent framework based on Langchain&Langgraph',
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
        "langgraph",
        "langchain",
        "langchain_core",
        "pydantic"
    ],
    keywords=['AI', 'LLM', 'Agent'],
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '.csv']
    },
)
