/*———————————————————————————————————————— template: rem.js

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

//———————————————————————————————————————— get window width

if (typeof document.documentElement.clientWidth != 'undefined')
  var win_width = document.documentElement.clientWidth;
else
  var win_width = window.innerWidth;

//———————————————————————————————————————— set the rem unit

var illustrator_pixel = win_width / visible_width;
var zoom              = zoomPct(win_width);

document.documentElement.style.fontSize = illustrator_pixel*zoom + 'px';


//:::::::::::::::::::::::::::::::::::::::: functions

//———————————————————————————————————————— function zoomPct()

// ratio of content size to window size

function zoomPct(w){
  var r = realWidth();
  var z = zoomedWidth();

  return Math.round(r/z*100) / 100;
}


//:::::::::::::::::::::::::::::::::::::::: methods

//———————————————————————————————————————— fin

function realWidth(){ // doesn't work in FF
  return window.outerWidth;
}

function zoomedWidth(){
  return window.innerWidth;
}

//  alert(window.innerWidth +':'+ document.documentElement.clientWidth +':'+ document.body.clientWidth); // all wrong in FF







// 1771 is real size
a8 = document.documentElement.clientWidth;
a9 = window.innerWidth;
aa = window.outerWidth;
ab = screen.width;
//ac = document.body.scrollWidth;
ac = 'unsupported in head';
ad = window.screen.width;
ae = globalThis.screen.availWidth;
af = globalThis.outerWidth;
//ag = document.body.clientWidth;
ag = 'unsupported in head';
ah = screen.width;
ai = screen.availWidth;
aj = window.innerWidth;
ak = window.outerWidth;
al = screen.availWidth;
am = screen.width;
an = screen.top;
ao = screen.left;
ap = screen.availTop;

//alert(a8+':'+a9+':'+aa+':'+ab+':'+ac+':'+ad+':'+ae+':'+af+':'+ag+':'+ah+':'+ai+':'+aj+':'+ak+':'+al+':'+am+':'+an+':'+ao+':'+ap);

/* none of them work - firefox creates a zoom by changing all the variables to make the page think it's in a smaller space 

there is NO objective measure available

firefox:
1771:1771:1771:2560:unsupported in head:2560:2560:1771:unsupported in head:2560:2560:1771:1771:2560:2560:0:0:25
1476:1476:1476:2133:unsupported in head:2133:2133:1476:unsupported in head:2133:2133:1476:1476:2133:2133:0:0:21


safari:
1642:1642:1642:2560:unsupported in head:2560:2560:1642:unsupported in head:2560:2560:1642:1642:2560:2560:undefined:undefined:25
1314:1313:1642:2560:unsupported in head:2560:2560:1642:unsupported in head:2560:2560:1313:1642:2560:2560:undefined:undefined:25


I could keep the screen resolution in a cookie, then compare the fake resolution to the real one.
*/














/*
  // https://stackoverflow.com/questions/3437786/get-the-size-of-the-screen-current-web-page-and-browser-window
  const width  = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
  const height = window.innerHeight|| document.documentElement.clientHeight|| document.body.clientHeight;
  return width
}
*/
//———————————————————————————————————————— fin

/*
var firefox = (navigator.userAgent.indexOf('Firefox') > 0);
var zoom    = isZoomed(win_width);

alert(zoom);

// keyboard zoom levels, unlikely to be pinch levels. 300 is max pinch, so left out

var levels  = [.50, .67, .75, .80, .85, .90, 1.00, 1.10, 1.25, 1.50, 1.70, 2.00, 2.40, 4.00, 5.00];

var pinched = (firefox && typeof levels[zoom] != 'undefined');
*/










/*

document.documentElement.clientWidth;
window.innerWidth;
window.outerWidth;
screen.width
document.body.scrollWidth
window.screen.width

.contentWidth
globalThis.screen.availWidth // screen size
globalThis.outerWidth // window size
document.body.clientWidth
document.body.clientWidth   // Full width of the HTML page as coded, minus the vertical scroll bar
screen.width                // Device screen width (i.e. all physically visible stuff)
screen.availWidth           // Device screen width, minus the operating system taskbar (if present)
window.innerWidth           // The browser viewport width (including vertical scroll bar, includes padding but not border or margin)
window.outerWidth           // The outer window width (including vertical scroll bar,
                            // toolbars, etc., includes padding and border but not margin)

Screen {
    availWidth: 1920,
    availHeight: 1040,
    width: 1920,
    height: 1080,
    colorDepth: 24,
    pixelDepth: 24,
    top: 414,
    left: 1920,
    availTop: 414,
    availLeft: 1920
}

var width = window.innerWidth
|| document.documentElement.clientWidth
|| document.body.clientWidth;


alert(window.screen.availWidth);
alert(window.screen.availHeight);

*/

// this works: I get better values for width

//alert(window.innerWidth +'::'+window.outerWidth); // returns almost the same numbers — get smaller as window is zoomed
//alert(window.devicePixelRatio); returns 2, 1.75, 3 depending on platform
//alert(w + ' ! ' + window.outerWidth); //2304, 2307 in FF · 2226, 2560 in Safari (1.15*) FF should be 2534

