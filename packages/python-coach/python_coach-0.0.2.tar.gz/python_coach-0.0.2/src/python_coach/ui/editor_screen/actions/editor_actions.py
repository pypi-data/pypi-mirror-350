from dataclasses import dataclass
from ui.state.base_action import BaseAction


@dataclass
class MakeTaskCurrentAction(BaseAction):
    type = "MAKE_TASK_CURRENT"
    task_id: int


@dataclass
class UpdateCodeAction(BaseAction):
    type = "UPDATE_CODE"
    code: str


@dataclass
class RunCodeAndSetResultsAction(BaseAction):
    type = "RUN_CODE_AND_SET_RESULTS"


@dataclass
class MakeQuizCurrentAction(BaseAction):
    type = "MAKE_QUIZ_CURRENT"
    quiz_id: str


@dataclass
class QuizNodeExpandAction(BaseAction):
    type = "QuizNodeExpand"
    quiz_id: str


@dataclass
class QuizNodeCollapseAction(BaseAction):
    type = "QuizNodeCollapsed"
    quiz_id: str
