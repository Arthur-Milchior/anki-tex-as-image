import json

from anki.latex import render_latex

from aqt import gui_hooks

from typing import Tuple, Any, Union
from . import web_export
from aqt.editor import Editor

def texify(original_field, editor):
    model = editor.note.model()
    col = editor.note.col
    return editor.mw.col.media.escapeImages(
        render_latex(original_field, model, col))
    

def setTexedAndOriginalFields(js, note, editor):
    """ Send all fields with tex replaced by images"""
    original_fields = [original_field for fld_name, original_field in note.items()]
    texed_fields = [
        texify(original_field, editor)
        for original_field in original_fields
    ]
    js = f"""
    changing_note = true;
    {js}
    setTexedAndOriginalFields({json.dumps(texed_fields)}, {json.dumps(original_fields)});
    changing_note=false;"""
    return js

gui_hooks.editor_will_load_note.append(setTexedAndOriginalFields)

def onBridgeCmd(handled: Tuple[bool, Any], message: str, editor: Union[Editor, Any]):
    if not (isinstance(editor, Editor) and message.startswith("blur")):
        return handled
    (type, ord_str, nid_str, original_field) = message.split(":", 3)
    ord = int(ord_str)
    nid = int(nid_str)
    if nid != editor.note.id:
        return
    texed_field = texify(original_field, editor)
    editor.web.eval(f"updateTexAndOriginalField({ord}, {json.dumps(original_field)}, {json.dumps(texed_field)}, {nid});")
    return handled

gui_hooks.webview_did_receive_js_message.append(onBridgeCmd)
