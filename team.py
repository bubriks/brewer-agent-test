from hopsworks_brewer.framework import Team

from . import sum, test_1, test_2

team = Team()

sum.add_to_team(team)
test_1.add_to_team(team)
test_2.add_to_team(team)

# Instead of get_agents we can just use the team and require the file to provide it
