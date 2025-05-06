<script>

/*:::::::::::::::::::::::::::::::::::::::: cloud_component.js

/*———————————————————————————————————————— notes

    https://www.toptal.com/developers/javascript-minifier

    Cloud Component contains 5 links:

    1. logo        mouse/cloudComponentLink/n          /cloud/svija/
    2. pages       mouse/cloudComponentLink/n/func
    3. components  mouse/cloudComponentLink/n          /cloud/svija/module/
    4. fonts       mouse/cloudComponentLink/n          /cloud/svija/font/
    5. mobile      mouse/cloudForceLink/func/mb

    this script handles the PAGES and MOBILE link */


//:::::::::::::::::::::::::::::::::::::::: link functions

/*———————————————————————————————————————— page link

    only used for pages, to go directly to the page being
    visited  — modules & fonts are just regular links
    page_pk is in system js */

function func_cloudComponentPages(){
  window.open("/cloud/svija/page/"+page_pk+"/change/", '_blank').focus()
}

/*———————————————————————————————————————— mobile/desktop link

    used to redirect to mobile or desktop on the opposite
    platform. cookieName is a supplied variable

    cloudForce is used by templates/svija/js/screens.js
    to NOT redirect if used */

function func_cloudComponentVersion(){
  alert('relocating')
  return true

  if (all_screens.length < 2)
    return true

  code = convertCode(code)
  localStorage.screen_code = code
  setCookie('screen_code', code, 7)

  window.location.replace(document.URL)
}


//:::::::::::::::::::::::::::::::::::::::: utility functions

/*———————————————————————————————————————— convertCode(code)

    currently only works if there are 1 or 2 screen codes
    requires mobile code to start with 'm'

    the module sends either mb or cp, and doesn't know
    if it's really mobile or ordinateur or 1200 etc.

    in system js:

    var all_screens = [[0, "1200"], [700, "300"]]; */

// need if it's cp I look for 0 else the other one

function convertCode(code){

  if (all_screens[0][0] == 0){
    var cpCode = all_screens[0][1]
    var mbCode = all_screens[1][1]
  }
  else{
    var cpCode = all_screens[1][1]
    var mbCode = all_screens[0][1]
  }

  code = Array.from(code)[0]

  if (code == 'm') return mbCode
  else return cpCode
  
}


//:::::::::::::::::::::::::::::::::::::::: fin


</script>
