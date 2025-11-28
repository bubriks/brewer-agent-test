"""
The catalog of the Brewer skills related to Hopsworks Feature Groups.
"""

from hopsworks_brewer.framework import Team

from . import create_feature_group, preview_feature_group


def add_to_team(team: Team):
    create_feature_group.add_to_team(team)
    preview_feature_group.add_to_team(team)
