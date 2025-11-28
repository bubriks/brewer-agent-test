# import h5py
# import orjson
# from langchain_core.tools import StructuredTool
# from openai import OpenAI
# from opensearchpy import OpenSearch
# from opensearchpy.helpers import bulk

# from hopsworks_brewer.server.constants import Constants
# from hopsworks_brewer.session import Session
# from hopsworks_brewer.utils.rag_utils import (
#     get_docs_index_dimensions,
#     get_docs_index_name,
#     get_embedding,
# )


# def hit_to_str(hit) -> str:
#     return f"Title: {hit['title']}\nURL: {hit['url']}\nContent:\n{hit['content']}"


# def create_index(client, index_name):
#     index_body = {
#         "settings": {
#             "knn": True,
#             "knn.algo_param.ef_search": 100,
#         },
#         "mappings": {
#             "properties": {
#                 "vector_embeddings": {
#                     "type": "knn_vector",
#                     "dimension": get_docs_index_dimensions(),
#                 },
#                 "content": {
#                     "type": "text",
#                 },
#                 "title": {
#                     "type": "text",
#                 },
#                 "summary": {
#                     "type": "text",
#                 },
#                 "url": {
#                     "type": "text",
#                 },
#             }
#         },
#     }
#     return client.indices.create(index=index_name, body=index_body)


# def retrieve_documentation(query: str) -> str:
#     """This is the documentation tool. The objetive of this tool is to search for documentation in the Hopsworks documentation. The input of this function should be a query, which is a string that represents the user's question or query. The output will be the page of the documentation that best matches the query.

#     For example:
#     - How to create a feature store in Hopsworks?
#     - How to create a project in Hopsworks?
#     - How to deploy a model in Hopsworks?
#     """
#     size = 5  # Number of results to return

#     project = Session().project
#     opensearch_api = project.get_opensearch_api()
#     client = OpenSearch(**opensearch_api.get_default_py_config())
#     # It would be nice to have it in a cluster-wide index, created during deployment of the cluster, but for now we use a project index
#     index = opensearch_api.get_project_index(get_docs_index_name())
#     if not client.indices.exists(index):
#         create_index(client, index)
#         docs = Constants.prepared_data_path / "docs"
#         embeddings = docs / "embeddings"
#         with open(docs / "docs.json", "rb") as json:
#             docslist = orjson.loads(json.read())
#         actions = []
#         for i, doc in enumerate(docslist):
#             with h5py.File(embeddings / f"{i}.h5", "r") as f:
#                 ds = f["embedding"]
#                 if not isinstance(ds, h5py.Dataset):
#                     raise Exception("Error getting embedding")
#                 embedding = ds[:]
#             actions.append(
#                 {
#                     "_index": index,
#                     "_id": doc["url"],
#                     "_source": doc | {"vector_embeddings": embedding},
#                 }
#             )
#         bulk(client, actions)

#     openai = OpenAI()

#     embedding = get_embedding(query, openai) or [0] * get_docs_index_dimensions()

#     request = {
#         "query": {"knn": {"vector_embeddings": {"vector": embedding, "k": size}}}
#     }
#     response = client.search(index=index, body=request, params={"size": size})

#     return "\n\n".join([hit_to_str(hit["_source"]) for hit in response["hits"]["hits"]])


# tool = StructuredTool.from_function(retrieve_documentation)
