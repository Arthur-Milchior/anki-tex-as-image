import json
import os.path

from .anki_code import onBlur
from anki.hooks import runHook, wrap
from anki.latex import render_latex
from aqt import gui_hooks, mw
from aqt.editor import Editor
from aqt.webview import WebContent

mw.addonManager.setWebExports(__name__, r"web/.*(css|js)")
addon_package = mw.addonManager.addonFromModule(__name__)


def note_loaded(editor):
    items = editor.note.items()
    model = editor.note.model()
    col = editor.note.col
    fldContentTexProcessed = [
        editor.mw.col.media.escapeImages(
            render_latex(val, model, col))
        for fld, val in items
    ]
    dumped = json.dumps(fldContentTexProcessed)
    editor.web.eval(f"""set_texs({dumped});""")


gui_hooks.editor_did_load_note.append(note_loaded)


def onBridgeCmd(handled, message, editor):
    if isinstance(editor, Editor) and message.startswith("blur"):
        ord = onBlur(editor, message)
        val = editor.note.fields[int(ord)]
        fldContent = editor.mw.col.media.escapeImages(val)
        fldContentTexProcessed = editor.mw.col.media.escapeImages(
            render_latex(val, editor.note.model(), editor.note.col))
        s = f"set_tex({ord}, {json.dumps(fldContent)}, {json.dumps(fldContentTexProcessed)});"
        print(s)
        editor.web.eval(s)
        return (True, None)
    # Handling does not actually change. Actual work for blur must still be done
    return handled


gui_hooks.webview_did_receive_js_message.append(onBridgeCmd)


def on_webview_will_set_content(web_content: WebContent, editor):
    if isinstance(editor, Editor):
        web_content.js.append(f"/_addons/{addon_package}/web/js.js")


gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
