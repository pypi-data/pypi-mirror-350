from textwrap import dedent
from rich.text import Text
from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Vertical
from textual.reactive import var

from ui.state.app_state import INITIAL_STATE, AppState


class CurrentTaskInfo(Vertical):

    DEFAULT_CSS = """
        CurrentTaskInfo {
            border: solid $primary;
            background: $background;
            height: 1fr;            
        }
    """

    state = var(INITIAL_STATE, init=False)

    task_text = Text.from_markup(dedent("""\
        Нужно вычислить сколько будет 2+2.
        :red_circle: Нужно написать функцию, которая
        [bold cyan]это делает[/bold cyan].
    """))

    def on_mount(self) -> None:
        self.border_title = "Задача"

    def compose(self) -> ComposeResult:
        yield Static(CurrentTaskInfo.task_text,
                     id="task_text")

    def watch_state(self, new_state: AppState) -> None:
        selected_task_id = new_state.current.task_id
        if selected_task_id is not None:
            task = new_state.tasks[selected_task_id]
            static = self.query_one("Static", Static)
            static.update(task.description)
