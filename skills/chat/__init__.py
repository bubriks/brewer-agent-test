"""
The catalog of the Brewer skills related to Brewer chats.
"""

from hopsworks_brewer.framework import Team

from . import set_title


def add_to_team(team: Team):
    set_title.add_to_team(team)
