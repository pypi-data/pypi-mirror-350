from textual.app import App, ComposeResult
from textual.widgets import Header, Footer


class HelloApp(App):

    def on_mount(self) -> None:
        self.title = "Hello, textual"
        
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
