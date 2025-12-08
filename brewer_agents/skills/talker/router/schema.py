# from pydantic import BaseModel, Field


# class WorkflowModel(BaseModel):
#     active_dataset_names: list[str] = Field(
#         description="Datasets to work with, based on the user query, minimal length is 1",
#     )

#     user_approval_status: bool = Field(
#         description="""
#         A boolean flag that indicates whether the user has explicitly approved the current workflow plan.
#         Set to True when the user gives clear approval to proceed with execution.
#         Set to False when the plan is newly proposed, the user has requested modifications,
#         or explicit approval is still pending.
#         """
#     )


# class ChartWorkflow(WorkflowModel):
#     """
#     For handling chart requests including:
#     - Creating and modifying charts
#     - Analyzing chart data
#     - Generating chart insights
#     """


# class FgChartWorkflow(WorkflowModel):
#     """
#     For handling feature group chart requests including:
#     - Creating and modifying charts displaying feature group data
#     - Analyzing feature group chart data
#     - Generating chart insights for feature group data

#     This tool should be prefered over ChartWorkflow when the user is working with feature groups.
#     """


# class FeatureGroupWorkflow(WorkflowModel):
#     """
#     For handling feature group workflow requests including:
#     - Direct requests to create feature groups
#     - Explicit commands to start feature engineering
#     - Actual data processing requests
#     - Active analysis/preparation tasks
#     - Feature Group Analysis (for Feature Group Context Retrieval and analysis)
#     """

#     reset_stages: list[str] = Field(
#         description=f"""
#         Stages that should be reset and rerun based on user intent
#         Options: [], {"WorkflowStage.ANALYSIS", "WorkflowStage.FEATURE_GROUP_ANALYSIS", "WorkflowStage.PREPARATION", "WorkflowStage.FEATURE_GROUP"}
#         - If the user starts to work with a new dataset or feature group, reset all stages
#         - If the user is working on the same task and the chat history progresses, set reset_stages to [] so the work is not reset and the system will not start from scratch
#         - If the user approves the plan, set reset_stages to []
#         - If the user created a feature group and then wants to create a derived feature group, reset all stages
#         """,
#     )
#     baseline_plan: str = Field(
#         description="""
#         Used for DECISION stages that require user approval and conductor plan generation.
#         Options:
#         - 'data_preprocessing': When user needs to approve preprocessing/feature engineering steps
#         - 'feature_group_creation': When user needs to approve feature group schema/configuration
#         - 'next_steps': For stage completion reports and transition questions
#         - 'auto': For automatic stages (data_analysis, feature_group_analysis, chart_generation)

#         CRITICAL RULES:
#         1. Set baseline_plan='auto' for AUTOMATIC stages (data_analysis, feature_group_analysis)
#         2. For initial requests, set baseline_plan='auto' to route directly to automatic analysis stages
#         3. Only set specific baseline_plan when the conductor needs to generate a decision plan
#         4. If user_approval_status=True for decision stages, set baseline_plan='auto' (execute existing plan)
#         5. If user_approval_status=False for decision stages, set appropriate baseline_plan (generate new plan)

#         Workflow flow:
#         - Initial request -> baseline_plan='auto', user_approval_status=True (automatic analysis)
#         - Analysis complete -> Ask user about next step
#         - User wants preprocessing -> baseline_plan='data_preprocessing', user_approval_status=False (generate plan)
#         - User approves preprocessing -> baseline_plan='auto', user_approval_status=True (execute plan)
#         """,
#     )
