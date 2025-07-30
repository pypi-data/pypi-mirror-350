from typing import Any
from textual import on
from textual.app import App

from ui.auth_screen.auth import AuthScreen
from ui.editor_screen.editor import EditorScreen
from ui.editor_screen.actions.init_action import InitAction
from ui.state.app_state import INITIAL_STATE
from ui.state.app_reducer import app_dispatch


class RunnerApp(App[Any]):
    COMMAND_PALETTE_BINDING = "ctrl+backslash"

    MODES = {  # type: ignore
        "editor": EditorScreen,
        "auth": AuthScreen
    }

    def on_mount(self) -> None:
        self.switch_mode("auth")
        self.theme = "gruvbox"
        self.title = "Клондайк аналитика"
        self.sub_title = "Интерактивный тренажер Python на вашем компьютере"

    @on(AuthScreen.AuthSuccess)
    def on_auth_success(self, event: AuthScreen.AuthSuccess) -> None:
        if not isinstance(self.app.screen, EditorScreen):
            return
        editor_screen: EditorScreen = self.app.screen
        editor_screen.state = app_dispatch(
            INITIAL_STATE,
            InitAction(data=event.json)
        )

    @on(EditorScreen.UpdateAppTitleMessage)
    def on_title_subtitle_changed(self, event: EditorScreen.UpdateAppTitleMessage) -> None:
        self.title = event.title
        self.sub_title = event.subtitle
