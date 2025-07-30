from dataclasses import dataclass
from datacontext.quiz_content import (
    JsonLoadResult,
    PythonQuizJson,
    QuestionJson)
from ui.state.app_state import (
    AppState,
    PythonQuizState,
    PythonTaskState)
from ui.state.base_action import BaseAction


@dataclass
class InitAction(BaseAction):
    type = "INIT_APP"
    data: JsonLoadResult


def init_state(state: AppState, data: JsonLoadResult) -> None:
    state.user_email = data.user_info.email
    state.quizes = {
        x.id: _get_quiz_state(x) for x in data.quizes
    }
    state.tasks = {
        question.id: _get_question_state(question)
        for quiz in data.quizes
        for question in quiz.questions
    }
    state.current.app_title = "Клондайк аналитика"
    state.current.app_subtitle = "интерактивный тренажер Python на вашем компьютере"


def _get_quiz_state(data: PythonQuizJson) -> PythonQuizState:
    return PythonQuizState(
        id=data.id,
        title=data.title,
        tasks={
            q.id: _get_question_state(q) for q in data.questions
        }
    )


def _get_question_state(data: QuestionJson) -> PythonTaskState:
    return PythonTaskState(
        id=data.id,
        title=data.title,
        description=data.text,
        code_template=data.code_template,
        code=data.code_template,
        test_cases=data.test_cases,
        is_passed="not_runned"
    )
