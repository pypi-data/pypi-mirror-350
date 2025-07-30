from abc import ABC, abstractmethod

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from langgraph.graph.state import CompiledStateGraph
from typing_extensions import List

from .runnable import Runnable


class PatternGraphBase(Runnable, ABC):
    """设计模式相关的Graph的基类"""

    graph: CompiledStateGraph = None

    def __init__(self, **kwargs):
        print('PatternGraphBase.__init__ %s' % kwargs)
        super().__init__(**kwargs)

    @abstractmethod
    def _init_graph(self):
        """初始化graph： CompiledStateGraph"""
        raise NotImplemented

    @classmethod
    @abstractmethod
    def create(cls, **kwargs):
        raise NotImplemented

    @property
    def callable(self):
        """alias of graph"""
        return self.graph

    def get_context(self):
        return self.graph.get_state({"configurable": {"thread_id": self.thread_id}})

    def astream_events(self, *args, **kwargs):
        return self.graph.astream_events(*args, **kwargs)


class PatternSingleLlmGraphBase(PatternGraphBase):
    """包含单llm设计模式相关的Graph的基类"""

    llm: BaseChatModel

    prompt_template: ChatPromptTemplate = None

    def __init__(self, llm: BaseChatModel, prompt_template: ChatPromptTemplate = None, **kwargs):
        super().__init__(**kwargs)
        print('PatternSingleLlmGraphBase.__init__ %s' % kwargs)

        assert llm is not None

        self.llm = llm
        self.prompt_template = prompt_template

    @classmethod
    @abstractmethod
    def create(cls, llm: BaseChatModel, **kwargs):
        raise NotImplemented

    @property
    def llm_callable(self):
        if self.prompt_template:
            return self.prompt_template | self.llm
        else:
            return self.llm


class PatternMultiLlmGraphBase(PatternGraphBase):
    """包含多llm设计模式相关的Graph的基类"""

    llms: dict[str, BaseChatModel]
    '''结构为{'role': 'llm'}'''

    prompt_templates: dict[str, ChatPromptTemplate]

    def __init__(self, llms: dict[str, BaseChatModel], prompt_templates: dict[str, ChatPromptTemplate] = None, **kwargs):
        print('PatternMultiLlmGraphBase.__init__')
        super().__init__(**kwargs)

        assert llms is not None
        self.llms = llms
        self.prompt_templates = prompt_templates

    @classmethod
    @abstractmethod
    def create(cls, llms: dict[str, BaseChatModel], **kwargs):
        raise NotImplemented


class PatternToolGraphBase(PatternSingleLlmGraphBase):
    """包含tool calls设计模式相关的Graph的基类，依赖单llm作为推理模型"""

    tools: List[BaseTool]

    def __init__(self, llm: BaseChatModel, tools: List[BaseTool], prompt_template: ChatPromptTemplate, **kwargs):
        super().__init__(llm=llm, prompt_template=prompt_template, **kwargs)
        print('PatternToolGraphBase.__init__ %s' % kwargs)

        assert tools is not None
        assert len(tools) > 0
        self.tools = tools

    @classmethod
    @abstractmethod
    def create(cls, llm: BaseChatModel, tools: List[BaseTool], **kwargs):
        raise NotImplemented

    @property
    def llm_callable_with_tools(self):
        if self.prompt_template:
            return self.prompt_template | self.llm.bind_tools(tools=self.tools)
        else:
            return self.llm.bind_tools(tools=self.tools)
