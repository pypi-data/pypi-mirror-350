from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.message import Message
from textual.containers import Grid, Horizontal
from textual.widgets import Label, Input, Button

from datacontext.dc import DataContext
from datacontext.quiz_content import JsonLoadResult


class AuthScreen(Screen[None]):

    CSS_PATH = "auth.tcss"

    class AuthSuccess(Message):
        """Successfull login"""

        def __init__(self, json: JsonLoadResult):
            super().__init__()
            self.json = json

    def compose(self) -> ComposeResult:
        with Grid():
            yield Label("Авторизация")
            yield Input("xyz@gmail.com", id="email")
            yield Input("1234", id="pwd")
            with Horizontal():
                yield Button("Войти",
                             id="login_button",
                             variant="success")
                yield Button("Выход",
                             id="exit_button",
                             variant="error")

    @on(Button.Pressed, "#login_button")
    def on_login(self) -> None:
        email_input = self.query_one("#email", Input)
        pwd_input = self.query_one("#pwd", Input)
        context = DataContext()
        load_result = context.get_quiz_json(email_input.value,
                                            pwd_input.value)
        self.post_message(self.AuthSuccess(load_result))
        self.app.switch_mode("editor")

    @on(Button.Pressed, "#exit_button")
    def on_exit(self) -> None:
        self.app.exit(0)
