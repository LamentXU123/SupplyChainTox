from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.timer import Timer
from textual.widgets import Static


APP_NAME = "SupplyChainTox"
# Use an escape sequence so the cursor renders consistently across shells.
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


def render_splash(cursor_visible: bool, loading_frame: int) -> str:
    # Both splash timers feed through this helper so the output stays in sync.
    cursor = INSERT_CURSOR if cursor_visible else " "
    spinner = LOADING_FRAMES[loading_frame % len(LOADING_FRAMES)]
    return f"[b]{APP_NAME}{cursor}[/]\n\n[dim]loading {spinner}[/]"


class SupplyChainToxApp(App[None]):
    TITLE = APP_NAME
    SUB_TITLE = "Minimal Textual shell"
    BINDINGS = [
        # Let the UI exit like a normal terminal app.
        Binding("ctrl+c", "quit", "Quit", show=False),
    ]

    CSS = """
    Screen {
        background: #0b111b;
        color: #e5edf6;
    }

    #splash {
        width: 1fr;
        height: 1fr;
        content-align: center middle;
        text-align: center;
        color: #7dd3fc;
        text-style: bold;
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
        yield Static("", id="splash")
        # The main shell is intentionally blank once the splash completes.
        yield Vertical(id="app-shell")

    def on_mount(self) -> None:
        self.query_one("#app-shell").display = False
        self._update_splash()
        # Keep the cursor blink slower than the spinner to reduce visual noise.
        self._cursor_timer = self.set_interval(0.5, self._tick_cursor)
        self._loading_timer = self.set_interval(0.12, self._tick_loading)
        self.set_timer(2.0, self._finish_splash)

    def _tick_cursor(self) -> None:
        self._cursor_visible = not self._cursor_visible
        self._update_splash()

    def _tick_loading(self) -> None:
        self._loading_frame += 1
        self._update_splash()

    def _update_splash(self) -> None:
        self.query_one("#splash", Static).update(
            render_splash(self._cursor_visible, self._loading_frame)
        )

    def _finish_splash(self) -> None:
        if self._cursor_timer is not None:
            self._cursor_timer.stop()
        if self._loading_timer is not None:
            self._loading_timer.stop()
        self.query_one("#splash", Static).display = False
        self.query_one("#app-shell").display = True


def main() -> None:
    SupplyChainToxApp().run()


if __name__ == "__main__":
    main()
