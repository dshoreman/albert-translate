"""Translates a string to English or a specified language,
auto-detecting the source language with the Cloud Translate API.

Usage: tr [to:<lang-code>] <text to translate>"""

import os
import json
import configparser
from albertv0 import *
from google.api_core.exceptions import *
from google.cloud import translate_v3beta1 as api
from urllib.parse import quote as quote_url

__iid__ = "PythonInterface/v0.2"
__author__ = "Dave Shoreman"
__prettyname__ = "Translate"
__version__ = "0.3.0"
__trigger__ = "tr "
__dependencies__ = []

confPath = os.path.join(configLocation(), "translate.ini")
iconPath = os.path.dirname(__file__) + "/icon.png"
config = configparser.ConfigParser()
project_id = ""
client = None

def initialize():
    loadConfig()

    keyfile = None
    if config.has_option('api', 'service_key'):
        keyfile = os.path.expanduser(config.get('api', 'service_key'))

        if not os.path.exists(keyfile):
            warning("Could not find service key JSON at " + keyfile)
            keyfile = None

    global client, parent, project_id
    project_id = config.get('api', 'project_id').strip()

    if project_id == "":
        critical("Translation requires Project ID to be set in " + confPath)
    else:
        try:
            if keyfile is not None:
                client = api.TranslationServiceClient.from_service_account_file(keyfile)
            else:
                client = api.TranslationServiceClient()

            parent = client.location_path(project_id, 'global')
        except Exception as err:
            critical(err)

def loadConfig():
    global writeConfig
    writeConfig = False
    config.read(confPath)

    addConfigOption('api', 'project_id')
    addConfigOption('api', 'service_key')
    addConfigOption('extension', 'source_lang', 'auto')
    addConfigOption('extension', 'target_lang', 'en')

    if writeConfig:
        with open(confPath, 'w') as configFile:
            info("Writing config file to {}".format(confPath))
            config.write(configFile)

def addConfigOption(section, option, value=''):
    if not config.has_section(section):
        config.add_section(section)

    if config.has_option(section, option):
        return

    global writeConfig
    config[section][option] = value
    writeConfig = True

def handleQuery(query):
    if not query.isTriggered:
        return

    if not project_id:
        return badConfigItem(query, "Missing or invalid config", "Press enter to open it in your editor")

    if client is None:
        return badConfigItem(query, "Failed to load API client", "Did you set your service key path?")

    global targets
    str, source, targets = parseArgs(query.string.strip())
    if str == "":
        return makeItem(query, subtext="Usage: `tr [string to translate]`")

    if source != "auto" and not lang.has(source):
        return badLanguageItem(query, source)

    items = []
    targets = targets.split(',')
    for target in targets:
        if target.strip() == "" or len(targets) > 1 and source == target:
            continue

        if lang.has(target):
            item = translate(str, source, target, query)
            if item is None:
                continue
        else:
            item = badLanguageItem(query, target)
        items.append(item)

    return items

def parseArgs(str):
    source = config.get('extension', 'source_lang', fallback='auto')
    target = config.get('extension', 'target_lang')

    for i, current in enumerate(str.split(' ')):
        if i > 1 or ":" not in current:
            break

        arg, value = current.split(':')
        if value == "":
            continue

        if arg == "from":
            str = ' '.join(str.split(' ')[1:])
            source = value
        elif arg == "to":
            str = ' '.join(str.split(' ')[1:])
            target = value

    if source == "":
        source = "auto"

    return str, source, target

def translate(str, source, target, query):
    try:
        params = {
            'parent': parent,
            'contents': [str],
            'mime_type': 'text/plain',
            'target_language_code': target
        }
        if source != "auto":
            params['source_language_code'] = source

        return responseToItem(client.translate_text(**params),
                              str, source, target, query)
    except GoogleAPICallError as err:
        errmsg = "Translation failed: {}".format(err.message)
        warning(err)
    except RetryError as err:
        errmsg = "Translation failed"
        warning(err)
    except ValueError as err:
        errmsg = "Translation failed"
        warning(err)

    return makeItem(query, subtext=errmsg)

def responseToItem(response, str, source, target, query):
    translation = response.translations[0]
    if source == "auto" and len(targets) > 1 and target == translation.detected_language_code:
        return None

    item = makeItem(
        query, translation.translated_text,
        "Translated to {} from {}".format(
            lang.toName(target),
            lang.toName(translation.detected_language_code if source == "auto" else source)
        )
    )
    item.addAction(ClipAction("Copy to clipboard", item.text))
    item.addAction(UrlAction(
        "View in Google Translate",
        "https://translate.google.com/#{}/{}/{}".format(source, target, quote_url(str, safe=''))
    ))
    return item

def badConfigItem(query, text, subtext):
    item = makeItem(query, text, subtext)
    item.addAction(ProcAction("Open extension config in your editor", ["xdg-open", confPath]))
    item.addAction(UrlAction("View installation instructions",
                             "https://github.com/dshoreman/albert-translate#installation"))
    item.addAction(UrlAction("Create a Google Cloud Platform Project",
                             "https://console.cloud.google.com/projectcreate"))
    item.addAction(UrlAction("Create a Service Account Key",
                             "https://console.cloud.google.com/apis/credentials/serviceaccountkey"))
    return item

def badLanguageItem(query, lang):
    item = makeItem(query, "Translation failed",
                    "{} is not a valid language.".format(lang.upper()))
    item.addAction(UrlAction("Open list of support languages",
                             "https://cloud.google.com/translate/docs/languages"))
    return item

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

    def has(self, code):
        return code in self.languages

    def toCode(self, name):
        return self.languages.keys()[languages.values().index(name)]

    def toName(self, code):
        return self.languages.get(code)

lang = Lang()
