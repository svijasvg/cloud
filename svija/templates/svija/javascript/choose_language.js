//———————————————————————————————————————— template: choose_language.js

function chooseLanguage(flag){
  setCookie('choseLang',   flag, 365);
  location.href=flag;
}

// redirect to other language?
// needs to be rewritten to use prefixes from DB

var x = 'h'+document.referrer;
refr_parts = x.split('/');
page_parts = page_url.split('/');

// need to add check for NOT internal page to following IF statement

// if visitor is not already on site
if (refr_parts[2] != page_parts[2]){
  if (getCookie('choseLang') == '/fr/' && location.href.indexOf('/en/') > 0) { location.href = '/fr/'; }
  if (getCookie('choseLang') == '/en/' && location.href.indexOf('/fr/') > 0) { location.href = '/en/'; }

  if (getCookie('choseLang') == '/fr/' && location.href.indexOf('/em/') > 0) { location.href = '/fm/'; }
  if (getCookie('choseLang') == '/en/' && location.href.indexOf('/fm/') > 0) { location.href = '/em/'; }
}

// need to know default site language & default language prefix to be able to fix this
// right now it will have no effect because it is only called 
