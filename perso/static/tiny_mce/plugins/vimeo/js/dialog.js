tinyMCEPopup.requireLangPack();

var VimeoDialog = {
    init : function() {
    },

    insert : function() {
        // Insert the contents from the input into the document
        var embedCode = '<iframe src="//player.vimeo.com/video/'+document.forms[0].vimeoID.value+'" width="'+document.forms[0].vimeoWidth.value+'" height="'+document.forms[0].vimeoHeight.value+'" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>'
        tinyMCEPopup.editor.execCommand('mceInsertRawHTML', false, embedCode);
        tinyMCEPopup.close();
    }
};

tinyMCEPopup.onInit.add(VimeoDialog.init, VimeoDialog);
