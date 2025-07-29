from textual.app import App, ComposeResult

from textual_hires_canvas import Canvas


class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Canvas()

    def on_mount(self) -> None:
        self.query_one(Canvas).set_pixel(0, 0)


MyApp().run()
