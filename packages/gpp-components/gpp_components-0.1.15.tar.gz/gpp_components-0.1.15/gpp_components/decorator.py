import time
from rich import print
from rich import box
from rich.pretty import Pretty
from rich.panel import Panel
from rich.console import Console
from rich.padding import Padding
from rich.text import Text

console = Console()


class Decorators:
    def __init__(self, jsonStr) -> None:
        self.jsonStr = jsonStr

    def _timeIt(*dargs, **dkwargs):
        def decorator(func):
            def wrapper(*wargs, **wkwargs):
                # print(dargs, dkwargs)

                _s_time = time.time()
                result = func(*wargs, **wkwargs)
                _e_time = time.time()

                if settings := dkwargs.get("decorator_setting"):
                    title = settings
                else:
                    title = ""

                content = "Tasks ==> %s" % Decorators.during_sec(_e_time - _s_time)

                panel = Decorators.getPanel(
                    Pretty(content),
                    title=f":pile_of_poo: [bold green blink] Start [bold blue blink]{title} :thumbs_up:",
                    subtitle=f":pile_of_poo: [bold green blink] End [bold blue]{title} :thumbs_up:",
                )
                print(panel)
                print(Padding("", 1))

                return result

            return wrapper

        return decorator

    def during_sec(sec):
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)

    def getPanel(text, *args, **kwargs):
        try:
            text = a if type(a := text) == Text or type(a) == Pretty else str(a)

            panel = Panel(
                text,
                title=kwargs.get("title", "[bold blue]Title"),
                title_align=kwargs.get("title_align", "left"),
                subtitle=kwargs.get("subtitle", "[bold blue]SubTitle"),
                subtitle_align=kwargs.get("subtitle_align", "right"),
                style=kwargs.get("style", "none"),
                box=kwargs.get("box", box.HEAVY_EDGE),
                border_style=kwargs.get("border_style", "green"),
                padding=kwargs.get("padding", 1),
                highlight=kwargs.get("highlight", False),
            )
            return panel

        except Exception:
            console.print_exception()


if __name__ == "__main__":

    @Decorators._timeIt(decorator_setting={"factory": "CCC2", "item": "Allocation"})
    def run(*args, **kwargs):
        print(kwargs)

    run({"a": "b"})
