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

//———————————————————————————————————————— predefined variable

// visible_width is supplied by server

//———————————————————————————————————————— variables

var minZoom = 5;   // percent difference needed to count as a zoom

//———————————————————————————————————————— save state

var savedScreen = getCookie('savedScreen');

if (savedScreen == ''){
  savedScreen = globalThis.screen.availWidth;
  setCookie('savedScreen', savedScreen, 7);
}

var savedWidth   = document.documentElement.clientWidth;

console.log('36 calling zoomPct');
var savedZoom    = zoomPct();

console.log('39 savedScreen='+savedScreen+', savedWidth='+savedWidth+', savedZoom='+savedZoom);
// alert(zoomPct()); wrong on load

//———————————————————————————————————————— set the rem unit

var insideWidth       = document.documentElement.clientWidth;
var illustrator_pixel = insideWidth / visible_width;

console.log('47 calling zoomPct');
var zoomAtLoad        = zoomPct();
console.log('49 insideWidth='+insideWidth+', illustrator_pixel='+illustrator_pixel+', zoomAtLoad='+zoomAtLoad);

document.documentElement.style.fontSize = illustrator_pixel*zoomAtLoad + 'px';

//———————————————————————————————————————— resize listener function

if (typeof resizeListener == 'undefined')
  var resizeListener = window.addEventListener('resize', redraw);

function redraw(){

  if (!page_loaded) return false;

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

  var illustrator_pixel = window.visualViewport.width / visible_width + 'px';
  document.documentElement.style.fontSize = illustrator_pixel;

  savedWidth = window.visualViewport.width;
};


//:::::::::::::::::::::::::::::::::::::::: methods

/*———————————————————————————————————————— function zoomPct()

    accepts w=inside width of current window

    ratio of content size to window size
    on zoom, firefox lies about screen size
    so we compare to stored value */

function zoomPct(){
  console.group('zoomPct()');

  if (savedScreen != globalThis.screen.availWidth){
    var real   = savedScreen;
    var zoomed = globalThis.screen.availWidth;
    console.log('99 —› real='+real+', zoomed='+zoomed);
  }

  else{
    if (document.documentElement.clientWidth != 'undefined'){
      var real   = document.documentElement.scrollWidth; // THIS DOES NOT WORK IT CHANGES WITH THE ZOOM, IS SUPPOSED TO NEVER CHANGE
      var zoomed = document.documentElement.clientWidth;
      console.log('106 —› real='+real+', zoomed='+zoomed);
    }
    else{
      var real   = globalThis.screen.availWidth;
      var zoomed = globalThis.screen.availWidth;
      console.log('111 —› real='+real+', zoomed='+zoomed);
    }
  }

  pct = real/zoomed;
  console.log('116 —› pct='+pct);
  console.groupEnd();

  return pct;
}

//———————————————————————————————————————— zoomDiff(newZoom, savedZoom);

function zoomDiff(newZoom, savedZoom){
  var cgmt = newZoom - savedZoom;
  if (cgmt < 0) cgmt = 0 - cgmt;
  cgmt = cgmt * 100;

  return cgmt;
}


//———————————————————————————————————————— fin
