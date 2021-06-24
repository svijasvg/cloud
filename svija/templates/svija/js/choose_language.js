//———————————————————————————————————————— template: choose_language.js

// cookie would contain /fr/ for example

// used by menus when one clicks on flag

function chooseLanguage(flag){
  setCookie('choseLang',   flag, 365);
  location.href=flag;
}

//———————————————————————————————————————— redirect if 4 conditions are met

// condition: visitor already chose language
var redir = getCookie('choseLang');
var cond1 = redir != '';

// condition: visitor not already on site
var x = 'h'+document.referrer;
var refr_parts = x.split('/');
var page_parts = page_url.split('/');
var cond2 = refr_parts[2] != page_parts[2];

// condition: no subdirectory
var bits = location.href.split('/');
var cond3 = bits.length == 4;

// condition: choice not same as default
var cond4 = redir != '/'+language_code+'/';

// needs to be rewritten to use prefixes from DB
if (cond1 && cond2 && cond3 && cond4){
  location.href = redir.slice(1);
}
