from abc import ABC, abstractmethod
from collections import deque
from typing import Union, Any

from duowen_agent.llm.chat_model import OpenAIChat
from duowen_agent.llm.embedding_model import OpenAIEmbedding, EmbeddingCache
from duowen_agent.llm.rerank_model import GeneralRerank
from duowen_agent.rag.retrieval.retrieval import Retrieval


class BaseAgent(ABC):

    def __init__(
        self,
        llm: OpenAIChat = None,
        retrieval_instance: Retrieval = None,
        embedding_instance: Union[EmbeddingCache, OpenAIEmbedding] = None,
        rerank_model: GeneralRerank = None,
        callback: deque = None,
        **kwargs,
    ):
        self.llm = llm
        self.retrieval_instance = retrieval_instance
        self.embedding_instance = embedding_instance
        self.rerank_model = rerank_model
        self.callback = callback
        self.kwargs = kwargs

    def put_callback(self, item):
        if self.callback:
            self.callback.append(item)

    @abstractmethod
    def _run(self, instruction: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def run(
        self,
        instruction: str,
        *args,
        **kwargs,
    ) -> Any:
        result: str = self._run(instruction, *args, **kwargs)
        return result
