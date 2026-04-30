import unittest

from textual.widgets import Static

from main import (
    APP_NAME,
    INSERT_CURSOR,
    LOADING_FRAMES,
    SupplyChainToxApp,
    render_loading,
    render_title,
)


class SplashRenderTests(unittest.TestCase):
    def test_render_title_uses_center_text_and_cursor_markup(self) -> None:
        title = render_title(cursor_visible=True)

        self.assertIn(APP_NAME, title)
        self.assertIn(INSERT_CURSOR, title)
        self.assertIn("[b white]", title)
        self.assertIn("[b #f59e0b]", title)

    def test_render_title_hides_cursor_when_disabled(self) -> None:
        title = render_title(cursor_visible=False)

        self.assertIn(APP_NAME, title)
        self.assertNotIn(INSERT_CURSOR, title)

    def test_render_loading_uses_lighter_markup_and_spinner(self) -> None:
        loading = render_loading(1)

        self.assertIn("[#e5e7eb]", loading)
        self.assertIn(f"loading {LOADING_FRAMES[1]}", loading)


class SplashControlTests(unittest.IsolatedAsyncioTestCase):
    async def test_loading_stays_hidden_until_requested(self) -> None:
        app = SupplyChainToxApp()

        async with app.run_test() as pilot:
            await pilot.pause()
            loading = app.query_one("#splash-loading", Static)

            self.assertFalse(loading.display)

            app.show_loading()
            await pilot.pause()

            self.assertTrue(loading.display)

    async def test_finish_loading_switches_to_main_screen(self) -> None:
        app = SupplyChainToxApp()

        async with app.run_test() as pilot:
            await pilot.pause()
            app.show_loading()
            await pilot.pause()
            app.finish_loading()
            await pilot.pause()

            self.assertFalse(app.query_one("#splash-shell").display)
            self.assertTrue(app.query_one("#app-shell").display)


if __name__ == "__main__":
    unittest.main()
