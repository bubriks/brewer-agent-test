from hsfs.core.data_source import DataSource
from llama_index.core.tools import FunctionTool

from hopsworks_brewer.framework import Team
from hopsworks_brewer.session import Session


def preview_data_source(connector: str, database: str, group: str, table: str) -> dict:
    """
    Retrieve comprehensive context from a specific table in a storage connector.
    Returns: Structured context information about the specific table as a dictionary.
    """
    fs = Session().project.get_feature_store()

    # Get the storage connector
    sc = fs.get_storage_connector(connector)

    # Get data preview and feature information for the target table
    try:
        data_object = sc.get_data(
            DataSource(database=database, group=group, table=table)
        )

        # Extract feature information with safe field access
        features = [
            {
                "name": feature.get("name", ""),
                "type": feature.get("type", ""),
                "description": feature.get("description", ""),
            }
            for feature in data_object.features
        ]

        # Get data preview
        data_preview = [row["values"] for row in data_object.preview["preview"][:5]]

        # Structure data preview for easier interpretation
        preview_data = {}
        for row in data_preview:
            for feature in row:
                preview_data.setdefault(feature["value0"], []).append(feature["value1"])

        # Return structured context for the specific table
        return {
            "connector": connector,
            "database": database,
            "group": group,
            "table": table,
            "features": features,
            "data_preview": preview_data,
        }

    except Exception as e:
        return {
            "error": f"Problem retrieving data for table {table}",
            "details": str(e),
            "connector": connector,
            "database": database,
            "group": group,
            "table": table,
        }


def add_to_team(team: Team):
    team.add_tool(FunctionTool.from_defaults(preview_data_source))
