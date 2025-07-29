from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static

from textual_plot import PlotWidget


class ScrollApp(App):
    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Static("Hello, world!\n" * 20)
            yield PlotWidget()

    def on_mount(self) -> None:
        self.query_one(PlotWidget).plot([1, 2, 3, 4, 5], [10, 20, 30, 20, 10])


ScrollApp().run()
