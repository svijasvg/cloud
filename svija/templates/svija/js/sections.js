//———————————————————————————————————————— template: sections.js
//
//   cookie would contain fr for example
//   used by menus when one clicks on flag
//
//———————————————————————————————————————— redirect if 4 conditions are met

// condition: visitor already chose section
var cookie_code = getCookie('section_code');

var x = 'h'+document.referrer;
var referring_host = x.split('/')[2];
var current_host = page_url.split('/')[2];

var path_parts = location.href.split('/');

//———————————————————————————————————————— four conditions

var cond1 =       cookie_code != '';
var cond2 =    referring_host != current_host;
var cond3 = path_parts.length == 4;
var cond4 =       cookie_code != section_code;

//———————————————————————————————————————— redirect if appropriate

if (cond1 && cond2 && cond3 && cond4){
  location.href = '/' + cookie_code
}

//———————————————————————————————————————— function

function chooseSection(code){
  setCookie('section_code', code, 7);
  location.href = '/' + code;
}
