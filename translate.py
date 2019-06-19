"""Translates a string to English."""

import os
import configparser
from albertv0 import *
from google.api_core.exceptions import *
from google.cloud import translate_v3beta1 as translate

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
client = None

def initialize():
    config.read(confPath)

    if 'api' not in config or 'project_id' not in config['api']:
        critical("Translation requires Project ID to be set in " + confPath)

        config['api'] = {'project_id': ''}

        with open(confPath, 'w') as configFile:
            config.write(configFile)

    global client, parent, project_id
    project_id = config.get('api', 'project_id')

    if project_id != "":
        client = translate.TranslationServiceClient()
        parent = client.location_path(project_id, 'global')

def handleQuery(query):
    str = query.string.strip()
    text=__prettyname__
    lang_to = 'en'

    if not query.isTriggered or str == "":
        return Item(
            id=__prettyname__,
            icon=iconPath,
            text=text,
            subtext="Usage: `tr [string to translate]`"
        )

    if not project_id:
        return Item(
            id=__prettyname__,
            icon=iconPath,
            text=__prettyname__,
            subtext="Missing or invalid config in " + confPath
        )

    if "to:" in str.split(' ', 1)[0]:
        arg, str = str.split(' ', 1)
        lang_to = arg.split(':')[1].strip()

    try:
        response = client.translate_text(
            parent=parent,
            contents=[str],
            mime_type='text/plain',
            target_language_code=lang_to
        )

        translation = response.translations[0]
        subtext = translation.translated_text
        text = "Translated from {}".format(
            translation.detected_language_code
        )
    except GoogleAPICallError as err:
        subtext = "Translation failed ({}) ".format(err.message)
        warning("GoogleAPICallError")
        print(err)
    except RetryError as err:
        subtext = "Translation failed"
        warning("RetryError")
        print(err)
    except ValueError as err:
        subtext = "Translation failed"
        warning("Got ValueError: " + err)
        print(err)

    return Item(
        id=__prettyname__,
        icon=iconPath,
        text=text or __prettyname__,
        subtext=subtext,
        completion=query.rawString
    )
