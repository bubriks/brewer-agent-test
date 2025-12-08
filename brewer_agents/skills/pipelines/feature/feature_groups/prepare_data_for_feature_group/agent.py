# from collections.abc import AsyncGenerator
# from datetime import datetime

# from langgraph.types import Command

# from hopsworks_brewer.agents.data_preparation.prompt import DataPreparationPrompt
# from hopsworks_brewer.agents.feature_agent import FeatureAgent
# from hopsworks_brewer.core.state import Agents, State, WorkflowStage
# from hopsworks_brewer.events import Event, LogEvent, StepEvent
# from hopsworks_brewer.state import State, WorkflowStage
# from hopsworks_brewer.utils.workflow_utils import StageResult, run_workflow_stage


# class DataPreparationAgent(FeatureAgent):
#     def __init__(self, llm):
#         super().__init__(llm)
#         self.llm = llm
#         self.prompt_builder = DataPreparationPrompt()
#         self.prompt = self.prompt_builder.get_prompt()
#         self.chain = self.get_chain()

#     async def run_workflow(self, state) -> AsyncGenerator[Event, None]:
#         yield LogEvent(f"FEATURE_GROUP_ROUTE: {state.feature_group_route}")
#         yield LogEvent(f"PREPARATION NODE - COMPLETED_STAGES: {state.completed_stages}")
#         yield LogEvent(
#             f"FG ANALYSIS IN COMPLETED STAGES?: {str(WorkflowStage.FEATURE_GROUP_ANALYSIS) in state.completed_stages}"
#         )

#         if str(WorkflowStage.FEATURE_GROUP_ANALYSIS) in state.completed_stages:
#             data_analysis_code = state.feature_group_analysis_code
#             data_analysis_context = state.feature_group_analysis_context
#         else:
#             data_analysis_code = state.data_analysis_code
#             data_analysis_context = state.data_analysis_context

#         async for event in run_workflow_stage(
#             workflow_plan=state.current_workflow_plan,
#             stage_chain=self.chain,
#             stage_name="data_preparation",
#             stage_inputs={
#                 "data_analysis_code": data_analysis_code,
#                 "data_analysis_context": data_analysis_context,
#             },
#         ):
#             if isinstance(event, StageResult):
#                 state.current_stage_code = event.stage_code
#                 state.data_preparation_context = event.stage_context
#                 state.data_preparation_code = event.stage_code
#                 state.completed_at = datetime.now().isoformat()
#                 continue
#             yield event

#     async def get_node(
#         self, state: State
#     ) -> AsyncGenerator[Event | Command[str], None]:
#         state.current_workflow = "feature_group_creation"
#         state.current_workflow_stage = "data_preparation"

#         # Check if this stage is already completed
#         if (
#             WorkflowStage.PREPARATION in state.completed_stages
#             and state.data_preparation_context
#             and state.data_preparation_code
#         ):
#             yield Command(update=state, goto="conductor")
#             return

#         # Add context reporting
#         state.context_to_report = "data_preparation_context"
#         yield StepEvent(
#             f"\N{WRENCH} Starting data preparation for the {' and '.join(state.active_dataset_names)} data"
#         )

#         async for result in self.run_workflow(state):
#             yield result

#         # Update completed stages
#         if WorkflowStage.PREPARATION not in state.completed_stages:
#             # Create a new list with the additional stage
#             updated_completed_stages = (
#                 list(state.completed_stages) if state.completed_stages else []
#             )
#             updated_completed_stages.append(WorkflowStage.PREPARATION)
#             state.completed_stages = updated_completed_stages
#             state.should_commit_file_events = False

#         # Data preparation complete - route to conductor for completion report and next steps
#         state.baseline_plan = "next_steps"
#         yield Command(update=state, goto=str(Agents.CONDUCTOR))
