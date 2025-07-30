metadata_mapping = {
    "settings": {
        "index": {
            "number_of_shards": 2,  # 50GB总数据，单分片约17GB（10-50GB范围内） 根据数据量（10-50GB / 分片）和节点资源设置，避免过多或过少
            "number_of_replicas": 1,  # 3节点集群，1副本保证高可用（副本分布在另外2节点）
            "refresh_interval": "1s",  # 平衡实时性（5秒内可搜索）和写入性能,写负载高时调大（如 30s），实时性要求高时保持小（如 1-5s）
        },
        "similarity": {
            "scripted_sim": {
                "type": "scripted",
                "script": {
                    "source": "double idf = Math.log(1+(field.docCount-term.docFreq+0.5)/(term.docFreq + 0.5))/Math.log(1+((field.docCount-0.5)/1.5)); return query.boost * idf * Math.min(doc.freq, 1);"
                },
            }
        },
    },
    "mappings": {
        "properties": {
            "id": {"type": "keyword", "store": "true"},
            "page_content": {
                "type": "text",
                "index": "true",
                "store": "true",
            },
            "vector_content": {
                "type": "text",
                "index": "true",
                "store": "true",
            },
            "kb_id": {  # 知识库 ['xxxx'， 'xxxxxx']
                "type": "keyword",
                "store": "true",
                "index": "true",
            },
            "label": {  # 标签  ['xxx', 'xxx']
                "type": "keyword",
                "store": "true",
                "index": "true",
            },
            "slots": {"type": "keyword", "store": "true", "index": "true"},
            "page_content_split": {
                "type": "text",
                "analyzer": "whitespace",
                "store": "true",
            },
            "page_content_sm_split": {
                "type": "text",
                "similarity": "scripted_sim",
                "analyzer": "whitespace",
                "store": "true",
            },
            "file_id": {"type": "text", "store": "true", "index": "true"},
            "title": {"type": "text", "store": "true", "index": "true"},
            "title_split": {
                "type": "text",
                "similarity": "scripted_sim",
                "analyzer": "whitespace",
                "store": "true",
            },
            "title_sm_split": {
                "type": "text",
                "similarity": "scripted_sim",
                "analyzer": "whitespace",
                "store": "true",
            },
            "important_keyword": {
                "type": "text",
                "similarity": "scripted_sim",
                "analyzer": "whitespace",
                "store": "true",
            },
            "important_keyword_split": {
                "type": "text",
                "similarity": "scripted_sim",
                "analyzer": "whitespace",
                "store": "true",
            },
            "create_time": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||yyyy-MM-dd_HH:mm:ss",
                "store": "true",
            },
            "question": {"type": "keyword", "store": "true", "index": "true"},
            "question_split": {
                "type": "text",
                "similarity": "scripted_sim",
                "analyzer": "whitespace",
                "store": "true",
            },
            "authors": {"type": "keyword", "store": "true", "index": "true"},
            "institution": {"type": "keyword", "store": "true", "index": "true"},
            "abstract": {"type": "text", "index": "true", "store": "true"},  # 文档摘要
            "chunk_index": {  # 切片index
                "type": "integer",
                "index": "true",
                "store": "true",
            },
            "metadata": {
                "type": "object",
                "properties": {},
                "dynamic": "true",
                "enabled": "true",
            },
            "vector_128": {
                "type": "dense_vector",
                "dims": 128,
                "index": "true",
                "similarity": "cosine",
            },
            "vector_256": {
                "type": "dense_vector",
                "dims": 256,
                "index": "true",
                "similarity": "cosine",
            },
            "vector_384": {
                "type": "dense_vector",
                "dims": 384,
                "index": "true",
                "similarity": "cosine",
            },
            "vector_512": {
                "type": "dense_vector",
                "dims": 512,
                "index": "true",
                "similarity": "cosine",
            },
            "vector_768": {
                "type": "dense_vector",
                "dims": 768,
                "index": "true",
                "similarity": "cosine",
            },
            "vector_1024": {
                "type": "dense_vector",
                "dims": 1024,
                "index": "true",
                "similarity": "cosine",
            },
            "vector_1536": {
                "type": "dense_vector",
                "dims": 1536,
                "index": "true",
                "similarity": "cosine",
            },
        },
        "date_detection": "true",
        "dynamic_templates": [
            {
                "metadata_int": {
                    "path_match": "metadata.*_int",
                    "match_mapping_type": "long",
                    "mapping": {"type": "integer", "store": "true"},
                }
            },
            {
                "metadata_ulong": {
                    "path_match": "metadata.*_ulong",
                    "match_mapping_type": "long",
                    "mapping": {"type": "unsigned_long", "store": "true"},
                }
            },
            {
                "metadata_long": {
                    "path_match": "metadata.*_long",
                    "match_mapping_type": "long",
                    "mapping": {"type": "long", "store": "true"},
                }
            },
            {
                "metadata_short": {
                    "path_match": "metadata.*_short",
                    "match_mapping_type": "long",
                    "mapping": {"type": "short", "store": "true"},
                }
            },
            {
                "metadata_numeric": {
                    "path_match": "metadata.*_flt",
                    "match_mapping_type": "double",
                    "mapping": {"type": "float", "store": "true"},
                }
            },
            {
                "metadata_kwd": {
                    "match_pattern": "regex",
                    "path_match": "^metadata\\..*(_kwd|id|uid)$",
                    "match_mapping_type": "string",
                    "mapping": {
                        "type": "keyword",
                        "similarity": "boolean",
                        "store": "true",
                    },
                }
            },
            {
                "metadata_dt": {
                    "match_pattern": "regex",
                    "path_match": "^metadata\\..*_(at|dt|time|date)$",
                    "match_mapping_type": "string",
                    "mapping": {
                        "type": "date",
                        "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||yyyy-MM-dd_HH:mm:ss",
                        "store": "true",
                    },
                }
            },
            {
                "metadata_nested": {
                    "path_match": "metadata.*_nst",
                    "match_mapping_type": "object",
                    "mapping": {"type": "nested"},
                }
            },
            {
                "metadata_object": {
                    "path_match": "metadata.*_obj",
                    "match_mapping_type": "object",
                    "mapping": {"type": "object", "dynamic": "true"},
                }
            },
            {
                "metadata_string": {
                    "path_match": "metadata.*_str",
                    "match_mapping_type": "string",
                    "mapping": {"type": "text", "index": "false", "store": "true"},
                }
            },
        ],
    },
}
