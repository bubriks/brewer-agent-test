# import traceback
# from collections.abc import AsyncGenerator
# from pathlib import Path

# from hopsworks_brewer.events import Event, FileEvent, LogEvent, StepEvent, TextEvent
# from hopsworks_brewer.utils.execution_utils import (
#     execute_python_script,
#     install_requirements,
#     simple_execute_python_script,
# )
# from hopsworks_brewer.utils.file_utils import save_python_code
# from hopsworks_brewer.utils.parser_utils import parse_and_save


# class StageResult:
#     def __init__(self, stage_context, stage_code) -> None:
#         self.stage_context = stage_context
#         self.stage_code = stage_code

#     def __eq__(self, other):
#         if not isinstance(other, StageResult):
#             return False
#         return (
#             self.stage_context == other.stage_context
#             and self.stage_code == other.stage_code
#         )


# def handle_chain_response(
#     chain_response, python_file_path: Path
# ) -> tuple[str, str, bool]:
#     """
#     Handle both string and structured chain responses.

#     Args:
#         chain_response: Either a string response or structured output object
#         python_file_path: Path to save the Python code

#     Returns:
#         tuple[str, str, bool]: (requirements, code, is_structured)
#     """
#     # Check if it's a structured output (has code attribute)
#     if hasattr(chain_response, "code"):
#         # Structured output - extract directly
#         requirements = getattr(chain_response, "requirements", None)
#         code = chain_response.code
#         # Handle None requirements - convert to empty string
#         requirements_str = requirements if requirements is not None else ""
#         save_python_code(code, python_file_path)
#         return requirements_str, code, True
#     # String response
#     requirements, code = parse_and_save(chain_response, python_file_path)
#     # Handle None requirements from parse_and_save - convert to empty string
#     requirements_str = requirements if requirements is not None else ""
#     return requirements_str, code, False


# async def run_workflow_stage(
#     workflow_plan: str,
#     stage_chain,
#     stage_name: str,
#     stage_inputs: dict | None = None,
#     py_path: Path | None = None,
#     max_retries: int = 3,
# ) -> AsyncGenerator[Event | StageResult, None]:
#     """
#     Runs a workflow stage and handles retries with improved error feedback.
#     Supports both string and structured output from LLM chains.

#     Args:
#         stage_chain: Chain to execute (can return string or structured output)
#         stage_name: Current stage name
#         stage_inputs: Additional inputs for the stage
#         py_path: Path for generated Python files
#         max_retries: Maximum number of retry attempts

#     Yields:
#         Events during execution (logs, steps, etc.)

#     Returns:
#         StageResult with (stage_context, stage_code) or (None, None) if failed
#     """
#     if stage_inputs is None:
#         stage_inputs = {}
#     error_logs = []
#     stage_code = "No Code (First iteration)"
#     stage_name_formatted = " ".join(
#         [word.capitalize() for word in stage_name.split("_")]
#     )

#     def prepare_error_logs(logs: list[str]) -> str:
#         if not logs:
#             return "No previous errors"
#         return "\n".join(
#             f"Attempt {i + 1} error:\n{error}" for i, error in enumerate(logs)
#         )

#     # Base inputs that are common across stages
#     base_inputs = {
#         "workflow_plan": workflow_plan,
#         "error_logs": prepare_error_logs(error_logs),
#         "stage_code": stage_code,
#     }

#     # Merge base inputs with stage-specific inputs
#     input_dict = {**base_inputs, **stage_inputs}

#     for attempt in range(max_retries):
#         if attempt != 0:
#             yield StepEvent(
#                 f"Oops... something went wrong. Let me try again... ({attempt + 1}/{max_retries})",
#             )
#         try:
#             # Get LLM response (could be string or structured output)
#             stage_chain_response = await stage_chain.ainvoke(input=input_dict)

#             if not py_path:
#                 stage_filename = f"{stage_name}_stage_attempt{attempt + 1}"
#                 py_path = Path(f"{stage_filename}.py")

#             # Handle both structured and string responses
#             requirements, stage_code, is_structured = handle_chain_response(
#                 chain_response=stage_chain_response,
#                 python_file_path=py_path,
#             )

#             if is_structured:
#                 yield StepEvent("Executing the code...")
#                 error = await simple_execute_python_script(py_path)
#                 if error:
#                     yield LogEvent(f"Error in run_workflow_stage, execution: {error}")
#                     error_logs.append(error)
#                     input_dict.update(
#                         {
#                             "error_logs": prepare_error_logs(error_logs),
#                             "stage_code": stage_code,
#                         }
#                     )
#                     continue

#                 # Success case for structured output
#                 yield FileEvent(
#                     path=py_path,
#                     title=f"{stage_name_formatted} Stage Script",
#                     description=f"The Python script for {stage_name_formatted} stage",
#                 )
#                 # For structured output, we don't have execution context, so return empty list
#                 yield StageResult([], stage_code)
#                 return
#             else:
#                 # For string responses
#                 requirements_error = await install_requirements(requirements or "")
#                 if requirements_error:
#                     yield LogEvent(
#                         f"Error in run_workflow_stage, requirements: {requirements_error}"
#                     )
#                     error_logs.append(
#                         f"Failed to install requirements: {requirements_error}"
#                     )
#                     input_dict["error_logs"] = prepare_error_logs(error_logs)
#                     continue

#                 yield StepEvent("Executing the code...")
#                 success, stage_context, error = await execute_python_script(py_path)

#                 if success:
#                     # Add file events for generated files
#                     yield FileEvent(
#                         path=py_path,
#                         title=f"{stage_name_formatted} Stage Script",
#                         description=f"The Python script for {stage_name_formatted} stage",
#                     )
#                     yield StageResult(stage_context, stage_code)
#                     return  # Stop the generator

#                 # Handle failure
#                 yield LogEvent(f"Error in run_workflow_stage, execution: {error}")
#                 error_logs.append(error)

#                 input_dict.update(
#                     {
#                         "error_logs": prepare_error_logs(error_logs),
#                         "stage_code": stage_code,
#                     }
#                 )

#         except Exception as e:
#             yield LogEvent(f"Error in run_workflow_stage: {traceback.format_exc()}")
#             error_logs.append(str(e))
#             input_dict["error_logs"] = prepare_error_logs(error_logs)

#     yield TextEvent(Constants.retries_exceeded_message)
#     yield StageResult(None, None)
#     return
