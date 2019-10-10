//———————————————————————————————————————— serverside: choose_language.js
// javascript:chooseLanguage('/fr/');

function chooseLanguage(flag){
  setCookie('choseLang',   flag, 365);
  location.href=flag;
}

//---------------------------------------- redirect to other language?

if (getCookie('choseLang') == '/fr/' && location.href.indexOf('/en/') > 0) { location.href = '/fr/'; }
if (getCookie('choseLang') == '/en/' && location.href.indexOf('/fr/') > 0) { location.href = '/en/'; }

if (getCookie('choseLang') == '/fr/' && location.href.indexOf('/em/') > 0) { location.href = '/fm/'; }
if (getCookie('choseLang') == '/en/' && location.href.indexOf('/fm/') > 0) { location.href = '/em/'; }
