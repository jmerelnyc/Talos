"""talos-sdk: use the Talos network (talos-auto) from Python, or auto-configure
your editor with the bundled `talos` CLI.

    from talos_sdk import Client

    client = Client()  # reads TALOS_API_KEY from the environment
    print(client.ask("Say hi in five words or fewer."))
"""
from __future__ import annotations

from .client import Client

__version__ = "0.1.0"
__all__ = ["Client", "__version__"]
