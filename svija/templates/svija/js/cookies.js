//———————————————————————————————————————— template: cookies.js

function setCookie(cname, cvalue, exdays) {

  var earl = window.location.hostname;
//  deleteParentCookieIfNecessary(cname, earl);

  if (exdays > 7) exdays = 7; // max in Safari

  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));

  var name = cname + '=' + cvalue + '; ';
  var expy = 'expires=' + d.toUTCString(); + '; ';
  var domn = '; domain=' + earl + '; ';
  var path = 'path=/; ';
  var secu = 'samesite=lax; secure;';

  

//var complete = name + expy + domn + path + secu;
  var complete = name + expy + path + secu;
  document.cookie = complete;
}

function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i=0; i<ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0)==' ') c = c.substring(1);
    if (c.indexOf(name) != -1) return c.substring(name.length,c.length);
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
