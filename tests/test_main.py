import unittest

from main import APP_NAME, INSERT_CURSOR, LOADING_FRAMES, render_splash


class SplashTests(unittest.TestCase):
    def test_render_splash_uses_insertion_cursor_and_loading(self) -> None:
        splash = render_splash(cursor_visible=True, loading_frame=0)

        self.assertIn(APP_NAME, splash)
        self.assertIn(INSERT_CURSOR, splash)
        self.assertIn(f"loading {LOADING_FRAMES[0]}", splash)

    def test_render_splash_hides_cursor_when_disabled(self) -> None:
        splash = render_splash(cursor_visible=False, loading_frame=1)

        self.assertIn(APP_NAME, splash)
        self.assertNotIn(f"{APP_NAME}{INSERT_CURSOR}", splash)
        self.assertIn(f"loading {LOADING_FRAMES[1]}", splash)


if __name__ == "__main__":
    unittest.main()
