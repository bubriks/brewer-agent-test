# import json
# import re

# from openai import OpenAI

# from hopsworks_brewer.server.constants import Constants


# def decide_on_redirection(chunk: str, query: str, openai_client: OpenAI) -> str:
#     system_prompt = """You will be given a list of urls and information about each route. You must decide which route to take based on the information provided. Return the URL of the route you would like to take.
#     """

#     response = openai_client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {
#                 "role": "user",
#                 "content": f"URLs: {chunk}\n\nQuery:\n{query}",
#             },
#         ],
#     )
#     return response.choices[0].message.content or ""


# def extract_url_from_chunk(chunk: str) -> str:
#     match = re.search(r"/[^\s\(\)]+", chunk)
#     return match.group(0) if match else ""


# def generate_routes(
#     query: str,
#     project_id: str,
#     fs_id: str,
# ) -> str:
#     result = (
#         "You can access the Hopsworks Web app.\n"
#         "The query you entered is: \n"
#         f"{query}\n"
#         "Here are the routes you can take:\n"
#     )

#     with open(Constants.prepared_data_path / "routes.json") as f:
#         data = json.load(f)
#     for route, desc in data.items():
#         route = route.replace(":id", project_id).replace(":fsId", fs_id)
#         result += f"{route} -- {desc}\n"
#     return result
