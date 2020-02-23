import json
import os.path

from anki.hooks import runHook, wrap
from anki.latex import render_latex
from aqt.editor import Editor
from aqt.qt import *

from .from_file import str_from_file_name


def loadNote(self, focusTo=None):
    """Todo
     focusTo -- Whether focus should be set to some field."""
    if not self.note:
        return

    data = []
    for fld, val in list(self.note.items()):
        fldContent = self.mw.col.media.escapeImages(val)
        fldContentTexProcessed = self.mw.col.media.escapeImages(
            render_latex(val, self.note.model(), self.note.col))
        data.append((
            fld,
            fldContent,
            fldContentTexProcessed
        ))
        # field name, field content modified so that it's image's url can be used locally.
    print(f"data is {data}")
    self.widget.show()
    self.updateTags()

    def oncallback(arg):
        if not self.note:
            return
        self.setupForegroundButton()
        self.checkValid()
        if focusTo is not None:
            self.web.setFocus()
        runHook("loadNote", self)

    self.web.evalWithCallback("set_fields_tex(%s); setFonts(%s); focusField(%s); setNoteId(%s)" % (
        json.dumps(data),
        json.dumps(self.fonts()), json.dumps(focusTo),
        json.dumps(self.note.id)),
        oncallback)


Editor.loadNote = loadNote


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
