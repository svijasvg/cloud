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


//:::::::::::::::::::::::::::::::::::::::: CSS styles

/*———————————————————————————————————————— system JS

var svija_version='2.3.3'
var section_code = "en"
var screen_code = "cp"
var page_pk = 94
var milliseconds = "1746793412577319970"
var all_screens = [[0, "cp"], [500, "mb"]] // WHAT IS THIS CALLED?
var tracking_on = false
var page_url = 'https://dev.svija.love/en/home'
var admin=true
var page_width = 1680
var visible_width = 1200
var page_offsetx = 240
var page_offsety = 0 */


//:::::::::::::::::::::::::::::::::::::::: link functions

/*———————————————————————————————————————— page link

    only used for pages, to go directly to the page being
    visited  — modules & fonts are just regular links
    page_pk is in system js */

function cloudComponentPages(){
  window.open("/cloud/svija/page/"+page_pk+"/change/", '_blank').focus()
}

/*———————————————————————————————————————— mobile/desktop link

    used to redirect to mobile or desktop on the opposite
    platform. cookieName is a supplied variable

    cloudForce is used by templates/svija/js/screens.js
    to NOT redirect if used */

function cloudComponentVersion(){
  if (all_screens.length < 2)
    return true

  var this_screen = 0

  for(let [key, value] of Object.entries(all_screens)) {
    alert(key+'::'+value)
  }

//for (var x=0; x<all_screens.length; x++){
//  if (all_screens[x].value == code)
//    this_screen = x
//}

  // switch between biggest & smallest
  // https://stackoverflow.com/questions/7196212/how-to-create-a-dictionary-and-add-key-value-pairs-dynamically-in-javascript
  // https://stackoverflow.com/questions/684672/how-do-i-loop-through-or-enumerate-a-javascript-object










// we don't have code — it was sent by the module svg. Now we need to deduce it.

  return true

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
