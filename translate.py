"""Translates a string to English."""

import os
import configparser
from albertv0 import *

__iid__ = "PythonInterface/v0.2"
__author__ = "Dave Shoreman"
__prettyname__ = "Translate"
__version__ = "0.1.0"
__trigger__ = "tr "
__dependencies__ = []

confPath = os.path.join(configLocation(), "translate.ini")
iconPath = os.path.dirname(__file__) + "/icon.png"
config = configparser.ConfigParser()
project_id = ""

def initialize():
    config.read(confPath)

    if 'api' not in config or 'project_id' not in config['api']:
        critical("Translation requires Project ID to be set in " + confPath)

        config['api'] = {'project_id': ''}

        with open(confPath, 'w') as configFile:
            config.write(configFile)

    global project_id
    project_id = config.get('api', 'project_id')

def handleQuery(query):
    if not query.isTriggered:
        return Item(
            id=__prettyname__,
            icon=iconPath,
            text=__prettyname__,
            subtext="Usage: `tr [string to translate]`"
        )

    if not project_id:
        return Item(
            id=__prettyname__,
            icon=iconPath,
            text=__prettyname__,
            subtext="Missing or invalid config in " + confPath
        )

    str = query.string or "translate"

    return Item(
        id=__prettyname__,
        icon=iconPath,
        text=__prettyname__,
        subtext="Hello, {:s}!".format(str),
        completion=query.rawString
    )
