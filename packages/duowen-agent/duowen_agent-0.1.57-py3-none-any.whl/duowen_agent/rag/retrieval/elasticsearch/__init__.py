import logging
from typing import List, Dict, Any, Union

import numpy as np
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from duowen_agent.llm import OpenAIEmbedding
from duowen_agent.rag.models import Document, SearchResult
from .mapping import metadata_mapping
from ..base import BaseVector
from ...nlp import LexSynth


class ElasticsearchVector(BaseVector):
    def __init__(
        self,
        llm_embeddings_instance: OpenAIEmbedding,
        lex_synth: LexSynth,
        es: Elasticsearch,
        collection_name: Union[str, None] = None,
    ):
        self.collection_name = collection_name or "duowen_agent_collection"
        self.llm_embeddings_instance = llm_embeddings_instance
        self.lex_synth = lex_synth
        self._client = es
        self.create_collection()

    def create_collection(self) -> bool:
        if not self._client.indices.exists(index=self.collection_name):
            self._client.indices.create(
                index=self.collection_name, body=metadata_mapping
            )
            logging.info(f"Elasticsearch 创建集合 {self.collection_name} 成功")
        return True

    def get_backend_type(self) -> str:
        info = self._client.info()
        return f'Elasticsearch version:{info["version"]["number"]}'

    def pretreated(self, document: Document) -> Document:

        if not document.page_content_split:
            document.page_content_split = self.lex_synth.content_cut(
                document.page_content
            )

        if not document.page_content_sm_split:
            document.page_content_split = self.lex_synth.content_sm_cut(
                document.page_content
            )

        if document.title and not document.title_split:
            document.title_split = self.lex_synth.content_cut(document.title)

        if document.title and not document.title_sm_split:
            document.title_sm_split = self.lex_synth.content_sm_cut(document.title)

        if document.important_keyword and not document.important_keyword_split:
            document.important_keyword_split = self.lex_synth.content_cut(
                " ".join([i for i in document.important_keyword])
            )

        if document.question and not document.question_split:
            document.question_split = self.lex_synth.content_cut(
                " ".join([i for i in document.question])
            )

        return document

    def text_exists(self, id: str) -> bool:
        return bool(self._client.exists(index=self.collection_name, id=id))

    def refresh(self):
        """手动刷新索引"""
        self._client.indices.refresh(index=self.collection_name)

    def add_document(self, document: Document, **kwargs) -> str:

        if not document.vector:
            document.vector = self.llm_embeddings_instance.get_embedding(
                document.vector_content or document.page_content
            )[0]

        document = self.pretreated(document)

        vector_data = document.model_dump()

        vector_data[f"vector_{self.llm_embeddings_instance.dimension}"] = (
            document.vector
        )
        del vector_data["vector"]

        if self.text_exists(document.id):
            self._client.update(
                index=self.collection_name,
                id=self.collection_name,
                body={"doc": vector_data},
            )
            logging.info(f"更新ES数据成功，ID: {document.id}")
        else:
            self._client.index(
                index=self.collection_name, id=document.id, body=vector_data
            )
            logging.info(f"插入ES数据成功，ID: {document.id}")

        return vector_data.get("id", "")

    def batch_add_document(
        self, documents: list[Document], batch_num: int = 100, **kwargs: Any
    ) -> None:

        if not documents[0].vector:
            _data = [i.vector_content or i.page_content for i in documents]
            _vdata = self.llm_embeddings_instance.get_embedding(_data)
            for i, v in enumerate(_vdata):
                documents[i].vector = v

        documents = [self.pretreated(i) for i in documents]

        _vector_datas = [i.model_dump() for i in documents]

        for i in _vector_datas:
            i[f"vector_{self.llm_embeddings_instance.dimension}"] = i["vector"]
            del i["vector"]

        actions = []
        for vector_data in _vector_datas:
            actions.append(
                {
                    "_index": self.collection_name,
                    "_id": vector_data["id"],
                    "_source": vector_data,
                }
            )

            if len(actions) >= batch_num:
                bulk(self._client, actions)
                actions = []

        if actions:
            bulk(self._client, actions)

        self.refresh()

    def get_documents_by_ids(self, ids: list[str], **kwargs: Any) -> List[Document]:
        if not ids:
            return []
        query_body = {"query": {"bool": {"filter": [{"terms": {"id": ids}}]}}}
        vector_field = f"vector_{self.llm_embeddings_instance.dimension}"
        response = self._client.search(index=self.collection_name, body=query_body)
        docs = []
        for hit in response["hits"]["hits"]:
            _data = hit["_source"]
            _data["vector"] = _data[vector_field]
            docs.append(Document(**_data))
        return docs

    def delete_documents_by_ids(self, ids: list[str], **kwargs: Any):
        try:
            for _id in ids:
                self._client.delete(index=self.collection_name, id=_id)
                logging.info(f"删除ES数据成功，ID: {_id}")
        except Exception as e:
            logging.error(f"删除ES数据时发生错误: {e}")
            raise

    def delete_collection(self) -> None:
        self._client.indices.delete(index=self.collection_name)
        logging.info(f"删除集合 {self.collection_name} 成功")

    def semantic_search(
        self,
        query: str,
        query_embedding: np.ndarray | List[float] = None,
        top_k=5,
        filter: List[Dict[str, Any]] = None,
        score_threshold=None,
        **kwargs,
    ) -> list[SearchResult]:
        try:
            if not query:
                raise ValueError("query 不能为空")
            if filter and not isinstance(filter, list):
                raise ValueError("参数 'filter' 必须是一个列表")

            if query_embedding:
                query_vector = query_embedding
            else:
                query_vector = self.llm_embeddings_instance.get_embedding(query)[0]

            field = f"vector_{self.llm_embeddings_instance.dimension}"
            _query = {
                "query": {
                    "script_score": {
                        "query": {"match_all": {}},
                        "script": {
                            "source": f"cosineSimilarity(params.query_vector, '{field}')",
                            "params": {"query_vector": query_vector},
                        },
                    }
                }
            }
            query_body = {"query": {"bool": {"must": [_query["query"]], "filter": []}}}

            if score_threshold:
                query_body["min_score"] = score_threshold

            if top_k:
                query_body["size"] = top_k

            if filter:
                query_body["query"]["bool"]["filter"] = filter

            if top_k == 0:
                query_body["track_total_hits"] = True
                query_body["size"] = 0

            response = self._client.search(index=self.collection_name, body=query_body)

            logging.info(f"向量召回条数: {len(response['hits']['hits'])}")

            vector_field = f"vector_{self.llm_embeddings_instance.dimension}"

            docs = []
            for idx, hit in enumerate(response["hits"]["hits"]):
                _data = hit["_source"]
                _data["vector"] = _data[vector_field]
                docs.append(
                    SearchResult(
                        result=Document(**_data),
                        vector_similarity_score=hit["_score"],
                    )
                )

        except ValueError as ve:
            logging.error(f"参数校验失败: {ve}")
            raise
        except Exception as e:
            logging.error(f"向量检索时发生错误: {e}")
            raise

        return sorted(docs, key=lambda doc: doc.vector_similarity_score, reverse=True)

    def full_text_search(
        self,
        query: str,
        top_k=5,
        filter: List[Dict[str, Any]] = None,
        score_threshold=None,
        **kwargs,
    ) -> list[SearchResult]:
        try:
            if filter and not isinstance(filter, list):
                raise ValueError("参数 'filter' 必须是一个列表")

            query_body = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "query_string": {
                                    "query": self.lex_synth.term_weight(query),
                                    "fields": [
                                        "title_split^10",
                                        "title_sm_split^5",
                                        "important_keyword^30",
                                        "important_sm_keyword^20",
                                        "question_split^20",
                                        "content_split^2",
                                        "content_sm_split",
                                    ],
                                    "type": "best_fields",
                                }
                            }
                        ],
                        "filter": [],
                    }
                }
            }

            if top_k:
                query_body["size"] = top_k

            if filter:
                query_body["query"]["bool"]["filter"] = filter

            if top_k == 0:
                query_body["track_total_hits"] = True
                query_body["size"] = 0

            logging.debug(f"查询body：{query_body}")
            response = self._client.search(index=self.collection_name, body=query_body)
            logging.debug(f"全文召回条数: {len(response['hits']['hits'])}")

            vector_field = f"vector_{self.llm_embeddings_instance.dimension}"

            docs = []
            for idx, hit in enumerate(response["hits"]["hits"]):
                _data = hit["_source"]
                _data["vector"] = _data[vector_field]
                docs.append(
                    SearchResult(
                        result=Document(**_data), token_similarity_score=hit["_score"]
                    )
                )

        except ValueError as ve:
            logging.error(f"参数校验失败: {ve}")
            raise
        except Exception as e:
            logging.error(f"全文检索时发生错误: {e}")
            raise

        return sorted(docs, key=lambda doc: doc.token_similarity_score, reverse=True)
