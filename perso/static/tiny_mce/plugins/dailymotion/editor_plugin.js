(function(){tinymce.PluginManager.requireLangPack('dailymotion');tinymce.create('tinymce.plugins.dailymotionPlugin',{init:function(ed,url){ed.addCommand('mcedailymotion',function(){ed.windowManager.open({file:url+'/dialog.htm',width:320+parseInt(ed.getLang('dailymotion.delta_width',0)),height:120+parseInt(ed.getLang('dailymotion.delta_height',0)),inline:1},{plugin_url:url,some_custom_arg:'custom arg'});});ed.addButton('dailymotion',{title:'dailymotion.desc',cmd:'mcedailymotion',image:url+'/img/dailymotion.gif'});ed.onNodeChange.add(function(ed,cm,n){cm.setActive('dailymotion',n.nodeName=='IMG');});},createControl:function(n,cm){return null;},getInfo:function(){return{longname:'dailymotion plugin',author:'Mark Geurds',authorurl:'http://tinymce.moxiecode.com',infourl:'http://wiki.moxiecode.com/index.php/TinyMCE:Plugins/dailymotion',version:"1.0"};}});tinymce.PluginManager.add('dailymotion',tinymce.plugins.dailymotionPlugin);})();