
//:::::::::::::::::::::::::::::::::::::::: template: window_mgmt.js
/*
https://www.toptal.com/developers/javascript-minifier
*/

//alert('window_mgmt.js\n'+screen_code)

/*———————————————————————————————————————— notes

    This script sets the window size and defines the REM unit.

    It's complex, because there are some circumstances where it's
    necessary to rezise (the window changed), but others where it's
    counterproductive (the user zoomed).

    The page should stay scrolled to the same point during resizing.

    There is a known issue where side columns are not taken into effect,
    for example the reading list in Safari.

    On initial load this script does little:

    1. calculates the REM size
    2. sets the scroll position if there's an offset in Svija Cloud
    3. adds a listener to redo the rem size if something changes */

//———————————————————————————————————————— variables

// var visible_width = 1200;   // supplied by system JS

var MIN_DIFF = 5;            // percent difference needed to count as a zoom

//———————————————————————————————————————— is it Firefox?

var IS_FIREFOX = navigator.userAgent.indexOf('Firefox')>0;

/*———————————————————————————————————————— get real screen size for FF & iPhone

    This has the potential problem of firefox retaining the zoom level, then
    a visitor coming back and seeing an "initially zoomed" page that
    we can't detect. */

// real screen width, for firefox
if (IS_FIREFOX && getCookie('screenWidth') != '')
  var REAL_SCREEN_WIDTH = getCookie('screenWidth');
else{
  var REAL_SCREEN_WIDTH = globalThis.screen.availWidth;
  setCookie('screenWidth', REAL_SCREEN_WIDTH, 7);
}

// real screen height, for iPhone
if (getCookie('screenHeight') == ''){
  var REAL_SCREEN_HEIGH = globalThis.screen.availHeight;
  setCookie('screenHeight', REAL_SCREEN_HEIGH, 7);
}
else
  var REAL_SCREEN_HEIGH = getCookie('screenHeight');

//———————————————————————————————————————— environmental variables

var PREVIOUS_WIDTH = zoomedWidth();   // used in resize();
var PREVIOUS_ZOOM  = zoom();          // used in resize();

if (areDifferent(zoom(), 1)) var LOADED_ZOOMED = true;
                        else var LOADED_ZOOMED = false;

//———————————————————————————————————————— set the rem unit

var rawPixel = zoomedWidth() / visible_width; // ⚠️  USED BY OTHER SCRIPTS
var  aiPixel = rawPixel * zoom();

document.documentElement.style.fontSize = aiPixel + 'px';

//———————————————————————————————————————— resize listener

  var resizeListener = window.addEventListener('resize', resize);

//———————————————————————————————————————— set scroll position per Cloud params

var left_margin_px = page_offsetx * aiPixel;
var top_margin_px  = page_offsety * aiPixel;

var X_INIT = Math.round(left_margin_px);
var Y_INIT = Math.round(top_margin_px);

// this can't work because this script is in head
//setScroll(); setTimeout(setScroll, 1);


//:::::::::::::::::::::::::::::::::::::::: methods

//———————————————————————————————————————— zoomedWidth()

function zoomedWidth(){
  var r = globalThis.innerWidth;
  return r;
}

//———————————————————————————————————————— setScroll()

function setScroll(){
  if (LOADED_ZOOMED) return true;
  window.scrollTo(X_INIT, Y_INIT);
  console.log('init values: '+X_INIT+':'+ Y_INIT);
}

//———————————————————————————————————————— areDifferent(a, b);

//    returns % difference between two numbers like 1.1, 1
/*  used to compensate for minor differences in zoom() caused by the presence of scrollbars in PC browsers */

function areDifferent(a, b){
  var d = Math.round(Math.abs( a-b ) * 100);
  if (d > MIN_DIFF) return  true;
                 else return false;
}

/*———————————————————————————————————————— zoom(w)

    close values mean scrollbars, so we return 1 */

function zoom(){

  // android screen was rotated
  if (globalThis.screen.availWidth == REAL_SCREEN_HEIGH){
    REAL_SCREEN_HEIGH = globalThis.screen.availHeight;
    REAL_SCREEN_WIDTH  = globalThis.screen.availWidth;
  }

  var w = REAL_SCREEN_WIDTH;               // this is just to make
  if (w == globalThis.screen.availWidth){   // sure it's not firefox
    var z = globalThisOuterWidth()/zoomedWidth();
  }

  // firefox
  else{
    var z = w/globalThis.screen.availWidth; 
  }

  if (!areDifferent(z, 1)) z = 1;

  return z;
}

/*———————————————————————————————————————— resize()

    called when a resize event is triggered */

function resize(){
  if (!pageLoaded) {return true;}

 var zoomFactor = 1;

  // page was just made longer
  if (zoomedWidth() == PREVIOUS_WIDTH) {return true;}
  
  if (globalThis.innerWidth != REAL_SCREEN_HEIGH)
    zoomFactor = zoom();

  else
    // iPhone rotated to landscape
    console.log('iPhone rotated to landscape');

  aiPixel = zoomedWidth() / visible_width * zoomFactor;

  document.documentElement.style.fontSize = aiPixel + 'px';

  PREVIOUS_WIDTH = zoomedWidth();

  return true;
};

/*———————————————————————————————————————— globalThisOuterWidth()

    called by zoom()

    because iPhone returns wrong value in landscape mode */

function globalThisOuterWidth(){
  var r;

  // iPhone rotated to landscape
  if (window.innerWidth == REAL_SCREEN_HEIGH){
    r = window.innerWidth;
  }

  // iPhone rotated to portrait
  else if (globalThis.outerWidth == REAL_SCREEN_HEIGH){
    r = window.innerWidth;
  }

  else r= globalThis.outerWidth;

  return r;
}


//:::::::::::::::::::::::::::::::::::::::: fin
