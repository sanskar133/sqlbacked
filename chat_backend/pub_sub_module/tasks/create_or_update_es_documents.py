from vectordb.elastic_search import ElasticSearchDB
from vectordb.utils import (
    create_index_name_from_user_and_connection_id,
    EmbeddingModel,
)
from pub_sub_module.manager import app


@app.task
def create_or_update_es_documents(document, user_id, connection_id):
    """Task to create or update a document in ELastic Search"""
    try:
        es_instance = ElasticSearchDB()
        es_index_name = create_index_name_from_user_and_connection_id(
            connection_id, user_id
        )
        es_instance.create_or_update_documents(
            document, es_index_name, model=EmbeddingModel()
        )

    except Exception as e:
        print(f"Error in create_or_update_es_documents: {str(e)}")
        return f"Task failed with exception: {str(e)}"
