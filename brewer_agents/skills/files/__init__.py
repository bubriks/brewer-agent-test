"""
The catalog of the Brewer skills related to file management.
"""

from hopsworks_brewer.framework import Team

from . import list_directory, preview_file_data, read_file, save_file


def add_to_team(team: Team):
    list_directory.add_to_team(team)
    preview_file_data.add_to_team(team)
    read_file.add_to_team(team)
    save_file.add_to_team(team)
