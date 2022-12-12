/*———————————————————————————————————————— template: window_mgmt.js

/*———————————————————————————————————————— notes

    causes flash because we don't have correct zoomed width
    when executed in header

    included once in header to get rough overall size
    then once after initial scroll div to correct
    for scrollbars — window width changes with the
    addition of scrollbars, which are only added
    when the content is loaded

    we don't have to handle pinch because Safari handles
    it automatically when page is reloaded */

//———————————————————————————————————————— variables

// visible_width   // supplied by server
var globalMinZoom = 3;   // percent difference needed to count as a zoom

console.group('window mgmt');

//———————————————————————————————————————— running from <head>?

console.log('typeof inHead='+typeof inHead);

if (typeof inHead == 'undefined') var inHead = true;
                             else var inHead = false;

console.log('inHead='+inHead);

/*———————————————————————————————————————— get real screen width for FF zoom calc.

    This has the potential problem of firefox retaining the zoom level, then
    a visitor coming back and seeing an "initially zoomed" page that
    we can't detect. */

if (getCookie('screenWidth') != ''){
  var globalRealScreenWidth = getCookie('screenWidth');
}

else{
  var globalRealScreenWidth = globalThis.screen.availWidth;
  setCookie('screenWidth', globalRealScreenWidth, 7);
}

console.log('globalRealScreenWidth='+globalRealScreenWidth);

//———————————————————————————————————————— save state

if (inHead){
  var globalSavedWidth   = globalThis.innerWidth;    // used in setScale();
  var globalSavedZoom    = zoom();                   // used in body & setScale();

  console.log('gsw='+globalSavedWidth+', gsz='+globalSavedZoom);
}

//———————————————————————————————————————— set the rem unit

var aiPixel = globalThis.innerWidth / visible_width; // ⚠️  NEEDED IN OTHER SCRIPTS

document.documentElement.style.fontSize = aiPixel * globalSavedZoom + 'px';

console.log('aiPixel='+aiPixel); 

//———————————————————————————————————————— resize listener

if (inHead)
  var resizeListener = window.addEventListener('resize', setScale);

console.log('—————\n\n\n');
console.groupEnd();


//:::::::::::::::::::::::::::::::::::::::: methods

/*———————————————————————————————————————— function zoom(w)

    returns current zoom level
    requires globalRealScreenWidth, which is
    necessary for firefox

    close values mean scrollbars, so we return 1 */

function zoom(){

  var w = globalRealScreenWidth;

  if (w == globalThis.screen.availWidth)
    var r = globalThis.outerWidth/globalThis.innerWidth;

  // firefox
  else var r =  w/globalThis.screen.availWidth;

  return Math.round(r * 20) /20;
}

//———————————————————————————————————————— pctDifferent(a, b);

//    returns % difference between two numbers like 1.1, 1

function pctDifferent(a, b){
  return Math.round(Math.abs( a-b ) * 100);
}

/*———————————————————————————————————————— setScale()

    called when a resize event is triggered

    - if page is not fully loaded, return true
    - if page is made longer but not wider, return true
    - if page is zoomed more than 2%, return true

*/

function setScale(){

  if (!pageLoaded) return true;

  // page was just made longer
  var newWidth = globalThis.innerWidth;
  if (newWidth == globalSavedWidth) return true;
  
  // page was zoomed
  var d = pctDifferent(zoom(), globalSavedZoom);
  if (d > globalMinZoom) return true;

  // it's a resize event
  aiPixel = newWidth / visible_width + 'px';
  document.documentElement.style.fontSize = aiPixel;
  globalSavedWidth = globalThis.innerWidth;
  return true;

};


//———————————————————————————————————————— fin

// HORZ SCROLLBARS ON PC

// gsw is not going down from head to body
// ai pixel is not prcise enough: only 2 decimals
