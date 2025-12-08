# from typing import Annotated

# from langchain_core.tools import StructuredTool
# from langgraph.prebuilt import InjectedState

# from hopsworks_brewer.state import State
# from hopsworks_brewer.utils.tools_utils import hopsworks_ui_info


# def get_ui_info(query: str, state: Annotated[State, InjectedState]) -> str:
#     """This is the ui awareness tool. The objetive of this tool is to give information to the users about the Hopsworks website. The input of this function should be a query, which is a string that represents the user's question or query. The output will show information about the Hopsworks website.

#     For example:
#     - What can I do in this website?
#     - What is the purpose of this website?
#     - How can I change my API keys?
#     - How can I find the list of feature groups?
#     - How can I access the project overview?
#     """

#     origin = state.origin
#     response = f"This is the origin url where the user is: {origin}\n"
#     response += hopsworks_ui_info(query)
#     return response


# tool = StructuredTool.from_function(get_ui_info)
