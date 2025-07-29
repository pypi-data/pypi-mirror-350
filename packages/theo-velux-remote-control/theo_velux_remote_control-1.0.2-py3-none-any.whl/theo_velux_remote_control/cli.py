import typer
from rich import print
from .velux import *


app = typer.Typer()


@app.command()
def open():
    """Open the shutter."""
    v_open()

@app.command()
def stop():
    """Stop the shutter."""
    v_stop()

@app.command()
def close():
    """Close the shutter."""
    v_close()

@app.command()
def clean():
    """
    Clear the Python GPIOs setup, if you plan to use them later in another project for example.
    """
    v_cleanup()

@app.command()
def show():
    """
    Show the GPIOs that will be used to execute open, stop, or close commands.
    """
    print(f"Open: {VELUX_PIN_OPEN}")
    print(f"Stop: {VELUX_PIN_STOP}")
    print(f"Close: {VELUX_PIN_CLOSE}")
    v_cleanup()


if __name__ == "__main__": app()
