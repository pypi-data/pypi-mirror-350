from .auth import login, logout
from .data import Data, Graph, Histogram, Table
from .file import Artifact, Audio, File, Image, Text, Video
from .init import finish, init
from .sets import Settings
from .sys import System

# TODO: setup preinit

_hooks = []
ops, log, watch, alert = None, None, None, None

__all__ = (
    "Data",
    "Graph",
    "Histogram",
    "Table",
    "File",
    "Artifact",
    "Text",
    "Image",
    "Audio",
    "Video",
    "System",
    "Settings",
    "alert",
    "init",
    "login",
    "logout",
    "watch",
    "finish",
)

__version__ = "0.0.2"
