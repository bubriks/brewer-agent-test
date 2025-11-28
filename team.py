from hopsworks_brewer.framework import Team

import test_p, test_1, test_2

team = Team()

test_p.add_to_team(team)
test_1.add_to_team(team)
test_2.add_to_team(team)

# Instead of get_agents we can just use the team and require the file to provide it
