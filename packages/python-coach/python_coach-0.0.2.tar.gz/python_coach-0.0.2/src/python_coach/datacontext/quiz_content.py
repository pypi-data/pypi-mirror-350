from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class UserInfoJson:
    email: str


@dataclass
class QuestionJson:
    id: int
    title: str
    text: str
    code_template: str
    test_cases: list[dict[str, Any]]


@dataclass
class PythonQuizJson:
    id: str
    title: str
    questions: list[QuestionJson]


@dataclass
class JsonLoadResult:
    user_info: UserInfoJson
    quizes: list[PythonQuizJson]
