/**
Contains the original fields, as in the note database. Or None if this
value is already in the field.
*/
var original_fields = [];

function on_focus_tex(event) {
    /*
       Called when focus is set to the field `elem`.

       If the field is not changed, nothing occurs.
       Otherwise, set currentField value, warns python of it.
       Change buttons.
       If the change is note made by mouse, then move caret to end of field, and move the window to show the field.

    */
    elem = event.target;
    currentField = elem;
    var ord = currentFieldOrdinal();
    on_focus_field(ord);
}

function on_focus_field(ord) {
    var field_content = original_fields[ord];
    var $field = $("#f"+ord);
    if (field_content !== null) {
        $field.html(field_content);
        original_fields[ord] = null;
    }
}

function current_field_ordinal_aux() {
    if (currentField) {
        return currentField.id.substring(1);
    } else {
        return null;
    }
}

function set_tex(ord, fieldValue, fieldValueTexProcessed) {
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
    $field = $("#f"+ord);
    $field.html(fieldValueTexProcessed);
    MathJax.Hub.Queue(["Typeset", MathJax.Hub,`f${ord}`]);
}

function set_texs(tex){
    nb_fields = tex.length;
    original_fields = new Array(nb_fields);
    for (var i = 0; i < nb_fields; i++) {
        fieldValue = tex[i];
        if (fieldValue === "") {
            fieldValue = "<br>";
        }
        $div = $("#f" + i);
        original_fields[i] = $div.html();
        $div.html(fieldValue);
        $div.focus(on_focus_tex);
        MathJax.Hub.Queue(["Typeset", MathJax.Hub,`f${i}`]);
    }
}
