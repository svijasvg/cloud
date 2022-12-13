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

// visible_width         // supplied by server
var envMinDiff = 5;   // percent difference needed to count as a zoom

//———————————————————————————————————————— running from <head>?

if (typeof envInHead == 'undefined') var envInHead = true;
                             else var envInHead = false;

/*———————————————————————————————————————— get real screen width for FF zoom calc.

    This has the potential problem of firefox retaining the zoom level, then
    a visitor coming back and seeing an "initially zoomed" page that
    we can't detect. */

if (envInHead){

  if (getCookie('screenWidth') == ''){
    var envRealScreenWidth = globalThis.screen.availWidth;
    setCookie('screenWidth', envRealScreenWidth, 7);
  }
  else
    var envRealScreenWidth = getCookie('screenWidth');
  
}

//———————————————————————————————————————— set the rem unit

var envPrevWidth    = currentWidth();                 // used in resize();
var aiPixel         = currentWidth() / visible_width; // ⚠️  NEEDED IN OTHER SCRIPTS
var envCurrentZoom  = zoom();                         // used in body & resize();
var envLoadedZoomed = false;

if (areDifferent(envCurrentZoom, 1)) envLoadedZoomed = true;

aiPixel = aiPixel*envCurrentZoom;

document.documentElement.style.fontSize = aiPixel + 'px';

//———————————————————————————————————————— log initial values

console.group('window mgmt on load');
console.log('envRealScreenWidth='+envRealScreenWidth);
console.log('page zoom on load: '+envCurrentZoom);
console.log('envPrevWidth='+envPrevWidth);
console.log('aiPixel='+aiPixel); 
console.log('envCurrentZoom='+envCurrentZoom);
console.groupEnd();

//———————————————————————————————————————— resize listener

if (envInHead)
  var resizeListener = window.addEventListener('resize', resize);

//———————————————————————————————————————— set scroll position

// makes centered over-width pages appear centered on load instead of centering late
// page_offsets set in admin // aiPixel set in rem.js

var left_margin_px = page_offsetx * aiPixel;
var top_margin_px  = page_offsety * aiPixel;

var xInit = Math.round(left_margin_px);
var yInit = Math.round(top_margin_px);

setScroll(); setTimeout(setScroll, 1);


//:::::::::::::::::::::::::::::::::::::::: methods

/*———————————————————————————————————————— zoom(w)

    returns current zoom level
    requires envRealScreenWidth, which is
    necessary for firefox

    close values mean scrollbars, so we return 1 */

function zoom(){

  var w = envRealScreenWidth;
  if (w == globalThis.screen.availWidth){
    var z = globalThis.outerWidth/currentWidth();
  }

  // firefox
  else var z = w/globalThis.screen.availWidth;
  
  if (z>0.91 && z<1.09) z = 1;

//console.log('zoom(): z='+z+', globalThis.outerWidth='+globalThis.outerWidth+', currentWidth()='+currentWidth());
  return z;
}

//———————————————————————————————————————— currentWidth()

function currentWidth(){
  if (envInHead) return globalThis.innerWidth;
  return document.documentElement.clientWidth;
}

//———————————————————————————————————————— setScroll()

function setScroll(){
  if (envLoadedZoomed) return true;

  console.log('scrolling to '+xInit+', '+yInit);
  window.scrollTo(xInit, yInit);
}

//———————————————————————————————————————— areDifferent(a, b);

//    returns % difference between two numbers like 1.1, 1
/*  used to compensate for minor differences in zoom() caused by the presence of scrollbars in PC browsers */

function areDifferent(a, b){
  var d = Math.round(Math.abs( a-b ) * 100);
  if (d > envMinDiff) return  true;
                 else return false;
}

/*———————————————————————————————————————— resize()

    called when a resize event is triggered

    - if page is not fully loaded, return true
    - if page is made longer but not wider, return true
    - if page is zoomed more than 2%, return true

*/

function resize(){

  if (!pageLoaded) {console.log('page not loaded'); return true;}

  // page was just made longer
  if (currentWidth() == envPrevWidth) {console.log('page made longer'); return true;}
  
  // page was zoomed
  if (areDifferent(zoom(), envCurrentZoom)) {
    console.log('page zoomed: '+zoom()+', envCurrentZoom='+envCurrentZoom);
    envCurrentZoom = zoom();
  }

  // it's a resize event
  aiPixel = currentWidth() / visible_width * zoom() + 'px';
  document.documentElement.style.fontSize = aiPixel;
  envPrevWidth = currentWidth();

  console.log('page resized');
  return true;

};


//———————————————————————————————————————— fin
