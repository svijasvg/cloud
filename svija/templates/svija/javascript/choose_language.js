//———————————————————————————————————————— template: choose_language.js

function chooseLanguage(flag){
  setCookie('choseLang',   flag, 365);
  location.href=flag;
}

// redirect if conditions are met

// condition: visitor already chose language
var cky = getCookie('choseLang');
var cond1 = cky != '';

// condition: visitor not already on site
var x = 'h'+document.referrer;
var refr_parts = x.split('/');
var page_parts = page_url.split('/');
var cond2 = refr_parts[2] != page_parts[2];

// condition: no subdirectory
var bits = location.href.split('/');
var cond3 = bits.length == 4;

// condition: choice not same as default
var cond4 = cky != '/'+language_code+'/';

// needs to be rewritten to use prefixes from DB
var redir = cky;
if (cond1 && cond2 && cond3 && cond4){
  location.href = redir;
}
