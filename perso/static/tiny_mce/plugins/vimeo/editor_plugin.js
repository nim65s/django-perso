(function(){tinymce.PluginManager.requireLangPack('vimeo');tinymce.create('tinymce.plugins.VimeoPlugin',{init:function(ed,url){ed.addCommand('mceVimeo',function(){ed.windowManager.open({file:url+'/dialog.htm',width:320+parseInt(ed.getLang('vimeo.delta_width',0)),height:120+parseInt(ed.getLang('vimeo.delta_height',0)),inline:1},{plugin_url:url,some_custom_arg:'custom arg'});});ed.addButton('vimeo',{title:'vimeo.desc',cmd:'mceVimeo',image:url+'/img/vimeo.gif'});ed.onNodeChange.add(function(ed,cm,n){cm.setActive('vimeo',n.nodeName=='IMG');});},createControl:function(n,cm){return null;},getInfo:function(){return{longname:'Vimeo plugin',author:'Guilhem Saurel',authorurl:'http://saurel.me',infourl:'http://saurel.me',version:"1.0"};}});tinymce.PluginManager.add('vimeo',tinymce.plugins.VimeoPlugin);})();