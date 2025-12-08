"""
The catalog of the Brewer skills related to Hopsworks Data Sources.
"""

from hopsworks_brewer.framework import Team

from . import describe_data_source, preview_data_source


def add_to_team(team: Team):
    describe_data_source.add_to_team(team)
    preview_data_source.add_to_team(team)
