## What is this?

A very small and simple Python package meant to close, open, and stop a 
Velux shutter using a remote control wired to a few GPIOs.  
For assembly details, see [this section](#assembly).
<br><br>
This GitHub repo: [https://github.com/Theo-Dancoisne/velux-remote-control](https://github.com/Theo-Dancoisne/velux-remote-control)  
This PyPi package: [https://pypi.org/project/theo-velux-remote-control](https://pypi.org/project/theo-velux-remote-control)

## How to install

```bash
pip install theo-velux-remote-control
```

## Usage

This package provides a simple CLI, you can see all the available commands by running:
```bash
velux --help
```  

Or use the module:
```python
from theo_velux_remote_control import velux


def IdoThings():
    velux.v_close()

def IdoThings2():
    velux.v_open()

def IdoThings3():
    velux.v_stop()

```


> [!NOTE]
> If you later want to use the GPIOs in other programs, or encounter strange results, try cleanning up the GPIOs setup with either `velux clean` or `velux.v_clean()`.

## Use other GPIOs pins

By default this package will use pin 2 to open, 3 to stop, and 4 to close.  
To change this you can set these environment variables to some appropriate **BMC codes**:
```bash
GPIO_PIN_VOPEN=2
GPIO_PIN_VSTOP=3
GPIO_PIN_VCLOSE=4
```

## Build from source

This package is managed with [Poetry](https://python-poetry.org/).
```bash
poetry install              # Installs dependencies
poetry build                # Builds the source and wheels archives
pip install --user /path_of_project/velux-remote-control/dist/package_name.whl
# ↳ Installs the package for the current user, don't forget to replace the project path and the name of the Wheel archive
```

Or if you simply want to test this package you can do this:
```bash
poetry install              # Installs dependencies
poetry run velux --help     # Runs a velux command in the Poetry virtual environment
```


<h2 id="assembly">Assembly instructions</h2>
Once you removed all but the circuit board from the remote controller (glued plastic foil with the 3 buttons included):

- Connect the - to a ground pin
- Connect the + to a 3.3V pin
- Connect the inner contact of the close button (between + and -) to the GPIO 4
- Connect the inner contact of the stop button (below close) to the GPIO 3
- Connect the inner contact of the open button (below stop) to the GPIO 2

<p align="middle">
    <img src="public/wiring_power.jpg" alt="Image visible on the GitHub repo" width="200">
    <img src="public/wiring_gpo.jpg" alt="Image visible on the GitHub repo" width="200">
</p>

> [!CAUTION]
> If your connection touches both the inner and outer contact of a button, it will trigger it until they are disconnected.

> [!TIP]
> Instead of wiring the + and - you can use the batteries, don't forget the battery connector if you do so.

## Q&A
#### Can I use this package with multiple remote controls?
Althoug this package wasn't designed to use multiple remote controls, as it only uses 3 environment variables to define the pins, we can consider some solutions sucha as:

- Do you know that a remote controls can operate several shutters at the same time?[^vhack]
- Connect all the remote controls to the same pins for simultaneous activation.
- Create a Docker container for each remote control, each container runs the package with the appropriate environment variables, the GPIOs must be exposed.
- Create your own program, this package is very simple, you can take inspiration to make your own.

<br>

[^vhack]: Quote from a Velux shutter documention:  
    > **Registration of a solar product in more than one remote control**  
    > One or more of the remote controls can be used for simultaneous operation.  
    > The example shows three solar products, **A**, **B** and **C**, where all three products are to be registered in the remote control from product **C**. ln this way, remote control **C** can operate solar products **A** and **B** as well.  
    > **The next two steps must be completed within 10 minutes:** 
    > 1. Press RESET button at the back of remote controls **A** and **B** for at least 10 seconds with a pointed object.
    > 2. Press RESET button on the back of remote control **C** for 1 second.  
    > The solar products **A**, **B** and **C** can now be operated via remote control **C**.  
    > **Note:** The solar products A and B can still be operated with their respective remote controls.  
    > **Cancelling of registration of a solar product**  
    > To remove the registration of a solar product in the remote control, press button *P* on the product (3) for 10 seconds (or until the product starts running).  
    > **Note:** The cancellation applies to all remote controls in which the product has been registered.

