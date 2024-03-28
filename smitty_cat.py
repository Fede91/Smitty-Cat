from pydantic import BaseModel
from cat.mad_hatter.decorators import plugin, hook
from cat.mad_hatter.plugin import Plugin as smittyPlugin
import os

class SmittyCatSettings(BaseModel):

    project_name: str = ""
    api_key: str = ""
    tracing_v2: bool = False

@plugin
def settings_model():
    return SmittyCatSettings

@plugin
def save_settings(settings):
    tracing_v2 = settings.get("tracing_v2")
    if(tracing_v2):
        api_key = settings.get("api_key")
        project_name = settings.get("project_name")
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_PROJECT"] = project_name
        os.environ["LANGCHAIN_API_KEY"] = api_key
    else:
        if "LANGCHAIN_TRACING_V2" in os.environ:
            del os.environ["LANGCHAIN_TRACING_V2"]
        if "LANGCHAIN_PROJECT" in os.environ:
            del os.environ["LANGCHAIN_PROJECT"]
        if "LANGCHAIN_API_KEY" in os.environ:
            del os.environ["LANGCHAIN_API_KEY"]

    plugin_folder = os.path.dirname(os.path.realpath(__file__))
    this_plugin = smittyPlugin(plugin_folder)
    this_plugin.save_settings(settings)
    return settings

@plugin
def deactivated(plugin):
    if "LANGCHAIN_TRACING_V2" in os.environ:
        del os.environ["LANGCHAIN_TRACING_V2"]
    if "LANGCHAIN_PROJECT" in os.environ:
        del os.environ["LANGCHAIN_PROJECT"]
    if "LANGCHAIN_API_KEY" in os.environ:
        del os.environ["LANGCHAIN_API_KEY"]

# Load settings
plugin_folder = os.path.dirname(os.path.realpath(__file__))
this_plugin = smittyPlugin(plugin_folder)
settings = this_plugin.load_settings()
tracing_v2 = settings.get("tracing_v2")

if(tracing_v2):
    api_key = settings["api_key"]
    project_name = settings["project_name"]
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = project_name
    os.environ["LANGCHAIN_API_KEY"] = api_key
