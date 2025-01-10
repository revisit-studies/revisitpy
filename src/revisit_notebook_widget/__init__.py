import importlib.metadata
import pathlib
import anywidget
import traitlets

try:
    __version__ = importlib.metadata.version("revisit_notebook_widget")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"



# class Widget2(anywidget.AnyWidget):
    
class TestWidget(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
      let button = document.createElement("button");
      button.innerHTML = `count is ${model.get("value")}`;
      button.addEventListener("click", () => {
        model.set("value", model.get("value") + 1);
        model.save_changes();
      });
      model.on("change:value", () => {
        button.innerHTML = `count is ${model.get("value")}`;
      });
      el.classList.add("counter-widget");
      el.appendChild(button);
    }
    export default { render };
    """
    _css = """
    .counter-widget button { color: white; font-size: 1.75rem; background-color: #ea580c; padding: 0.5rem 1rem; border: none; border-radius: 0.25rem; }
    .counter-widget button:hover { background-color: #9a3412; }
    """
    value = traitlets.Int(0).tag(sync=True)



class Widget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"
    # value = traitlets.Int(0).tag(sync=True)
    config = traitlets.Dict({}).tag(sync=True)
    sequence = traitlets.List([]).tag(sync=True)
    internalWidget = TestWidget()

    @traitlets.observe('sequence')
    def _sequence_changed(self, change):
        self.internalWidget.value += 1
        # internalWidget.value += 1
        # print("{name} changed from {old} to {new}".format(**change))

    