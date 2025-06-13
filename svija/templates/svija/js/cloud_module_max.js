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
var all_screens = [[0, "cp"], [500, "mb"]]
var tracking_on = false
var page_url = 'https://dev.svija.love/en/home'
var admin=true
var page_width = 1680
var visible_width = 1200
var page_offsetx = 240
var page_offsety = 0 */


//:::::::::::::::::::::::::::::::::::::::: link functions

/*———————————————————————————————————————— update link name to mobile/desktop
    */

cloudModuleScreenName.innerHTML = getCurrentScreenCodeName()

/*———————————————————————————————————————— page link

    only used for pages, to go directly to the page being
    visited  — modules & fonts are just regular links
    page_pk is in system js */

function cloudComponentPages(){
  window.open("/cloud/svija/page/"+page_pk+"/change/", '_blank').focus()
}

/*———————————————————————————————————————— changeScreenCode()

    used to redirect to mobile or desktop on the opposite
    platform. cookieName is a supplied variable

    cloudForce is used by templates/svija/js/screens.js
    to NOT redirect if used */

// get screen code which does not equal current screen code and THAT'S IT

function changeScreenCode(){
  if (all_screens.length < 2)
    return true

  var new_code = screen_code

  for (var x=0; x<all_screens.length; x++) {
    var code = all_screens[x][1]
    if (code != screen_code)
      new_code = code
  }

//alert(`screen code: ${screen_code}\nnew_code: ${new_code}`)

  localStorage.screen_code = new_code
  setCookie('screen_code', new_code, 7)

  window.location.replace(document.URL)
}


//:::::::::::::::::::::::::::::::::::::::: utility functions

/*———————————————————————————————————————— getScreenCodeName()
    */

function getCurrentScreenCodeName(){
  var otherScreenCodeName = 'screen'

  for (var x=0; x<all_screens.length; x++) {
    var code = all_screens[x][1]
    if (code != screen_code)
      otherScreenCodeName = all_screens[x][2]
  }
  return otherScreenCodeName
}

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
