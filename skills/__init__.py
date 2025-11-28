"""
The catalog of all Brewer skills.
"""

from hopsworks_brewer.framework.team import Team

from . import (
    charts,
    chat,
    execute_python,
    files,
    generate_uuid,
    hopsworks,
    pipelines,
    talker,
)


def add_to_team(team: Team):
    charts.add_to_team(team)
    chat.add_to_team(team)
    execute_python.add_to_team(team)
    files.add_to_team(team)
    generate_uuid.add_to_team(team)
    hopsworks.add_to_team(team)
    pipelines.add_to_team(team)
    talker.add_to_team(team)
