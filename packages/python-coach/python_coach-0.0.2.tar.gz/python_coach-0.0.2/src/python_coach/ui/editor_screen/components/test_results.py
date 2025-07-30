from datetime import datetime
from textual.app import ComposeResult
from textual.reactive import var
from textual.widgets import ListView, ListItem
from textual.containers import Vertical
from rich.text import Text


from ui.editor_screen.actions.editor_actions import RunCodeAndSetResultsAction
from ui.state.app_state import INITIAL_STATE, AppState, ResultCaseState


class TestResultItem(ListItem):

    DEFAULT_CSS = """
        TestResultItem {
            height: 1;
        }
    """

    def __init__(self, res: ResultCaseState):
        super().__init__()
        self._res = res

    def render(self) -> Text:
        if self._res.passed:
            return Text.from_markup(":green_circle: Test passed")
        return self._failed_markup()

    def _failed_markup(self) -> Text:
        if self._res.has_exception:
            return Text.from_markup(f":red_circle: {self._res.exception_message}")
        expected = self._res.expected
        actual = self._res.actual
        params_str = ",".join(f"{k} = {v}" for k, v
                              in self._res.func_params.items())
        return Text.from_markup(f":red_circle: Failed for {params_str}. " +
                                f"Expected = {expected}, " +
                                f"but having = {actual}")


class ErrorResultItem(ListItem):
    def __init__(self, error: str) -> None:
        super().__init__()
        self._error = error

    def render(self) -> Text:
        return Text.from_markup(f":red_circle: {self._error}")


class AllTestsPassedResultItem(ListItem):

    def render(self) -> Text:
        return Text.from_markup(":green_circle: задача решена!")


def has_failed_cases(state: AppState) -> bool:
    return any(not r.passed for r in state.run_code.result_cases)


def select_first_failed_case(state: AppState) -> ResultCaseState:
    failed_cases = (c for c in state.run_code.result_cases if not c.passed)
    return next(failed_cases)


def are_all_cases_passed(state: AppState) -> bool:
    return all(c.passed for c in state.run_code.result_cases)


def has_cases(state: AppState) -> bool:
    return len(state.run_code.result_cases) > 0


class TestResults(Vertical):

    state = var(INITIAL_STATE)

    DEFAULT_CSS = """
        TestResults {
            border: solid $primary;
            
            ListView {
                background: $background;

                ListItem {
                    background: $background;
                }
            }
        }

        """

    def __init__(self) -> None:
        super().__init__()

    def on_mount(self) -> None:
        self.border_title = "Test results"

    def compose(self) -> ComposeResult:
        yield ListView()

    def watch_state(self, state: AppState) -> None:
        if state.last_action_type != RunCodeAndSetResultsAction.type:
            return
        list_view = self.query_one("ListView", ListView)
        list_view.clear()
        # if has errors then append errors in list
        if state.run_code.has_errors:
            for err in state.run_code.errors:
                list_view.append(ErrorResultItem(err))
            return

        if are_all_cases_passed(state) and has_cases(state):
            list_view.append(AllTestsPassedResultItem())
            return
        if has_failed_cases(state):
            failed_case = select_first_failed_case(state)
            list_view.append(TestResultItem(failed_case))

        # # if no errors then display test results
        # for result in state.run_code.result_cases:
        #     list_view.append(TestResultItem(result))

        # display last run info
        if state.run_code.last_code != "":
            self.border_title = f"Результаты: {datetime.strftime(state.run_code.last_run_dt,
                                                                 "%H:%M:%S")}"
        self._last_update_dt = datetime.now()
