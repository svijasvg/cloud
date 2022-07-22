/*———————————————————————————————————————— same-page.js

    sends user back to same admin page where they were
    so you can use Svija Sync to easily find your place

    logic:
    
    if you arrive on admin page not from admin page,
    you get sent to the last admin page you visited
 
    short-lived cookie, only for a day */

//———————————————————————————————————————— sumpin

const cname  = 'adminPage';
const exdays = 1;

const ref = document.referrer.substr(-7);
const loc = location.href.substr(-7);
const cky = getCookie(cname);


console.log('referrer: '+ref);
console.log('location: '+loc);
console.log('cookie: '  +cky);

var redirect = true;

if ( cky == ''                            ) redirect = false; // if we don't have cookie
if ( loc != '/admin/' && loc != '/svija/' ) redirect = false; // we're not at top level
if ( ref != ''        && loc != ref       ) redirect = false; // referrer exists & doesn't match location

if (redirect) location.href = cky;

/*—set cookie if:

   not redirecting
   page is not /svija/ or /admin/      */

var earl = window.location.hostname;
var d = new Date();
d.setTime(d.getTime() + (exdays*24*60*60*1000));

if (loc != '/admin/' && loc != '/svija/')
  setCookie(cname, location.href, d, '/',earl, 'samesite=lax; secure;');
else
  setCookie(cname, '', d, '/',earl, 'samesite=lax; secure;');

//———————————————————————————————————————— new cookie function

// https://social.msdn.microsoft.com/Forums/en-US/b949843d-1967-4cff-8a8e-2128ebab6f1c/cookie-path-not-set-correctly-using-safari-and-url-rewriting?forum=asphtmlcssjavascript

function setCookie (name,value,expires,path,theDomain,secure) { 
   value = escape(value);
   var theCookie = value + 
   ((expires)    ? "; expires=" + expires.toGMTString() : "") + 
   ((path)       ? "; path="    + path   : "") + 
   ((theDomain)  ? "; domain="  + theDomain : "") + 
   ((secure)     ? "; secure"   : ""); 

   console.log('cookie "'+name+'" = '+theCookie);
   theCookie = name + "=" + theCookie;

   document.cookie = theCookie;
} 

//———————————————————————————————————————— broken, from template: cookies.js

function xsetCookie(cname, cvalue, exdays) {

  var earl = window.location.hostname;
//  deleteParentCookieIfNecessary(cname, earl);

  if (exdays > 7) exdays = 7; // max in Safari

  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));

  var name = cname + '=' + cvalue + '; ';
  var expy = 'expires=' + d.toUTCString(); + '; ';
  var domn = '; domain=' + earl + '; ';
  var path = 'path=/admin/; ';
  var secu = 'samesite=lax; secure;';

//var complete = name + expy + domn + path + secu;
  var complete = name + expy + path + secu;
console.log(complete);
  document.cookie = complete;
}

//———————————————————————————————————————— template: cookies.js

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

//———————————————————————————————————————— template: cookies.js

function deleteParentCookieIfNecessary(cname, domain){
  var parts = domain.split('.');
  if (parts.length > 2){ // on subdomain
    var domain = parts.slice(-2).join('.');
    document.cookie = cname + '=;domain=.' + domain + ';path=/;max-age=0';
  }
}
