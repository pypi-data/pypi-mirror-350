import sys
from helloai import *
from helloai.runner import prepare_mod, run_mod


mod = sys.modules["__main__"]
if not getattr(sys, "__helloai__", None):
    if not getattr(mod, "__file__", None):
        raise ImportError(
            "You are running from an interactive interpreter.\n"
            "'import pgzrun' only works when you are running a Python file."
        )
    prepare_mod(mod)


def go():
    """Run the __main__ module as a HelloAI script."""
    if getattr(sys, "__helloai__", None):
        return
    run_mod(mod)
