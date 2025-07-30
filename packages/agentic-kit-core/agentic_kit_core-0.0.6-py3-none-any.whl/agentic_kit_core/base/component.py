from abc import abstractmethod, ABC

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from typing_extensions import List

from .schema import BaseState


class InvokeComponentLlmBase(ABC):
    """base class for invokable component, llm only"""

    llm: BaseChatModel

    def __init__(self, llm: BaseChatModel, **kwargs):
        assert llm is not None
        self.llm = llm

    @abstractmethod
    def invoke(self, state: BaseState):
        raise NotImplemented

    async def ainvoke(self, state: BaseState):
        pass

    @classmethod
    @abstractmethod
    def create(cls, llm: BaseChatModel, **kwargs):
        raise NotImplemented

    @property
    def llm_callable(self):
        return self.llm


class InvokeComponentLlmToolsBase(InvokeComponentLlmBase, ABC):
    """base class for invokable component, llm and tools"""

    tools: List[BaseTool]

    def __init__(self, llm: BaseChatModel, tools: List[BaseTool], **kwargs):
        super().__init__(llm=llm, **kwargs)

        assert tools is not None
        assert len(tools) > 0
        self.tools = tools

    @classmethod
    @abstractmethod
    def create(cls, llm: BaseChatModel, tools: List[BaseTool], **kwargs):
        raise NotImplemented

    @property
    def llm_callable_with_tools(self):
        return self.llm.bind_tools(tools=self.tools)

    @property
    def llm_callable(self):
        return self.llm


class InvokeComponentBase(InvokeComponentLlmToolsBase, ABC):
    """base class for invokable component with llm, tools and prompt"""

    prompt_template: ChatPromptTemplate

    def __init__(self, llm: BaseChatModel, tools: List[BaseTool], prompt_template: ChatPromptTemplate, **kwargs):
        super().__init__(llm=llm, tools=tools, **kwargs)

        assert prompt_template is not None
        self.prompt_template = prompt_template

    @classmethod
    @abstractmethod
    def create(cls, llm: BaseChatModel, tools: List[BaseTool], prompt_template: ChatPromptTemplate, **kwargs):
        raise NotImplemented

    @property
    def llm_callable_with_tools(self):
        return self.prompt_template | self.llm.bind_tools(tools=self.tools)

    @property
    def llm_callable(self):
        return self.prompt_template | self.llm


class InvokeComponentLLmPromptBase(InvokeComponentLlmBase, ABC):
    """base class for invokable component with llm, prompt"""

    prompt_template: ChatPromptTemplate

    def __init__(self, llm: BaseChatModel, prompt_template: ChatPromptTemplate, **kwargs):
        super().__init__(llm=llm, **kwargs)

        assert prompt_template is not None
        self.prompt_template = prompt_template

    @classmethod
    @abstractmethod
    def create(cls, llm: BaseChatModel, prompt_template: ChatPromptTemplate, **kwargs):
        raise NotImplemented

    @property
    def llm_callable(self):
        return self.prompt_template | self.llm
