"""Translates a string to English."""

from albertv0 import *

__iid__ = "PythonInterface/v0.2"
__author__ = "Dave Shoreman"
__prettyname__ = "Translate"
__version__ = "0.1.0"
__trigger__ = "tr "
__dependencies__ = []

def handleQuery(query):
    if not query.isTriggered:
        return Item(
            id=__prettyname__,
            text=__prettyname__,
            subtext="Usage: `tr [string to translate]`"
        )

    return Item(
        id=__prettyname__,
        text=__prettyname__,
        subtext="Hello, translate!",
        completion=query.rawString
    )
