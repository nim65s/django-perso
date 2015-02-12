tinyMCEPopup.requireLangPack();

var dailymotionDialog = {
    init : function() {
    },

    insert : function() {
        // Insert the contents from the input into the document
        var embedCode = '<iframe width="'+document.forms[0].dailymotionWidth.value+'" height="'+document.forms[0].dailymotionHeight.value+'" src="//www.dailymotion.com/embed/video/'+document.forms[0].dailymotionID.value+'" frameborder="0" allowfullscreen></iframe>';
        tinyMCEPopup.editor.execCommand('mceInsertRawHTML', false, embedCode);
        tinyMCEPopup.close();
    }
};

tinyMCEPopup.onInit.add(dailymotionDialog.init, dailymotionDialog);
