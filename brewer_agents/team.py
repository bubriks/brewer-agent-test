from hopsworks_brewer.framework import Team

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from skills import add_to_team

team = Team()

add_to_team(team)
