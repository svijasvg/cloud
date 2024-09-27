/*:::::::::::::::::::::::::::::::::::::::: template: cookies.js

https://www.toptal.com/developers/javascript-minifier  */

/*———————————————————————————————————————— notes

    This script has no effect — in contains four functions used for
    working with cookies:

    setCookie(name, value, expDays)
      sets a cookie

    getCookie(cname)
      gets a cookie

    cookiesEnabled()
      returns true if cookies enabled, else false
 
    deleteParentCookieIfNecessary(cname, domain)
      not currently used (was called by setCookie)
      was used to delete cookies for svija.com when visiting dev.svija.com      
      because such cookies caused conflicts

    cookieName(unique, version)
      creats a unique cookie name by concatenating unique+verion without periods */


//:::::::::::::::::::::::::::::::::::::::: main methods

/*———————————————————————————————————————— setCookie(name, value, expDays)

// same code in static/admin/js/same-page.js
//              templates/svija/js/cookies.js */

function setCookie(name, value, expDays) {
  value = escape(value);

//deleteParentCookieIfNecessary(name, window.location.hostname);

  if (expDays > 7) expDays = 7; // max in Safari

  var d = new Date();
  d.setTime(d.getTime() + (expDays*24*60*60*1000));

  var expy = '; expires=' + d.toUTCString();
  var path = '; path=/';
  var domn = '; domain='  + window.location.hostname;

// var secu = '; SameSite=Lax; Secure;';
// secu deprecated: developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite
// var complete = value + expy + path + domn + secu;

  var complete = value + expy + path + domn;
  document.cookie = name + '=' + complete;
}

/*———————————————————————————————————————— getCookie(cname)
    */

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

//———————————————————————————————————————— cookiesEnabled()

// https://stackoverflow.com/questions/63471777/testing-function-which-checks-if-cookies-are-enabled-with-qunit

function cookiesEnabled() {

  if (navigator.cookieEnabled) {
      document.cookie = "test_cookie";
      if (document.cookie.indexOf("test_cookie") != -1)
        return true;
  }

  return false;
}

/*———————————————————————————————————————— cookieName(unique, version)

    creates a name composed of unique + version, with periods removed

    alert('makeCookeiName: ' + cookieName('svija', svija_version)) */

function cookieName(unique, version){
  version = version.replaceAll('.','')
  var res = unique+version
  return res
}


//:::::::::::::::::::::::::::::::::::::::: utility methods

//———————————————————————————————————————— deleteParentCookieIfNecessary(cname, domain)

function deleteParentCookieIfNecessary(cname, domain){
  var parts = domain.split('.');
  if (parts.length > 2){ // on subdomain
    var domain = parts.slice(-2).join('.');
    document.cookie = cname + '=;domain=.' + domain + ';path=/;max-age=0';
  }
}


//:::::::::::::::::::::::::::::::::::::::: fin

