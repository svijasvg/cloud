//———————————————————————————————————————— template: cookies.js

function setCookie(cname, cvalue, exdays) {

  if (exdays > 7) exdays = 7; // max in Safari

  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));

  var name = cname + '=' + cvalue + '; ';
  var expy = 'expires=' + d.toUTCString(); + '; ';
  var domn = '; domain=' + window.location.hostname + '; ';
  var path = '/; ';
//var secr = 'secure;';
  var secr = '';

  document.cookie = name + expy + domn + path + secr;
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
