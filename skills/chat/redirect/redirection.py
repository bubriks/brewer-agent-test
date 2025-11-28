# from collections.abc import AsyncGenerator
# from typing import Any

# from langchain_core.runnables import RunnableConfig
# from langchain_core.tools import StructuredTool
# from langchain_core.tools.base import ArgsSchema
# from langgraph.graph import END
# from langgraph.types import Command
# from openai import OpenAI
# from pydantic import BaseModel, Field

# from hopsworks_brewer.events import Event, RedirectEvent, TextEvent
# from hopsworks_brewer.utils.redirection_utils import (
#     decide_on_redirection,
#     extract_url_from_chunk,
# )
# from hopsworks_brewer.utils.tools_utils import hopsworks_ui_info


# class RedirectionInput(BaseModel):
#     query: str = Field(
#         description="The query to redirect the user to a specific page.",
#         title="Query",
#     )


# class Tool(StructuredTool):
#     name: str = "redirection"
#     description: str = """
#         This tool is used to redirect the user to a specific page based on their query.
#         The input of this function should be a query, which is a string that represents the user's question or query.
#         The output will be a string that contains the URL of the page that the user should be redirected to.
#         When you use this tool you MUST return just the URL that the tool gave you.
#         Do not worry about the formatting of the URL, the system will take care of that, the URLs will follow this format: /path/to/page.

#         For example:
#         - Redirect to the page where I can change my API keys.
#         - Redirect to the page where I can find the list of feature groups.
#         - Redirect to the page where I can access the project overview.
#         """

#     args_schema: ArgsSchema = RedirectionInput
#     return_direct: bool = True

#     async def astream(  # type: ignore[override]
#         self,
#         input: dict,
#         config: RunnableConfig | None = None,
#         **kwargs: Any | None,
#     ) -> AsyncGenerator[Event | Command, None]:
#         openai_client = OpenAI()

#         url = decide_on_redirection(
#             chunk=hopsworks_ui_info(input["query"]),
#             query=input["query"],
#             openai_client=openai_client,
#         )
#         url = extract_url_from_chunk(url)
#         yield TextEvent("I am redirecting you to " + url + " ...")
#         yield RedirectEvent(destination=url)
#         yield Command(update={"tool_caller": "", "tool_answers": []}, goto=END)


# tool = Tool()
