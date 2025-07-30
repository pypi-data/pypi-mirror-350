from abc import ABC, abstractmethod
from typing import List

import numpy as np

from ..models import Document, SearchResult


class BaseVector(ABC):

    @abstractmethod
    def get_backend_type(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def semantic_search(
        self, query: str, query_embedding: np.ndarray | List[float] = None, **kwargs
    ) -> list[SearchResult]:
        raise NotImplementedError

    @abstractmethod
    def full_text_search(self, query: str, **kwargs) -> list[SearchResult]:
        raise NotImplementedError

    @abstractmethod
    def add_document(self, document: Document, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def batch_add_document(self, documents: list[Document], batch_num: int, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_documents_by_ids(self, ids: list[str], **kwargs) -> list[Document]:
        raise NotImplementedError

    @abstractmethod
    def delete_documents_by_ids(self, ids: list[str], **kwargs):
        raise NotImplementedError
