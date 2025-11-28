"""
The catalog of the Brewer skills related to charts.
"""

from hopsworks_brewer.framework import Team

from . import aggregate_chart_data, chart_drawer, visualize_chart_data


def add_to_team(team: Team):
    aggregate_chart_data.add_to_team(team)
    chart_drawer.add_to_team(team)
    visualize_chart_data.add_to_team(team)
