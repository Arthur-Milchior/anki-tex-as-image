var original_fields = [];

function on_focus_tex(elem) {
    /*
       Called when focus is set to the field `elem`.

       If the field is not changed, nothing occurs.
       Otherwise, set currentField value, warns python of it.
       Change buttons.
       If the change is note made by mouse, then move caret to end of field, and move the window to show the field.

     */
    var previousCurrentField = currentField;
    currentField = elem;
    var ord = currentFieldOrdinal()
    var field = original_fields[ord];
    if (field !== null) {
        elem.innerHTML = field;
        original_fields[ord] = null;
    }
    if (previousCurrentField === elem) {
        // anki window refocused; current element unchanged
        return;
    }
    pycmd("focus:" + ord);
    enableButtons();
    // don't adjust cursor on mouse clicks
    if (mouseDown) {
        return;
    }
    // do this twice so that there's no flicker on newer versions
    caretToEnd();
    // scroll if bottom of element off the screen
    function pos(obj) {
        var cur = 0;
        do {
            cur += obj.offsetTop;
        } while (obj = obj.offsetParent);
        return cur;
    }

    var y = pos(elem);
    if ((window.pageYOffset + window.innerHeight) < (y + elem.offsetHeight) ||
        window.pageYOffset > y) {
        window.scroll(0, y + elem.offsetHeight - window.innerHeight);
    }
}

function current_field_ordinal_aux() {
    if (currentField) {
        return currentField.id.substring(1);
    } else {
        return null;
    }
}

function set_field(ord, fieldValue, fieldValueTexProcessed) {
    var currentOrd = current_field_ordinal_aux();
    if (currentOrd == ord) {
        return;
    }
    if (!fieldValue) {
        fieldValue = "<br>";
    }
    original_fields[ord] = fieldValue;
    if (!fieldValueTexProcessed) {
        fieldValueTexProcessed = "<br>";
    }
    field = $("#f"+ord);
    field.html(fieldValueTexProcessed);

}

function set_fields_tex(fields) {
    var txt = "";
    original_fields = [];
    for (var i = 0; i < fields.length; i++) {
        var n = fields[i][0];
        var f = fields[i][1];
        if (!f) {
            f = "<br>";
        }
        original_fields[i] = f;
        var fTex = fields[i][2];
        if (!fTex) {
            fTex = "<br>";
        }
        txt += "<tr><td class=fname>{0}</td></tr><tr><td width=100%>".format(n);
        txt += "<div id=f{0} onkeydown='onKey();' oninput='onInput()' onmouseup='onKey();'".format(i);
        txt += " onfocus='on_focus_tex(this);' onblur='onBlur();' class='field clearfix' ";
        txt += "ondragover='onDragOver(this);' onpaste='onPaste(this);' ";
        txt += "oncopy='onCutOrCopy(this);' oncut='onCutOrCopy(this);' ";
        txt += "contentEditable=true class=field>{0}</div>".format(fTex);
        txt += "</td></tr>";
    }
    $("#fields").html("<table cellpadding=0 width=100% style='table-layout: fixed;'>" + txt + "</table>");
    maybeDisableButtons();
}
