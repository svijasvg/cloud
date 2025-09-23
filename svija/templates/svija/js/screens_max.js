
/* vim: set foldmethod=marker fmr=/*—,///: */  

/*:::::::::::::::::::::::::::::::::::::::: template: screens.js

    https://www.toptal.com/developers/javascript-minifier */

/*———————————————————————————————————————— notes

    this script checks the current window width against supported
    resolutions and redirects if there's a better fit.

    if cookies are not enabled, nothing is done — the version
    of the page that was loaded is shown.

    if a screen code exists in localStorage or a cookie,
    the cookie is renewed and localStorage is set

    if no cookie or localStorage, the correct screen is determined
    and the screen code is stored in localStorage and a cookie. */
///
/*———————————————————————————————————————— notes
  
    defined in system js at top of page:
   
    var screen_code = "cp"
    var all_screens = {0:'cp', 400:'mb'}
 
    correct_code: set by screens_max.js
 
    —————————————————————————————————————
 
    three related scripts:
 
    1. templates/svija/js/screens_max.js
 
    2. views/modules/screen_redirect_js.py
 
       if it's a fresh start & page doesn't match
       correct code, reload page (if not google)
 
    3. templates/svija/js/cloud_module_max.js 
 
       sets cookie & localStorage to new screen code 
       to enable visiting a page with "wrong" code

///
/*———————————————————————————————————————— functioning

    CLOUD MODULE WORKS BY SETTING SCREEN CODE IN LOCALSTORAGE
    IF LOCALSTORAGE DOESN'T MATCH CORRECT CODE
    DO NOT AUTOMATICALLY REDIRECT 

    1. deletes invalid saved screen code, if any

    2. determines correct screen code

    3A. if localStorage is set do nothing but renew cookie

    3B. else set cookie & localStorage to correct code

///
/*———————————————————————————————————————— clear invalid values

    during updates, screen codes can change */

if (typeof localStorage.screen_code != 'undefined')
  if (invalid_screen(localStorage.screen_code, all_screens)){
    localStorage.removeItem('screen_code')
    setCookie('screen_code', '', 7)
    alert('invalid screen code unset')
  }
///
/*———————————————————————————————————————— */

correct_code = determine_code(all_screens)
///
/*———————————————————————————————————————— prolong cookie if set */

fresh_start  = false

recalculate: if (cookiesEnabled()){

  // there's an existing screen code, so we just renew the cookie and get out
  if (typeof localStorage.screen_code != 'undefined'){
    setCookie('screen_code', localStorage.screen_code, 7)
    break recalculate
  }

  // it's a fresh start, so we store code
  localStorage.screen_code = correct_code
  setCookie('screen_code', correct_code, 7)
  fresh_start = true

}
///

/*:::::::::::::::::::::::::::::::::::::::: functions */

/*———————————————————————————————————————— determine_code(all_screens)

    */

function determine_code(all_screens){

//var win_width = globalThis.outerWidth // DO NOT USE — IN CHROME THIS IS UNSET BEFORE DRAWING

  var win_width = width = window.innerWidth || document.documentElement.clientWidth
  var      code = all_screens[0][1]
  var min_value = 999999
  
  for (var x=0; x<all_screens.length; x++){

      key = all_screens[x][0]
    value = all_screens[x][1]

    if (win_width < key && win_width < min_value){
      min_value = key
      code = value
    }
  }

  return code
}
///
/*———————————————————————————————————————— invalid_screen(code, all_screens)

in system js:

    var all_screens = [[0, "cp", "Computer"], [500, "mb", "Mobile"]] */


function invalid_screen(code, all_screens){

  for(let x=0; x<all_screens.length; x++)
    if (code == all_screens[x][1]) return false

  return true
}
///

/*:::::::::::::::::::::::::::::::::::::::: fin */

