//:::::::::::::::::::::::::::::::::::::::: template: sections.js
/*
https://www.toptal.com/developers/javascript-minifier
*/

/*———————————————————————————————————————— notes

    Meant to redirect for languages — if someone already chose French
    they should be sent to the French version if they arrive again
    meaning in the absence of other information

    redirect if 4 conditions are met:

    1. user is coming from elsewhere
    2. the user is at home page (3 slashes = https://svija.love)
    3. there's a cookie code and it is NOT the same as the current section
       so user is in wrong section

    cookie would contain fr for example
    used by menus when one clicks on flag

    ——————————————————————————————————————

    This script also contains a function:

    chooseSection(code)

    which can be called by other scripts to set the section_code
    cookie and redirect to the appropriate section */


//:::::::::::::::::::::::::::::::::::::::: program

//———————————————————————————————————————— redirect if 4 conditions are met

var x = 'h'+document.referrer
var referring_host = x.split('/')[2]
var current_host = page_url.split('/')[2]

var path_parts = location.href.split('/')

// condition: visitor already chose section
var cookie_code = getCookie('section_code')

//———————————————————————————————————————— four conditions

var fromElsewhere     =    referring_host != current_host
var homePage          = path_parts.length == 4
var choseOtherSection =       cookie_code != '' && cookie_code != section_code

//———————————————————————————————————————— redirect if appropriate

if (fromElsewhere && homePage && choseOtherSection)
  location.href = '/' + cookie_code


//:::::::::::::::::::::::::::::::::::::::: methods

//———————————————————————————————————————— function

function chooseSection(code){
  setCookie('section_code', code, 7);
  location.href = '/' + code;
}


//:::::::::::::::::::::::::::::::::::::::: fin

