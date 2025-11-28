"""
The catalog of the Brewer skills related to the three ML pipelines, that is: feature, training, and inference.
"""

from hopsworks_brewer.framework import Team

from . import feature


def add_to_team(team: Team):
    feature.add_to_team(team)
