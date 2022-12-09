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
var zoom              = zoomPct(win_width);

document.documentElement.style.fontSize = illustrator_pixel*zoom + 'px';


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
