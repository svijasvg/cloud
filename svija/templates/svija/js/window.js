/*———————————————————————————————————————— template: window.js

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

//———————————————————————————————————————— predefined variables

// visible_width is supplied by server

//———————————————————————————————————————— variables

var sensitivity  = 10;                     // higher is more sensitive to resizing
var savedRatio   = get_ratio(sensitivity); // width/height
var savedWidth   = window.visualViewport.width;

//———————————————————————————————————————— save screen width for firefox

var savedScreen = getCookie('savedScreen');

if (savedScreen == ''){
  savedScreen = globalThis.screen.availWidth;
  setCookie('savedScreen', savedScreen, 7);
}

//———————————————————————————————————————— set the rem unit

var insideWidth = document.documentElement.clientWidth;
var aiPixel     = insideWidth / visible_width;
var zoomAtLoad  = zoomPct();

document.documentElement.style.fontSize = aiPixel*zoomAtLoad + 'px';

//———————————————————————————————————————— resize listener function

if (typeof resizeListener == 'undefined')
  var resizeListener = window.addEventListener('resize', redraw);

function redraw(){

  if (!page_loaded) return false;
  if (isZoomed())   return false;

  var newWidth = window.visualViewport.width;
  if (newWidth == savedWidth) return false;
  
  // resize to fit

  var aiPixel = window.visualViewport.width / visible_width + 'px';
  document.documentElement.style.fontSize = aiPixel;

  savedRatio = get_ratio(sensitivity); // width/height
  savedWidth = window.visualViewport.width;
};


//:::::::::::::::::::::::::::::::::::::::: methods

/*———————————————————————————————————————— function zoomPct()

    accepts w=inside width of current window

    ratio of content size to window size
    on zoom, firefox lies about screen size
    so we compare to stored value */

function zoomPct(){

  if (savedScreen != globalThis.screen.availWidth){
    var r = savedScreen;
    var z = globalThis.screen.availWidth;
  }

  else{
    var r = window.outerWidth;
    var z = document.documentElement.clientWidth;
  }

  pct = Math.round(r/z*100) / 100;

  if (pct > 0.95 && pct < 1.09) return 1; // necessary because scrollbars
  else return pct;                        // look like zooming
}

//———————————————————————————————————————— isZoomed()

function isZoomed(){

  var r = get_ratio(sensitivity);
  if (r != savedRatio) return false;

  return true;
}

/*———————————————————————————————————————— get_ratio(precision)

    when a window is resized on windows, the ratio changes because
    the scrollbars don't zoom with the page */

function get_ratio(precision){
  var w = window.visualViewport.width;
  var h = window.visualViewport.height;
  var r = Math.round(w/h * precision)/precision;

  return r;
}


//———————————————————————————————————————— fin
