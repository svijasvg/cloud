//———————————————————————————————————————— template: cookies.js

function setCookie(cname, cvalue, exdays) {

  if (exdays > 7) exdays = 7; // max in Safari

  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));

  var name = cname + '=' + cvalue + '; ';
  var expy = 'expires=' + d.toUTCString(); + '; ';
  var domn = '; domain=' + window.location.hostname + '; ';
  var path = 'path=/; ';
  var secu = 'samesite=lax; secure;';

  var complete = name + expy + domn + path + secr;
  // alert('setting: '+complete);
  // screen_code=mb; expires=Fri, 29 Oct 2021 08:54:53 GMT; domain=svija.dev; /; 
  document.cookie = name + expy + domn + path + secu;
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


// screen_code=mb;
// csrftoken=ul3cs75jZmvmDx7bkw9NPRGOU2n8FMV0sBugyA4DIZ83dWvoa9qrWzaNiS5GZuk4;
// screen_code=cp
