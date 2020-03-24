import unicodedata
from aqt import gui_hooks

def onBlurOrKey(self, args):
    cmd, ord, nid, txt = args.split(":", 3)
    ord = int(ord)
    try:
        nid = int(nid)
    except ValueError:
        nid = 0
    if nid != self.note.id:
        print("ignored late blur")
        return
    txt = unicodedata.normalize("NFC", txt)
    txt = self.mungeHTML(txt)
    # misbehaving apps may include a null byte in the text
    txt = txt.replace("\x00", "")
    # reverse the url quoting we added to get images to display
    txt = self.mw.col.media.escapeImages(txt, unescape=True)
    self.note.fields[ord] = txt
    if not self.addMode:
        self.note.flush()
        self.mw.requireReset()
    return ord

def onBlur(self, args):
    ord = onBlurOrKey(self, args)
    self.currentField = None
    # run any filters
    if gui_hooks.editor_did_unfocus_field(False, self.note, int(ord)):
        # something updated the note; update it after a subsequent focus
        # event has had time to fire
        self.mw.progress.timer(100, self.loadNoteKeepingFocus, False)
    else:
        self.checkValid()
    return ord
