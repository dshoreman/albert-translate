"""Translates a string to English."""

import os
from albertv0 import *

__iid__ = "PythonInterface/v0.2"
__author__ = "Dave Shoreman"
__prettyname__ = "Translate"
__version__ = "0.1.0"
__trigger__ = "tr "
__dependencies__ = []

iconPath = os.path.dirname(__file__) + "/icon.png"

def handleQuery(query):
    if not query.isTriggered:
        return Item(
            id=__prettyname__,
            icon=iconPath,
            text=__prettyname__,
            subtext="Usage: `tr [string to translate]`"
        )

    str = query.string or "translate"

    return Item(
        id=__prettyname__,
        icon=iconPath,
        text=__prettyname__,
        subtext="Hello, {:s}!".format(str),
        completion=query.rawString
    )
