# 多闻(duowen)语言模型工具包

LLM核心开发包

## 模型

### 语言模型

#### 指令模型

```python
from duowen_agent.llm import OpenAIChat
from os import getenv

llm_cfg = {"model": "THUDM/glm-4-9b-chat", "base_url": "https://api.siliconflow.cn/v1",
           "api_key": getenv("SILICONFLOW_API_KEY")}

_llm = OpenAIChat(**llm_cfg)

print(_llm.chat('''If you are here, please only reply "1".'''))

for i in _llm.chat_for_stream('''If you are here, please only reply "1".'''):
    print(i)

```

#### 推理模型

```python
from duowen_agent.llm import OpenAIChat
from os import getenv
from duowen_agent.utils.core_utils import separate_reasoning_and_response

llm_cfg_reasoning = {
    "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    "base_url": "https://api.siliconflow.cn/v1",
    "api_key": getenv("SILICONFLOW_API_KEY"),
    "is_reasoning": True,
}

_llm = OpenAIChat(**llm_cfg_reasoning)

content = _llm.chat('9.9比9.11哪个大?')

print(separate_reasoning_and_response(content))
```

### 嵌入模型

#### 调用

```python
from duowen_agent.llm import OpenAIEmbedding
from os import getenv

emb_cfg = {"model": "BAAI/bge-large-zh-v1.5", "base_url": "https://api.siliconflow.cn/v1",
           "api_key": getenv("SILICONFLOW_API_KEY")}

_emb = OpenAIEmbedding(**emb_cfg)
print(_emb.get_embedding('123'))
print(_emb.get_embedding(['123', '456']))
```

#### 缓存

```python
from duowen_agent.llm import OpenAIEmbedding, EmbeddingCache
from os import getenv
from duowen_agent.utils.cache import Cache
from redis import StrictRedis
from typing import List, Optional, Any

emb_cfg = {"model": "BAAI/bge-large-zh-v1.5", "base_url": "https://api.siliconflow.cn/v1",
           "api_key": getenv("SILICONFLOW_API_KEY")}

_emb = OpenAIEmbedding(**emb_cfg)

redis = StrictRedis(host='127.0.0.1', port=6379)


class RedisCache(Cache):
    # 基于Cache 接口类实现  redis缓存
    def __init__(self, redis_cli: StrictRedis):
        self.redis_cli = redis_cli
        super().__init__()

    def set(self, key, value, expire=60):
        return self.redis_cli.set(key, value, ex=expire)

    def mget(self, keys: List[str]) -> List[Optional[Any]]:
        return self.redis_cli.mget(keys)

    def get(self, key: str) -> Optional[Any]:
        return self.redis_cli.get(key)

    def delete(self, key: str):
        return self.redis_cli.delete(key)

    def exists(self, key: str) -> bool:
        return self.redis_cli.exists(key)

    def clear(self):
        raise InterruptedError("不支持")


embedding_cache = EmbeddingCache(RedisCache(redis), _emb)
print(embedding_cache.get_embedding('hello world'))
for i in embedding_cache.get_embedding(['sadfasf', 'hello world']):
    print(i)
```

## 图文向量

### 调用

```python
from duowen_agent.llm.embedding_vl_model import JinaClipV2Embedding, EmbeddingVLCache
from duowen_agent.utils.cache import InMemoryCache
from os import getenv

embedding_vl_model = JinaClipV2Embedding(
    base_url='http://127.0.0.1:8000',
    model_name='jina-clip-v2',
    api_key=getenv('JINA_API_KEY'),
    dimension=512
)
input = [{'text': 'aaa'}, {'text': 'bbb'}, {'text': 'ccc'},
         {'image': 'http://dingyue.ws.126.net/2025/0214/59c194dbj00srny17000md000f0008fp.jpg'}]
embedding_data = embedding_vl_model.get_embedding(input)
```

### 缓存调用

```python
from duowen_agent.llm.embedding_vl_model import JinaClipV2Embedding, EmbeddingVLCache
from duowen_agent.utils.cache import InMemoryCache
from os import getenv

embedding_vl_model = JinaClipV2Embedding(
    base_url='http://127.0.0.1:8000',
    model_name='jina-clip-v2',
    api_key=getenv('JINA_API_KEY'),
    dimension=512
)

embedding_vl_model_cache = EmbeddingVLCache(InMemoryCache(), embedding_vl_model)
input = [{'text': 'aaa'}, {'text': 'bbb'}, {'text': 'ccc'},
         {'image': 'http://dingyue.ws.126.net/2025/0214/59c194dbj00srny17000md000f0008fp.jpg'}]
embedding_data = embedding_vl_model_cache.get_embedding(input)
```

## 重排

```python
from duowen_agent.llm import GeneralRerank
from os import getenv
import tiktoken

rerank_cfg = {
    "model": "BAAI/bge-reranker-v2-m3",
    "base_url": "https://api.siliconflow.cn/v1/rerank",
    "api_key": getenv("SILICONFLOW_API_KEY")}

rerank = GeneralRerank(
    model=rerank_cfg["model"],
    api_key=rerank_cfg["api_key"],
    base_url=rerank_cfg["base_url"],
    encoding=tiktoken.get_encoding("o200k_base")
)

data = rerank.rerank(query='Apple', documents=["苹果", "香蕉", "水果", "蔬菜"], top_n=3)
for i in data:
    print(i)
```

## Rag

### 文本切割

#### token切割

> 根据标记（如单词、子词）将文本分割成块，通常用于处理语言模型的输入。

```python
from duowen_agent.rag.splitter import TokenChunker

txt = '...'
for i in TokenChunker().chunk(txt):
    print(i)
```

#### 分隔符切割

> 根据指定的分隔符（如换行符）将文本分割。

```python
from duowen_agent.rag.splitter import SeparatorChunker

txt = '...'
for i in SeparatorChunker(separator="\n\n").chunk(txt):
    print(i)
```

#### 递归切割

> 递归地尝试不同的分隔符（如换行符、句号、逗号等）来分割文本，直到每个块的大小符合要求。

```python
from duowen_agent.rag.splitter import RecursiveChunker

txt = '...'
for i in RecursiveChunker(splitter_breaks=("。", "？", "！", ".", "?", "!")).chunk(txt):
    print(i)
```

#### 语义切割 (依赖向量模型)

> 通过计算句子之间的语义相似性来确定分割点，从而将文本分割成语义上有意义的块。这种方法在处理需要语义连贯性的任务时非常有用，尤其是在需要将文本分割成适合模型处理的小块时。

```python
from duowen_agent.llm import OpenAIEmbedding
from duowen_agent.rag.splitter import SemanticChunker
from os import getenv

emb_cfg = {"model": "BAAI/bge-large-zh-v1.5", "base_url": "https://api.siliconflow.cn/v1",
           "api_key": getenv("SILICONFLOW_API_KEY")}

_emb = OpenAIEmbedding(**emb_cfg)
txt = '...'
for i in SemanticChunker(llm_embeddings_instance=_emb).chunk(txt):
    print(i)
```

#### markdown切割

> 通过识别 Markdown 文档中的标题将文档分割成基于标题的章节，并进一步将这些章节合并成大小可控的块。

```python
from duowen_agent.rag.splitter import MarkdownHeaderChunker

txt = '...'
for i in MarkdownHeaderChunker().chunk(txt):
    print(i)
```

#### 语言模型切割 (依赖语言模型)

> 通过调用大语言模型将文档分割成基于主题的章节，并进一步将这些章节分割成大小可控的块。质量高，效率较差，对需要切割的文本长度依赖模型max_token大小。

```python
from duowen_agent.llm import OpenAIChat
from duowen_agent.rag.splitter import SectionsChunker
from os import getenv

llm_cfg = {"model": "THUDM/glm-4-9b-chat", "base_url": "https://api.siliconflow.cn/v1",
           "api_key": getenv("SILICONFLOW_API_KEY")}

_llm = OpenAIChat(**llm_cfg)
txt = '...'
for i in SectionsChunker(llm_instance=_llm).chunk(txt):
    print(i)

```

#### 元数据嵌入切割 (依赖语言模型)

> 通过将文档分割成基于标题的章节，并进一步将章节分割成大小可控的块，同时为每个块添加上下文信息，从而增强块的语义信息。

```python
from duowen_agent.llm import OpenAIChat
from duowen_agent.rag.splitter import MetaChunker
from os import getenv

llm_cfg = {"model": "THUDM/glm-4-9b-chat", "base_url": "https://api.siliconflow.cn/v1",
           "api_key": getenv("SILICONFLOW_API_KEY")}

_llm = OpenAIChat(**llm_cfg)
txt = '...'
for i in MetaChunker(llm_instance=_llm).chunk(txt):
    print(i)
```

#### 快速混合切割

> 实现方案
> 1. markdown切割
> 2. 换行符切割(\n)
> 3. 递归切割(。？！.?!)
> 4. token切割（chunk_overlap 生效）

```python
from duowen_agent.rag.splitter import FastMixinChunker

txt = '...'
for i in FastMixinChunker().chunk(txt):
    print(i)
```
