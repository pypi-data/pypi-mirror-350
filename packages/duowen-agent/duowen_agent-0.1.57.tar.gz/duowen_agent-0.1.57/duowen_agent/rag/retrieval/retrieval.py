from typing import Optional, List

import numpy as np

from duowen_agent.llm.rerank_model import GeneralRerank
from duowen_agent.rag.models import Document, SearchResult
from .base import BaseVector
from ..nlp import LexSynth
from ...llm import OpenAIEmbedding


class Retrieval:
    def __init__(
        self,
        vector: BaseVector,
        lex_synth: LexSynth,
        llm_embeddings_instance: OpenAIEmbedding,
        rerank: GeneralRerank = None,
    ):
        self.vector = vector
        self.rerank_model = rerank
        self.lex_synth = lex_synth
        self.llm_embeddings_instance = llm_embeddings_instance

    def full_text_search(
        self,
        query: str,
        top_k: int = 10,
        score_threshold: Optional[float] = 0.0,
        **kwargs
    ) -> list[SearchResult]:
        data = self.vector.full_text_search(
            query, top_k=top_k, score_threshold=score_threshold, **kwargs
        )

        if score_threshold:
            data = [i for i in data if i.token_similarity_score >= score_threshold]

        return data

    def semantic_search(
        self,
        query: str,
        top_k: int = 10,
        score_threshold: Optional[float] = 0.0,
        query_embedding: np.ndarray | List[float] = None,
        **kwargs
    ) -> list[SearchResult]:

        data = self.vector.semantic_search(
            query,
            top_k=top_k,
            score_threshold=score_threshold,
            query_embedding=query_embedding,
            **kwargs
        )

        if score_threshold:
            data = [i for i in data if i.vector_similarity_score >= score_threshold]

        return data

    def hybrid_search(
        self,
        query: str,
        top_k: int = 10,
        score_threshold: Optional[float] = 0.0,
        vector_weight: float = 0.7,
        keyword_weight: float = 0.3,
        **kwargs
    ) -> list[SearchResult]:

        query_embedding = self.llm_embeddings_instance.get_embedding(query)[0]

        full_text_data = self.full_text_search(query, top_k=top_k, **kwargs)
        semantic_data = self.semantic_search(
            query, top_k=top_k, query_embedding=query_embedding, **kwargs
        )

        _data: List[Document] = list(
            set([i.result for i in full_text_data] + [i.result for i in semantic_data])
        )

        hybrid_data = self.lex_synth.hybrid_similarity(
            question=query,
            question_vector=query_embedding,
            docs_vector=[i.vector for i in _data],
            docs_sm=[i.page_content_split for i in _data],
            tkweight=keyword_weight,
            vtweight=vector_weight,
        )

        hybrid_data_index = [(index, score) for index, score in enumerate(hybrid_data)]

        hybrid_data_index = sorted(hybrid_data_index, key=lambda x: x[1], reverse=True)[
            :top_k
        ]

        if score_threshold:
            hybrid_data_index = [
                i for i in hybrid_data_index if i[1] >= score_threshold
            ]

        return [
            SearchResult(result=_data[i[0]], rerank_similarity_score=i[1])
            for i in hybrid_data_index
        ]
