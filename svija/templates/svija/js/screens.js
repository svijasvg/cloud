//———————————————————————————————————————— template: screens.js

/*———————————————————————————————————————— predefined values

  
   defined higher in the page:
  
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

//———————————————————————————————————————— set cookie & redirect if appropriate

if (cookiesEnabled()){

  var isLoggedIn = false
  if (typeof admin != 'undefined')
    if (admin == true) isLoggedIn = true

  var cloudName   = makeCookieName('cloudForce', svija_version)
  var forceCookie = getCookie(cloudName)

  if(forceCookie != 'true' || !isLoggedIn){

    setCookie('screen_code', correct_screen_code, 7);
    
    if (screen_code != correct_screen_code){
      history.scrollRestoration = 'manual';
      window.location.replace(document.URL);
    }
  }
}

//———————————————————————————————————————— fin
