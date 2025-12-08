# TODO: Move to Hopsworks MCP
# import json

# from langchain_core.tools import StructuredTool

# from hopsworks_brewer.session import Session


# def get_feature_group_metadata(feature_group_name, version=1):
#     """
#     Retrieves comprehensive metadata for a feature group in a unified, convenient format.

#     Parameters:
#     -----------
#     feature_group_name : str
#         The name of the feature group to retrieve metadata for
#     version : int
#         The version of the feature group to retrieve metadata for
#         Default: 1

#     Returns:
#     --------
#     dict
#         A dictionary containing all metadata about the feature group including:
#         - Basic metadata (name, description, primary key, etc.)
#         - Feature definitions (name, type, description)
#         - Feature statistics (completeness, distinctness, null values, etc.)
#     """
#     project = Session().project
#     fs = project.get_feature_store()
#     feature_group = fs.get_feature_group(
#         name=feature_group_name,
#         version=version,
#     )

#     # Create the base metadata dictionary
#     metadata = {
#         "feature_group_name": feature_group.name,
#         "feature_group_description": feature_group.description,
#         "primary_key": feature_group.primary_key,
#         "event_time": feature_group.event_time,
#         "online_enabled": feature_group.online_enabled,
#         "features": [],
#     }

#     # Get feature statistics
#     try:
#         statistics = feature_group.get_statistics().feature_descriptive_statistics
#         has_statistics = True
#     except Exception as e:
#         statistics = []
#         has_statistics = False
#         metadata["statistics_error"] = str(e)

#     # Create a dictionary to quickly look up statistics by feature name
#     stats_lookup = {}
#     if has_statistics:
#         for stat in statistics:
#             # Remove None values to keep the output clean
#             stats_dict = {
#                 k: v
#                 for k, v in stat.to_dict().items()
#                 if v is not None and k not in ["id", "featureName", "percentiles"]
#             }

#             stats_lookup[stat.feature_name] = stats_dict

#     # Combine feature definitions with their statistics
#     for feature in feature_group.features:
#         feature_info = {
#             "name": feature.name,
#             "type": feature.type,
#             "description": feature.description
#             if hasattr(feature, "description")
#             else None,
#             "statistics": stats_lookup.get(feature.name, {}),
#         }

#         # Remove None values
#         feature_info = {k: v for k, v in feature_info.items() if v is not None}
#         metadata["features"].append(feature_info)

#     return json.dumps(metadata)


# tool = StructuredTool.from_function(get_feature_group_metadata, return_direct=True)
