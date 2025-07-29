from pathlib import Path
from typing import Literal

_THIS_DIR = Path(__file__).parent
_TEMPLATES_DIR = _THIS_DIR.joinpath("templates")
_STATIC_DIR = _THIS_DIR.joinpath("static")

INDEX_TEMPLATE_PATH = _TEMPLATES_DIR.joinpath("index.html")
APP_IIFE_JS_PATH = _STATIC_DIR.joinpath("insta-ui.iife.js")
APP_ES_JS_PATH = _STATIC_DIR.joinpath("insta-ui.esm-browser.prod.js")
APP_ES_JS_MAP_PATH = _STATIC_DIR.joinpath("insta-ui.js.map")
APP_CSS_PATH = _STATIC_DIR.joinpath("insta-ui.css")
VUE_IIFE_JS_PATH = _STATIC_DIR.joinpath("vue.global.prod.js")
VUE_ES_JS_PATH = _STATIC_DIR.joinpath("vue.esm-browser.prod.js")
VUE_ES_RUNTIME_JS_PATH = _STATIC_DIR.joinpath("vue.runtime.esm-browser.prod.js")
FAVICON_PATH = _STATIC_DIR.joinpath("insta-ui.ico")
# tools
TOOLS_BROWSER_JS_PATH = _STATIC_DIR.joinpath("instaui-tools-browser.js")

PAGE_TITLE = "insta-ui"

_T_App_Mode = Literal["zero", "web", "webview"]
TModifier = Literal["trim", "number", "lazy"]
