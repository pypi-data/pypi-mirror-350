from os.path import dirname, realpath, join, exists
import json
from datacontext.quiz_content import JsonLoadResult, PythonQuizJson, QuestionJson, UserInfoJson
from ui.state.app_state import AppState, PythonQuizState, \
    PythonTaskState, RunCodeState, CurrentState


class DataContext:

    def get_quiz_json(self, email: str, pwd: str) -> JsonLoadResult:
        self._assert_login(email, pwd)
        this_file_dir = dirname(realpath(__file__))
        test_data_file_path = join(this_file_dir, "data_json.json")
        assert exists(test_data_file_path), "Test data file not exists"
        load_result = JsonLoadResult(
            user_info=UserInfoJson(email=""),
            quizes=[]
        )
        with open(test_data_file_path, encoding='UTF-8') as f:
            json_data = json.load(f)
            load_result.user_info.email = json_data["user_info"]["email"]
            # map quizes
            for quiz_json in json_data["quizes"]:
                quiz_obj = PythonQuizJson(
                    id=quiz_json["id"],
                    title=quiz_json["title"],
                    questions=[]
                )
                # map questions
                for question_json in quiz_json["questions"]:
                    quiz_obj.questions.append(
                        QuestionJson(
                            id=int(question_json["id"]),
                            title=question_json["title"],
                            text=question_json["text"],
                            code_template=question_json["code_template"],
                            test_cases=question_json["test_cases"]
                        )
                    )
                load_result.quizes.append(quiz_obj)

        return load_result

    def _assert_login(self, email: str, pwd: str) -> None:
        print(email)
        print(pwd)

    def create_state(self, data: JsonLoadResult) -> AppState:
        app_state = AppState(
            user_email=data.user_info.email,
            current=CurrentState(),
            run_code=RunCodeState(),
            quizes={},
            tasks={},
            last_action_type=""
        )
        app_state.quizes = {
            x.id: self._get_quiz_state(x) for x in data.quizes
        }
        app_state.tasks = {
            question.id: self._get_question_state(question)
            for quiz in data.quizes
            for question in quiz.questions
        }
        return app_state

    def _get_quiz_state(self, data: PythonQuizJson) -> PythonQuizState:
        return PythonQuizState(
            id=data.id,
            title=data.title,
            tasks={
                q.id: self._get_question_state(q) for q in data.questions
            }
        )

    def _get_question_state(self, data: QuestionJson) -> PythonTaskState:
        return PythonTaskState(
            id=data.id,
            title=data.title,
            description=data.text,
            code_template=data.code_template,
            code=data.code_template,
            test_cases=data.test_cases
        )
