from aqt import gui_hooks, mw
from aqt.webview import WebContent
from aqt.editor import Editor
from typing import Union, Any




mw.addonManager.setWebExports(__name__, r".*(css|js)")
addon_package = mw.addonManager.addonFromModule(__name__)

def on_webview_will_set_content(web_content: WebContent, editor: Union[Editor, Any]):
    if not isinstance(editor, Editor):
        return
    web_content.js.append(f"/_addons/{addon_package}/js.js")
    web_content.js.append("js/mathjax.js")
    web_content.js.append(f"/_addons/{addon_package}/mathjax.js")
    web_content.js.append("js/vendor/mathjax/tex-chtml.js")


gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
