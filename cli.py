# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2026/05/01 15:32:25
@Author  :   LamentXU 
'''
from __future__ import annotations
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.timer import Timer
from textual.widgets import Static
VERSION = 'v0.1 alpha'
APP_NAME = "SupplyChainTox"
# Use the literal block cursor the UI should display during the splash.
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


class SupplyChainToxApp(App[None]):
    TITLE = APP_NAME
    SUB_TITLE = "Minimal Textual shell"
    BINDINGS = [
        # Let the UI exit like a normal terminal app.
        Binding("ctrl+c", "quit", "Quit", show=False),
    ]

    CSS = """
    Screen {
        color: #ffffff;
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

    #app-shell {
        height: 1fr;
        width: 1fr;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self._cursor_visible = True
        self._loading_frame = 0
        self._cursor_timer: Timer | None = None
        self._loading_timer: Timer | None = None

    def compose(self) -> ComposeResult:
        with Vertical(id="splash-shell"):
            yield Static("", id="splash-title")
            yield Static("", id="splash-loading")
        # The main shell is intentionally blank once the splash completes.
        yield Vertical(id="app-shell")

    def on_mount(self) -> None:
        self.query_one("#app-shell").display = False
        self.query_one("#splash-loading", Static).display = False
        self._update_title()
        # Keep the cursor blink slower than the spinner to reduce visual noise.
        self._cursor_timer = self.set_interval(0.5, self._tick_cursor)

    def show_loading(self) -> None:
        """Show the bottom loading widget and start its spinner."""
        loading = self.query_one("#splash-loading", Static)
        loading.display = True
        self._update_loading()
        if self._loading_timer is None:
            self._loading_timer = self.set_interval(0.12, self._tick_loading)

    def finish_loading(self) -> None:
        """Stop splash animation and switch to the main screen."""
        if self._cursor_timer is not None:
            self._cursor_timer.stop()
            self._cursor_timer = None
        if self._loading_timer is not None:
            self._loading_timer.stop()
            self._loading_timer = None
        self.query_one("#splash-shell").display = False
        self.query_one("#app-shell").display = True

    def _tick_cursor(self) -> None:
        self._cursor_visible = not self._cursor_visible
        self._update_title()

    def _tick_loading(self) -> None:
        self._loading_frame += 1
        self._update_loading()

    def _update_title(self) -> None:
        self.query_one("#splash-title", Static).update(
            render_title(self._cursor_visible)
        )

    def _update_loading(self) -> None:
        self.query_one("#splash-loading", Static).update(
            render_loading(self._loading_frame)
        )


def main() -> None:
    SupplyChainToxApp().run()


if __name__ == "__main__":
    main()
