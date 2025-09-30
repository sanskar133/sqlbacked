from vectordb.elastic_search import ElasticSearchDB
from vectordb.utils import (
    create_index_name_from_user_and_connection_id,
    EmbeddingModel,
)
from pub_sub_module.manager import app
import logging

logger = logging.getLogger(__name__)


@app.task
def retrieve_es_documents(user_id, connection_id, user_query, index_name=None):
    """Task to retrieve documents from Elastic Search"""
    try:
        es_instance = ElasticSearchDB()

        if index_name is None:
            es_index_name = create_index_name_from_user_and_connection_id(
                connection_id, user_id
            )
        else:
            es_index_name = index_name

        result = es_instance.query(user_query, es_index_name, model=EmbeddingModel())

        logger.info(result)

        return result

    except Exception as e:
        print(f"Error in retrieving the documents: {str(e)}")
