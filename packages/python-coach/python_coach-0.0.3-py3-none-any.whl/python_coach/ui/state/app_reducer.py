from copy import deepcopy
from datetime import datetime
from typing import Union
from code_runner.runner import CodeRunner
from ui.state.app_state import (
    INITIAL_STATE,
    AppState,
    ResultCaseState)

from ui.editor_screen.actions.editor_actions import (
    BaseAction,
    MakeQuizCurrentAction,
    MakeTaskCurrentAction,
    QuizNodeCollapseAction,
    QuizNodeExpandAction,
    UpdateCodeAction,
    RunCodeAndSetResultsAction)

from ui.editor_screen.actions.init_action import InitAction, init_state
from ui.state.selectors import (
    select_current_task,
    select_quiz_by_id,
    select_task)

ActionType = Union[BaseAction,
                   MakeTaskCurrentAction,
                   UpdateCodeAction,
                   RunCodeAndSetResultsAction,
                   None]


def app_dispatch(state: AppState, action: BaseAction) -> AppState:
    new_state = deepcopy(state)
    new_state.last_action_type = action.type
    return apply_action(new_state, action)


def apply_action(state: AppState, action: ActionType) -> AppState:
    if isinstance(action, InitAction):
        init_state(state, action.data)
        return state
    if isinstance(action, MakeTaskCurrentAction):
        state.current.task_id = action.task_id
        state.current.quiz_id = None
        # set code to run
        curr_task = select_task(state, action.task_id)
        state.run_code.last_code = curr_task.code
        state.current.app_subtitle = curr_task.title
        state.current.object_name = "task"
        return state
    if isinstance(action, MakeQuizCurrentAction):
        state.current.quiz_id = action.quiz_id
        state.current.task_id = None
        quiz = select_quiz_by_id(state, action.quiz_id)
        state.current.app_subtitle = quiz.title
        state.current.object_name = "quiz"
        return state
    if isinstance(action, UpdateCodeAction):
        # update current code
        state.run_code.last_code = action.code

        # update current task code
        current_task = select_current_task(state)
        if current_task is not None:
            current_task.code = action.code

        # set code to run
        state.run_code.last_code = action.code
        return state
    if isinstance(action, RunCodeAndSetResultsAction):
        _run_and_set_results(state)
        return state
    if isinstance(action, QuizNodeExpandAction):
        quiz = state.quizes[action.quiz_id]
        quiz.is_node_expanded = True
        return state
    if isinstance(action, QuizNodeCollapseAction):
        quiz = state.quizes[action.quiz_id]
        quiz.is_node_expanded = False
        return state
    return INITIAL_STATE


def _run_and_set_results(state: AppState) -> None:
    current_task = select_current_task(state)
    if current_task is None:
        return
    # run code here and set results
    res = CodeRunner(function_name="solution").run_code(
        current_task.test_cases,
        current_task.code)

    # set last code run info
    state.run_code.last_run_dt = datetime.now()
    state.run_code.last_code = current_task.code

    state.run_code.result_cases = [
        ResultCaseState(
            func_params=r.func_params,
            expected=r.expected,
            actual=r.actual,
            passed=r.passed,
            has_exception=r.exception is not None,
            exception_message=r.exception
        ) for r in res.all_cases
    ]
    # add test case errors
    state.run_code.errors = list(res.errors)
    state.run_code.has_errors = len(res.errors) > 0

    are_all_tests_passed = all(c.passed for c in res.all_cases)

    is_task_passed = not state.run_code.has_errors and are_all_tests_passed

    # set run result:
    current_task.is_passed = "passed" if is_task_passed else "failed"
