
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

/*———————————————————————————————————————— predefined values
  
   defined in system js, higher in the page:
  
   var screen_code = "cp"
   var all_screens = {0:'cp', 400:'mb'} */


correct_code = calculate_code(all_screens)
first_visit  = false

recalculate: if (cookiesEnabled()){

/*———————————————————————————————————————— prolong cookie if set */

  if (typeof localStorage.screen_code != 'undefined'){
    setCookie('screen_code', localStorage.screen_code, 7)
    break recalculate
  }

/*———————————————————————————————————————— first visit */

  // store code for next visit

  localStorage.screen_code = correct_code
  setCookie('screen_code', correct_code, 7)
  first_visit = true


}

// added separately in screen_redirect_js.py view module:

// code = 'if (cookiesEnabled()) if (screen_code != correct_code) window.location.replace(document.URL)'


/*:::::::::::::::::::::::::::::::::::::::: functions */

/*———————————————————————————————————————— calculate_code(all_screens)

    */

function calculate_code(all_screens){
  var win_width = globalThis.outerWidth
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


/*:::::::::::::::::::::::::::::::::::::::: fin */

