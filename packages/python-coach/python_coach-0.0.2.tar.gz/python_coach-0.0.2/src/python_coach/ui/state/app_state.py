from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class AppState:
    user_email: str
    quizes: dict[str, PythonQuizState]
    tasks: dict[int, PythonTaskState]
    current: CurrentState
    run_code: RunCodeState
    last_action_type: str


CodeRunResult = Literal["passed", "failed", "not_run"]


@dataclass
class CurrentState:
    task_id: int | None = None
    quiz_id: str | None = None
    app_title: str = "Клондайк аналитика"
    app_subtitle: str = ""
    # название выбранного объекта
    object_name: Literal["quiz", "task", "account"] | None = None


@dataclass
class PythonQuizState:
    id: str
    title: str
    tasks: dict[int, PythonTaskState]
    is_node_expanded: bool = False


PythonTaskResult = Literal["passed", "failed", "not_runned"]


@dataclass
class PythonTaskState:
    id: int
    title: str
    description: str
    code_template: str
    code: str
    test_cases: list[dict[str, Any]]
    is_passed: PythonTaskResult


@dataclass
class RunCodeState:
    last_run_dt: datetime = datetime.now()
    last_code: str = ''
    result_cases: list[ResultCaseState] = field(
        default_factory=list["ResultCaseState"]
    )
    has_errors: bool = False
    errors: list[str] = field(default_factory=list[str])


@dataclass
class ResultCaseState:
    func_params: dict[str, Any]
    expected: str
    actual: str
    passed: bool
    has_exception: bool
    exception_message: str | None


INITIAL_STATE = AppState(
    user_email="",
    current=CurrentState(),
    run_code=RunCodeState(),
    tasks={},
    quizes={},
    last_action_type=""
)
