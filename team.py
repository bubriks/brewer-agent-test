from hopsworks_brewer.framework import Team

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import test_p
import test_1
import test_2
from skills import add_to_team

team = Team()

test_p.add_to_team(team)
test_1.add_to_team(team)
test_2.add_to_team(team)
#add_to_team(team)

# Instead of get_agents we can just use the team and require the file to provide it
