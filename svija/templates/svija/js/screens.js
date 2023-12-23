//:::::::::::::::::::::::::::::::::::::::: template: screens.js
/*
https://www.toptal.com/developers/javascript-minifier
*/

/*———————————————————————————————————————— notes

    this script checks the current window width against supported
    resolutions and redirects if there's a better fit.

    if cookies are not enabled, nothing is done — the version
    of the page that was loaded is shown.

    if an admin is logged in, and he has clicked on the Svija Cloud
    module to force desktop or mobile, no redirection is done */

/*———————————————————————————————————————— predefined values

  
   defined in system js, higher in the page:
  
   var screen_code = "cp";
   var all_screens = {0:'cp', 400:'mb'}; */

//———————————————————————————————————————— find best fit

var win_width = globalThis.outerWidth;
var correct_screen_code = all_screens[0][1];
var min_value = 1000000;

for (var x=0; x<all_screens.length; x++){
  key   = all_screens[x][0];
  value = all_screens[x][1];
  if (win_width < key && win_width < min_value){
    min_value = key;
    correct_screen_code = value;
  }
}

//———————————————————————————————————————— is an admin logged in?

  if (typeof admin == 'undefined')
    admin = false

/*———————————————————————————————————————— set cookie & redirect if appropriate

    sets cookie with correct screen code for server
    reloads page if there's a better screen match

    UNLESS

    there's a cloud module cookie AND the visitor is a signed-in admin */

if (cookiesEnabled()){

  var cloudModuleCookieName = cookieName('cloudModule', svija_version)
  var cloudModuleCookie     = getCookie(cloudModuleCookieName)

  // if cloud module don't redirect
  if(cloudModuleCookie == 'true' && admin)
    false

  // redirect if necessary
  else if (screen_code != correct_screen_code){
    setCookie('screen_code', correct_screen_code, 7);
    history.scrollRestoration = 'manual';
//  window.location.replace(document.URL);

    var searchStr = 'Googlebot'                                                
    if(window.navigator.userAgent.indexOf(searchStr) > -1)                     
      window.location.replace(document.URL); 
  }
}


//:::::::::::::::::::::::::::::::::::::::: fin
