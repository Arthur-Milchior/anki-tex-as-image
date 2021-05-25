var texedFields = [];
var originalFields = [];
var changing_note = false;

/** Editing area containing the editable*/
function editableToEditingArea(editable) {
    return editable.parentNode.host;
}

/** Ord of an editable*/
function editableToOrd(editable) {
    return editableToEditingArea(editable).ord;
}

/**
Executed with a field got focus. Ensure its original value is set back. Also ensure that on second focus, nothing occurs anymore.
 */
function onFocusTex(event) {
    if (changing_note) {
        return;
    }
    const editable = event.target;
    const ord = editableToOrd(editable);
    const $editable = $(editable);
    $editable.off("focus", onFocusTex);
    original_field = originalFields[ord];
    editable.fieldHTML = original_field;
}    

/** 
    When python get information about a field update due to a blur, it sends back the informaiton here, so that we know
    the new version with tex replaced by image. It also ensure that original_field is exactly what is saved in the
    database, even if it is probably redundant since it should be in the editable inner html.

    It set back the field to a version with latex and mathjax replaced by images and ensure that on focus, the original is set back.
*/
function updateTexAndOriginalField(ord, original_field, texed_field, nid) { // EditorField, txt/html
    current_nid = getNoteId();
    if (changing_note || nid != current_nid) {
        return;
    }
    originalFields[ord] = original_field;
    texedFields[ord] = texed_field;
    const editorField = getEditorField(ord);
    setTexAndOriginalField(editorField, texed_field);
}

/**
   Take a field (editor field) and the version with tex. If the field is not currently selected, replace it with the
   version with latex replaced by image and mathjax interpreted. Ensure that original is reset when focus is gained.
 */
function setTexAndOriginalField(field, texed_field) { // EditorField, txt/html
    const editingArea = field.editingArea;
    const shadowRoot = editingArea.shadowRoot;
    
    const ord = editingArea.ord;
    const editable = editingArea.editable;

    currentField = getCurrentField(); // EditingArea
    currentOrd = (currentField == null)? -1:currentField.ord;

    if (ord == currentOrd) {
        return;
    } 
    editingArea.fieldHTML = texed_field;
    typeset([editable]);

    $editable = $(editable);
    $editable.on("focus", onFocusTex);
};

/**
   Take the original fields and the version with tex replaced by image, save them in originalFields and texedFields, and
   replace all fields that are not selected by the texed version with mathjax interpreted. Ensure that if focus is put in a field, the original is reset there.
 */
function setTexedAndOriginalFields(texed_fields, original_fields) { // txt/html[], txt/html[],
    texedFields = texed_fields;
    originalFields = original_fields;
    forEditorField(texed_fields, setTexAndOriginalField);
}

