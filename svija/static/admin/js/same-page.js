/*———————————————————————————————————————— same-page.js

    sends user back to same admin page where they were
    so you can use Svija Sync to easily find your place

    short-lived cookie, only for a day */

//———————————————————————————————————————— sumpin

console.log('line 10 of same-page.js');

const cname  = 'adminPage';
const exdays = 1;

const ref = document.referrer.substr(-7);
const loc = location.href.substr(-7);
const cky = getCookie(cname);

var redirect = true;

if ( cky == ''                            ) redirect = false; // if we don't have cookie
if ( loc != '/admin/' && loc != '/svija/' ) redirect = false; // we're not at top level
if ( ref != ''        && loc != ref       ) redirect = false; // referrer exists & doesn't match location

if (redirect) location.href = cky;

if (loc != '/admin/' && loc != '/svija/') setCookie(cname, location.href, 1); // if we're on a page worth remembering
else                                      setCookie(cname, '',            1); // else delete cookie

//———————————————————————————————————————— new cookie function

// https://social.msdn.microsoft.com/Forums/en-US/b949843d-1967-4cff-8a8e-2128ebab6f1c/cookie-path-not-set-correctly-using-safari-and-url-rewriting?forum=asphtmlcssjavascript

//———————————————————————————————————————— template: cookies.js

// same code in static/admin/js/same-page.js
//              templates/svija/js/cookies.js

function setCookie(name, value, expires) {
  value = escape(value);

//deleteParentCookieIfNecessary(name, window.location.hostname);

  if (expires > 7) expires = 7; // max in Safari

  var d = new Date();
  d.setTime(d.getTime() + (expires*24*60*60*1000));

  var expy = '; expires=' + d.toUTCString();
  var path = '; path=/';
  var domn = '; domain='  + window.location.hostname;
  var secu = '; samesite=lax; secure;';

  var complete = value + expy + path + domn + secu;
  document.cookie = name + '=' + complete;
}

function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i=0; i<ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0)==' ') c = c.substring(1);
    if (c.indexOf(name) != -1) return unescape(c.substring(name.length,c.length));
  }
  return "";
}

function deleteParentCookieIfNecessary(cname, domain){
  var parts = domain.split('.');
  if (parts.length > 2){ // on subdomain
    var domain = parts.slice(-2).join('.');
    document.cookie = cname + '=;domain=.' + domain + ';path=/;max-age=0';
  }
}
