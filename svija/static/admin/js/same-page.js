/*———————————————————————————————————————— same-page.js

    sends user back to same admin page where they were
    so you can use Svija Sync to easily find your place

    short-lived cookie, only for a day */

//———————————————————————————————————————— sumpin

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

//———————————————————————————————————————— /templates/svija/js/cookies.js

function setCookie(cname, cvalue, exdays) {
  cvalue = escape(cvalue);

//deleteParentCookieIfNecessary(cname, window.location.hostname);

  if (exdays > 7) exdays = 7; // max in Safari

  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));

  var expy = '; expires=' + d.toUTCString();;
  var path = '; path=/';
  var domn = '; domain='  + window.location.hostname;
  var secu = '; samesite=lax; secure;';

  var complete = cvalue + expy + path + domn + secu;

  document.cookie = name+complete;
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
