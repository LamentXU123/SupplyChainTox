# -*- encoding: utf-8 -*-
from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import Screen
from textual.timer import Timer
from textual.widgets import Static, TextArea
from typing import Callable

VERSION = 'v0.1 alpha'
APP_NAME = "SupplyChainTox"
INSERT_CURSOR = "█"
LOADING_FRAMES = (
    "\u280b",
    "\u2819",
    "\u2839",
    "\u2838",
    "\u283c",
    "\u2834",
    "\u2826",
    "\u2827",
    "\u2807",
    "\u280f",
)


def render_title(cursor_visible: bool) -> str:
    cursor = f"[b #f59e0b]{INSERT_CURSOR}[/]" if cursor_visible else " "
    return f"[b white]{APP_NAME} [{VERSION}][/]{cursor}"


def render_loading(loading_frame: int) -> str:
    spinner = LOADING_FRAMES[loading_frame % len(LOADING_FRAMES)]
    return f"[#e5e7eb]loading {spinner}[/]"


class Stage:
    def __init__(
        self,
        id: str,
        title: str,
        content: str = "",
        on_enter: Callable[[], None] | None = None,
        on_exit: Callable[[], None] | None = None
    ):
        self.id = id
        self.title = title
        self.content = content
        self.on_enter = on_enter
        self.on_exit = on_exit
        self.active = False


class StageManager:
    def __init__(self):
        self.stages: list[Stage] = []
        self.current_index = -1
        self.on_change: Callable[[Stage], None] | None = None

    def add_stage(self, stage: Stage) -> 'StageManager':
        self.stages.append(stage)
        return self

    def go_to(self, index: int) -> bool:
        if 0 <= index < len(self.stages):
            if self.current_index >= 0:
                self.stages[self.current_index].active = False
                if self.stages[self.current_index].on_exit:
                    self.stages[self.current_index].on_exit()
            self.current_index = index
            s = self.stages[index]
            s.active = True
            if s.on_enter:
                s.on_enter()
            if self.on_change:
                self.on_change(s)
            return True
        return False

    def next(self) -> bool:
        return self.go_to(self.current_index + 1)

    def prev(self) -> bool:
        return self.go_to(self.current_index - 1)

    def current(self) -> Stage | None:
        if 0 <= self.current_index < len(self.stages):
            return self.stages[self.current_index]
        return None

    def update_content(self, index: int, content: str) -> bool:
        if 0 <= index < len(self.stages):
            self.stages[index].content = content
            return True
        return False


class StageView(Screen):
    def __init__(self, manager: StageManager):
        super().__init__()
        self.manager = manager
        self.manager.on_change = self._on_stage_change

    BINDINGS = [
        Binding("enter", "next_stage", show=False, priority=True),
        Binding("backspace", "prev_stage", show=False, priority=True),
    ]

    def compose(self) -> ComposeResult:
        yield TextArea(id="stage-content", read_only=True)
        yield Static("Enter: Next | Backspace: Previous", id="hint")

    def on_mount(self) -> None:
        self.set_timer(0.1, self._init)

    def _init(self) -> None:
        self.manager.go_to(0)

    def _on_stage_change(self, stage: Stage) -> None:
        content = self.query_one("#stage-content", TextArea)
        content.text = stage.content
        content.cursor_position = len(stage.content)

    def action_next_stage(self) -> None:
        self.manager.next()

    def action_prev_stage(self) -> None:
        self.manager.prev()


class SupplyChainToxApp(App[None]):
    TITLE = APP_NAME
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=False),
    ]

    CSS = """
    Screen {
        background: #1a1a2e;
    }

    #splash-shell {
        width: 1fr;
        height: 1fr;
    }

    #splash-title {
        width: 1fr;
        height: 1fr;
        content-align: center middle;
        text-align: center;
        color: #ffffff;
        text-style: bold;
    }

    #splash-loading {
        width: 1fr;
        height: 3;
        content-align: center middle;
        text-align: center;
    }

    #stage-content {
        height: 1fr;
        margin: 1;
        border: solid #e94560;
    }

    #hint {
        height: 1;
        content-align: center middle;
        color: #636e72;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self._cursor_visible = True
        self._loading_frame = 0
        self._cursor_timer: Timer | None = None
        self._loading_timer: Timer | None = None
        self._stage_manager = StageManager()
        self._setup_stages()

    def _setup_stages(self) -> None:
        self._stage_manager.add_stage(Stage(
            id="dashboard",
            title="Dashboard",
            content="Welcome to SupplyChainTox!\n\nThis dashboard displays the system's core functions and status information."
        )).add_stage(Stage(
            id="analysis",
            title="Attack Analysis",
            content="Analyze malicious packages, attack patterns, and threat indicators on PyPI."
        )).add_stage(Stage(
            id="scan",
            title="Dependency Scan",
            content="Scan for malicious packages, vulnerabilities, and security risks in project dependencies."
        )).add_stage(Stage(
            id="reports",
            title="Reports Center",
            content="Generate, view, and export security analysis reports."
        )).add_stage(Stage(
            id="settings",
            title="Settings",
            content="Configure scan rules, notification settings, and security policies."
        ))

    def compose(self) -> ComposeResult:
        with Vertical(id="splash-shell"):
            yield Static("", id="splash-title")
            yield Static("", id="splash-loading")

    def on_mount(self) -> None:
        self.query_one("#splash-loading", Static).display = False
        self._update_title()
        self._cursor_timer = self.set_interval(0.5, self._tick_cursor)
        self.set_timer(3.0, self._show_stages)

    def _show_stages(self) -> None:
        if self._cursor_timer is not None:
            self._cursor_timer.stop()
            self._cursor_timer = None
        if self._loading_timer is not None:
            self._loading_timer.stop()
            self._loading_timer = None
        self.push_screen(StageView(self._stage_manager))

    def show_loading(self) -> None:
        loading = self.query_one("#splash-loading", Static)
        loading.display = True
        self._update_loading()
        if self._loading_timer is None:
            self._loading_timer = self.set_interval(0.12, self._tick_loading)

    def _tick_cursor(self) -> None:
        self._cursor_visible = not self._cursor_visible
        self._update_title()

    def _tick_loading(self) -> None:
        self._loading_frame += 1
        self._update_loading()

    def _update_title(self) -> None:
        title = self.query_one("#splash-title", Static)
        title.update(render_title(self._cursor_visible))

    def _update_loading(self) -> None:
        loading = self.query_one("#splash-loading", Static)
        loading.update(render_loading(self._loading_frame))

    def get_stage_manager(self) -> StageManager:
        return self._stage_manager


def main() -> None:
    SupplyChainToxApp().run()


if __name__ == "__main__":
    main()