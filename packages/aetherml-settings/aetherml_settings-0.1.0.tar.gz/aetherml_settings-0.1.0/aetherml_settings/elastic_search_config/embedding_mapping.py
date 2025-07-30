"""
Config for the ElasticSearchEmbeddingMapper.
"""

class ESEmbeddingMapperConfigIndex:

    ELASTIC_PROPERTY_EMBEDDING_MAPPING = {
        "index_name": "property_embeddings",
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "description": {"type": "text"},
                "text": {"type": "text"},
                "vector": {
                    "type": "dense_vector",
                    "dims": 768,  # 768 is the dimension of the embedding model used
                    "index": True,
                    "similarity": "cosine"
                },
                "keywords": {"type": "keyword"},
                "timestamp": {"type": "date"}
            }
        }
    }