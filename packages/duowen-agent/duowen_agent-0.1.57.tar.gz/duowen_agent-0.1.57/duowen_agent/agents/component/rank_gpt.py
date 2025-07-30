from typing import List

from duowen_agent.llm.chat_model import OpenAIChat
from duowen_agent.llm.tokenizer import tokenizer
from .base import BaseComponent


class Ranker(BaseComponent):
    """通过语言模型实现 rerank能力 不支持分值，只能排序"""

    # query: str, documents
    def __init__(self, llm: OpenAIChat):
        self.llm = llm
        self.content_tokens_limit = None
        self.documents = None
        self.question_tokens = None
        self.prompt_tokens = 1000
        self.rank_limit = 5
        self.query = None

    def init_data(self, query: str, documents: List[str], rank_limit=5):
        self.query = query
        self.rank_limit = rank_limit
        self.question_tokens = tokenizer.chat_len(query)
        self.documents = documents
        self.content_tokens_limit = (
            self.llm.token_limit - self.prompt_tokens - self.question_tokens
        )

    def cut_passages(self):
        _content_tokens = self.content_tokens_limit
        _passages = []
        for _chunk in self.documents:
            _curr_token = tokenizer.chat_len(_chunk)
            _content_tokens = _content_tokens - _curr_token
            if _content_tokens > 0:
                _passages.append(_chunk)
            else:
                break
        self.documents = _passages

    def chk_passages_tokens_limit(self):
        if tokenizer.chat_len("".join(self.documents)) > self.content_tokens_limit:
            return False
        else:
            return True

    def get_prefix_prompt(self, num):
        return [
            {
                "role": "system",
                "content": "You are RankGPT, an intelligent assistant that can rank passages based on their relevancy to the query.",
            },
            {
                "role": "user",
                "content": f"I will provide you with {num} passages, each indicated by number identifier []. \nRank the passages based on their relevance to query: {self.query}.",
            },
            {"role": "assistant", "content": "Okay, please provide the passages."},
        ]

    def get_post_prompt(self, num):
        return f"Search Query: {self.query}. \nRank the {num} passages above based on their relevance to the search query. The passages should be listed in descending order using identifiers. The most relevant passages should be listed first. The output format should be [] > [], e.g., [1] > [2]. Only response the ranking results, do not say any word or explain."

    def create_permutation_instruction(self):
        if not self.chk_passages_tokens_limit():
            raise ValueError(
                f"Agent Ranker token passages overly long, model tokens limit number {self.llm.token_limit}."
            )
        num = len(self.documents)
        messages = self.get_prefix_prompt(num)
        rank = 0
        for hit in self.documents:
            rank += 1
            content = hit
            content = content.replace("Title: Content: ", "")
            content = content.strip()
            messages.append({"role": "user", "content": f"[{rank}] {content}"})
            messages.append(
                {"role": "assistant", "content": f"Received passage [{rank}]."}
            )
        messages.append({"role": "user", "content": self.get_post_prompt(num)})
        return messages

    def run_llm(self, messages):
        response = self.llm.chat(messages=messages, temperature=0)
        return response

    async def arun_llm(self, messages):
        response = await self.llm.achat(messages=messages, temperature=0)
        return response

    @staticmethod
    def clean_response(response: str):
        new_response = ""
        for c in response:
            if not c.isdigit():
                new_response += " "
            else:
                new_response += c
        new_response = new_response.strip()
        return new_response

    @staticmethod
    def remove_duplicate(response):
        new_response = []
        for c in response:
            if c not in new_response:
                new_response.append(c)
        return new_response

    def receive_permutation(self, permutation):
        _passages = []
        response = self.clean_response(permutation)
        response = [int(x) - 1 for x in response.split()]
        response = self.remove_duplicate(response)
        original_rank = [tt for tt in range(len(self.documents))]
        response = [ss for ss in response if ss in original_rank]
        response = response + [tt for tt in original_rank if tt not in response]
        for x in response[: self.rank_limit]:
            _passages.append(self.documents[x])
        return _passages

    def run(self, query: str, documents: List[str], rank_limit=5) -> List[str]:
        self.init_data(query, documents, rank_limit)
        if self.rank_limit < len(self.documents):
            messages = self.create_permutation_instruction()
            permutation = self.run_llm(messages)
            item = self.receive_permutation(permutation)
            return item
        else:
            return self.documents

    async def arun(self, query: str, documents: List[str], rank_limit=5) -> List[str]:
        self.init_data(query, documents, rank_limit)
        if self.rank_limit < len(self.documents):
            messages = self.create_permutation_instruction()
            permutation = await self.arun_llm(messages)
            item = self.receive_permutation(permutation)
            return item
        else:
            return self.documents
