import os
import sys
from python_coach.ui.runner_app import RunnerApp

this_file_dir = os.path.dirname(os.path.realpath(__file__))
python_coach_root = os.path.join(this_file_dir, "python_coach")

sys.path.append(python_coach_root)


def python_coach():
	app = RunnerApp()
	app.run()