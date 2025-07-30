from ui.state.app_state import AppState, PythonQuizState, PythonTaskState


def select_current_task(state: AppState) -> PythonTaskState | None:
    curr_id = state.current.task_id
    if curr_id is None:
        return None
    return state.tasks[curr_id]


def select_current_quiz(state: AppState) -> PythonQuizState | None:
    curr_id = state.current.quiz_id
    if curr_id is None:
        return None
    return state.quizes[curr_id]


def select_task(state: AppState, task_id: int) -> PythonTaskState:
    if task_id not in state.tasks:
        raise KeyError(f"{task_id} not exists")
    return state.tasks[task_id]


def select_quiz_by_id(state: AppState, quiz_id: str) -> PythonQuizState:
    if quiz_id not in state.quizes:
        raise KeyError(f"{quiz_id} not exists")
    return state.quizes[quiz_id]
