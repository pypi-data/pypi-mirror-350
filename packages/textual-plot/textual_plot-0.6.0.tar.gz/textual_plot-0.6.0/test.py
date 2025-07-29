from textual.app import App, ComposeResult
from textual_hires_canvas import Canvas

from textual_plot import PlotWidget


class MinimalApp(App[None]):
    def compose(self) -> ComposeResult:
        # yield PlotWidget()
        yield Canvas()

    def on_mount(self) -> None:
        # plot = self.query_one(PlotWidget)
        # plot.plot(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
        self.query_one(Canvas).set_pixel(0, 0)


MinimalApp().run()
