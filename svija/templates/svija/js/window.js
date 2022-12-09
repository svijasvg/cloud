/*———————————————————————————————————————— template: rem.js

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

//———————————————————————————————————————— save screen width

var firefoxScreen = getCookie('firefoxScreen');

if (firefoxScreen == ''){
  firefoxScreen = globalThis.screen.availWidth;
  setCookie('firefoxScreen', firefoxScreen, 7);
}

//———————————————————————————————————————— get window width

if (typeof document.documentElement.clientWidth != 'undefined')
  var win_width = document.documentElement.clientWidth;
else
  var win_width = window.innerWidth;

//———————————————————————————————————————— set the rem unit

var illustrator_pixel = win_width / visible_width;
var zoomAtLoad              = zoomPct(win_width);

document.documentElement.style.fontSize = illustrator_pixel*zoomAtLoad + 'px';


//:::::::::::::::::::::::::::::::::::::::: methods

/*———————————————————————————————————————— function zoomPct()

    ratio of content size to window size
    on zoom, firefox lies about screen size
    so we compare to stored value */

function zoomPct(w){

  if (firefoxScreen != globalThis.screen.availWidth){
    var r = firefoxScreen;
    var z = globalThis.screen.availWidth;
  }
  else{
    var r = realWidth();
    var z = zoomedWidth();
  }

  pct = Math.round(r/z*100) / 100;

  if (pct > 0.95 && pct < 1.09) return 1; // necessary because scrollbars
  else return pct;                        // look like zooming
}

//———————————————————————————————————————— realWidth()

function realWidth(){ // doesn't work in FF
  return window.outerWidth;
}

//———————————————————————————————————————— zoomedWidth()

function zoomedWidth(){
  return window.innerWidth;
}


//———————————————————————————————————————— fin
/*———————————————————————————————————————— on_resize.js

   templates/svija/javascript/on_resize.js

   adapts content to window on resize but not zoom */

//———————————————————————————————————————— predefined values

// var illustrator_pixel set in rem.js

//———————————————————————————————————————— variables

var sensitivity = 10;                    // higher is more sensitive to resizing
var prevRatio   = get_ratio(sensitivity); // width/height
var prevWidth   = window.visualViewport.width;

//———————————————————————————————————————— listener function

window.addEventListener("resize", resizeWindow);

function resizeWindow(){

  if (!page_loaded) return false;
  if (isZoomed())   return false;

  var newWidth = window.visualViewport.width;
  if (newWidth == prevWidth) return false;
  
  // resize to fit

  var illustrator_pixel = window.visualViewport.width / visible_width;
  document.documentElement.style.fontSize = illustrator_pixel + 'px';
  prevRatio = get_ratio(sensitivity); // width/height
  var prevWidth = window.visualViewport.width;
};


//:::::::::::::::::::::::::::::::::::::::: functions

//———————————————————————————————————————— isZoomed()

function isZoomed(){

  var r = get_ratio(sensitivity);
  if (r != prevRatio) return false;

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
