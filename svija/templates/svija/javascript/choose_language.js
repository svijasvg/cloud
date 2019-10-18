//———————————————————————————————————————— template: choose_language.js

function chooseLanguage(flag){
  setCookie('choseLang',   flag, 365);
  location.href=flag;
}

// redirect if 4 conditions are met

// condition 1: visitor not already on site

var x = 'h'+document.referrer;
var refr_parts = x.split('/');
var page_parts = page_url.split('/');
var cond1 = refr_parts[2] != page_parts[2];

// condition 2: there's no subdirectory

var bits = location.href.split('/');
var cond2 = bits.length == 4;

// condition 3: cookie choice is not same as default prefix
//              or there is no cookie choice

var cky = getCookie('choseLang');
var pfx = '/'+default_site_prefix+'/';
if (cky == ''){ cky = pfx; }
var cond3 = cky != pfx;

// condition 4: we're not already on mobile version of correct language if desktop is default or desktop if mobile is default
// this could only happen if mobile version was default prefix
// chooseLanguage should choose language, not prefix
// then I could get prefixes & check all of them

var cond4 = false

// needs to be rewritten to use prefixes from DB
if (cond1 && cond2 && cond3 && cond4){
  location.href = cky;
}
