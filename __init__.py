import json
import os.path

from anki.hooks import runHook, wrap
from anki.latex import render_latex
from aqt import gui_hooks
from aqt.editor import Editor
from aqt.qt import *

from .from_file import str_from_file_name


def note_loaded(editor):
    note = editor.note
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


def setupWeb(self):
    self.web.eval(str_from_file_name("js.js"))


Editor.setupWeb = wrap(Editor.setupWeb, setupWeb)

oldBridgeCmd = Editor.onBridgeCmd


def onBridgeCmd(self, cmd):
    r = oldBridgeCmd(self, cmd)
    if cmd.startswith("blur"):
        (type, ord, txt) = cmd.split(":", 2)
        val = self.note.fields[int(ord)]
        fldContent = self.mw.col.media.escapeImages(val)
        fldContentTexProcessed = self.mw.col.media.escapeImages(
            render_latex(val, self.note.model(), self.note.col))
        self.web.eval(
            f"set_field({ord}, {json.dumps(fldContent)}, {json.dumps(fldContentTexProcessed)});")
    return r


Editor.onBridgeCmd = onBridgeCmd
