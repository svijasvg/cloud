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
