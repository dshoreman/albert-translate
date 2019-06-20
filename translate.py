"""Translates a string to English or a specified language,
auto-detecting the source language with the Cloud Translate API.

Usage: tr [to:<lang-code>] <text to translate>"""

import os
import json
import configparser
from albertv0 import *
from google.api_core.exceptions import *
from google.cloud import translate_v3beta1 as translate

__iid__ = "PythonInterface/v0.2"
__author__ = "Dave Shoreman"
__prettyname__ = "Translate"
__version__ = "0.2.0"
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
        config['extension'] = {'target_lang': 'en'}

        with open(confPath, 'w') as configFile:
            config.write(configFile)

    global client, parent, project_id
    project_id = config.get('api', 'project_id')

    if project_id != "":
        client = translate.TranslationServiceClient()
        parent = client.location_path(project_id, 'global')

    if not config.has_section('extension'):
        info("Adding extension section to config")
        config.add_section('extension')

    if not config.has_option('lang', 'target_lang'):
        info("Setting config.lang.target_lang")
        config['extension']['target_lang'] = "en"
        with open(confPath, 'w') as configFile:
            config.write(configFile)

def handleQuery(query):
    if not query.isTriggered:
        return

    if not project_id:
        item = makeItem(query, "Missing or invalid config", "Press enter to open it in your editor")
        item.addAction(ProcAction("Open extension config in your editor", ["xdg-open", confPath]))
        return item

    str = query.string.strip()
    if str == "":
        return makeItem(query, subtext="Usage: `tr [string to translate]`")

    strParts = str.split(' ', 1)
    lang_to = config.get('extension', 'target_lang')
    if "to:" in strParts[0] and len(strParts) > 1:
        arg, str = strParts
        lang_to = arg.split(':')[1].strip()

    try:
        response = client.translate_text(
            parent=parent,
            contents=[str],
            mime_type='text/plain',
            target_language_code=lang_to
        )

        translation = response.translations[0]

        item = makeItem(
            query, translation.translated_text,
            "Translated to {} from {}".format(
                lang.toName(lang_to),
                lang.toName(translation.detected_language_code)
            )
        )
        item.addAction(ClipAction("Copy to clipboard", item.text))
        return item
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

    return makeItem(query, subtext=subtext)

def makeItem(query=None, text=__prettyname__, subtext=""):
    return Item(
        id=__prettyname__,
        icon=iconPath,
        text=text,
        subtext=subtext,
        completion=query.rawString
    )

class Lang:
    langPath = os.path.dirname(__file__) + "/languages.json"
    languages = dict()

    def __init__(self):
        if os.path.exists(self.langPath):
            debug("Loading support languages from " + self.langPath)
            with open(self.langPath) as langJson:
                self.languages = json.load(langJson)

    def toCode(self, name):
        return self.languages.keys()[languages.values().index(name)]

    def toName(self, code):
        return self.languages.get(code)

lang = Lang()
