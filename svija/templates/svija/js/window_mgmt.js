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
var minZoom = 5;   // percent difference needed to count as a zoom

//———————————————————————————————————————— running from <head>?

if (typeof inHead == 'undefined') inHead = true;
                             else inHead = false;

/*———————————————————————————————————————— get real screen width for FF zoom calc.

    This has the potential problem of firefox retaining the zoom level, then
    a visitor coming back and seeing an "initially zoomed" page that
    we can't detect. */

  var realScreenWidth = getCookie('screenWidth');

  if (realScreenWidth == ''){
    realScreenWidth = globalThis.screen.availWidth;
    setCookie('screenWidth', realScreenWidth, 7);
  }

//———————————————————————————————————————— save state

if (inHead){
  var savedWidth   = globalThis.outerWidth;
  var savedZoom    = zoomPct(realScreenWidth);
}

//———————————————————————————————————————— set the rem unit

var aiPixel = globalThis.innerWidth / visible_width; // ⚠️  NEEDED IN OTHER SCRIPTS

document.documentElement.style.fontSize = aiPixel * savedZoom + 'px';

//———————————————————————————————————————— resize listener function MOVE TO FIRSTLOAD

if (inHead)
  var resizeListener = window.addEventListener('resize', setScale);


//:::::::::::::::::::::::::::::::::::::::: methods

//———————————————————————————————————————— function zoomPct()

function zoomPct(rsw){

  if (rsw == globalThis.screen.availWidth)
    return globalThis.outerWidth/globalThis.innerWidth;

  // firefox
  else return rsw/globalThis.screen.availWidth;

//  NEED TO RETURN 1 IF IT'S LESS THAN 1.01 OR MORE THAN .99
}

//———————————————————————————————————————— zoomDiff(newZoom, savedZoom);

function zoomDiff(newZoom, savedZoom){
  var cgmt = newZoom - savedZoom;
  if (cgmt < 0) cgmt = 0 - cgmt;
  cgmt = cgmt * 100;

  return cgmt;
}

/*———————————————————————————————————————— setScale()

    called when a resize event is triggered

    - if page is not loaded, return true
    - if page is made longer but not wider, return true
    - if page is zoomed more than 2%, return true





*/

function setScale(){

  if (!pageLoaded) return false;


  var newWidth = document.documentElement.clientWidth;
  if (newWidth == savedWidth) return false;
  
  console.log('65 calling zoomPct');
  var newZoom = zoomPct();
  var thisDiff = zoomDiff(newZoom, savedZoom);

  if (thisDiff > minZoom){
    // it's a zoom event
    return true;
  }

  // it's a resize event

  var aiPixel = window.visualViewport.width / visible_width + 'px';
  document.documentElement.style.fontSize = aiPixel;

  savedWidth = window.visualViewport.width;
};


//———————————————————————————————————————— fin
