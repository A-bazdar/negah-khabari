/**
 * Created by Morteza on 13/03/2016.
 */

function copy_to_clipboard(elem) {
    var origSelectionStart, origSelectionEnd;
    origSelectionStart = elem.selectionStart;
    origSelectionEnd = elem.selectionEnd;
    var currentFocus = document.activeElement;
    elem.focus();
    elem.setSelectionRange(0, elem.value.length);

    var succeed;
    try {
    	  succeed = document.execCommand("copy");
    } catch(e) {
        succeed = false;
    }
    if (currentFocus && typeof currentFocus.focus === "function") {
        currentFocus.focus();
    }

    elem.setSelectionRange(origSelectionStart, origSelectionEnd);
    return succeed;
}

$(document).on('click','.copy_to_clipboard', function(){
    copy_to_clipboard(document.getElementById('copy_to_clipboard_input'));
});