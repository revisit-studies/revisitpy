import importlib.metadata
import pathlib
import anywidget  # type: ignore
import traitlets  # type: ignore
import pandas as pd

try:
    __version__ = importlib.metadata.version("revisit_notebook_widget")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


class Widget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"
    config = traitlets.Dict({}).tag(sync=True)
    sequence = traitlets.List([]).tag(sync=True)
    participants_data_json = traitlets.List([]).tag(sync=True)
    participants_data_tidy = traitlets.Dict({}).tag(sync=True)

    def get_df(self):
        # Extract rows and headers
        rows = self.participants_data_tidy['rows']
        header = self.participants_data_tidy['header']

        # Create DataFrame
        return pd.DataFrame(rows, columns=header)
