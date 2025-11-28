"""
The catalog of the Brewer skills related to the feature engineering pipeline.
"""

from hopsworks_brewer.framework import Team

from . import data_sources, feature_engineer, feature_groups


def add_to_team(team: Team):
    data_sources.add_to_team(team)
    feature_engineer.add_to_team(team)
    feature_groups.add_to_team(team)
