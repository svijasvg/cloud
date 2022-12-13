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
var envMinZoom = 5;   // percent difference needed to count as a zoom

console.group('window mgmt');

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
  
  console.log('envRealScreenWidth='+envRealScreenWidth);
}

//———————————————————————————————————————— set the rem unit

var envPrevWidth    = currentWidth();                 // used in resize();
var aiPixel         = currentWidth() / visible_width; // ⚠️  NEEDED IN OTHER SCRIPTS
var envCurrentZoom  = zoom();                         // used in body & resize();
var envLoadedZoomed = false;

if (pctDifferent(envCurrentZoom, 1) > envMinZoom){
  envLoadedZoomed = true;
  console.log('page zoomed on load: '+envCurrentZoom);
}

aiPixel = aiPixel*envCurrentZoom;
document.documentElement.style.fontSize = aiPixel + 'px';

console.log('envPrevWidth='+envPrevWidth);
console.log('aiPixel='+aiPixel); 
console.log('envCurrentZoom='+envCurrentZoom);

//———————————————————————————————————————— resize listener

if (envInHead)
  var resizeListener = window.addEventListener('resize', resize);

console.log('—————\n\n\n');
console.groupEnd();

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
    console.log('zoom()='+z+', globalThis.outerWidth='+globalThis.outerWidth+', currentWidth()='+currentWidth());
  }

  // firefox
  else var z = w/globalThis.screen.availWidth;
  
  return z;
}

//———————————————————————————————————————— pctDifferent(a, b);

//    returns % difference between two numbers like 1.1, 1

function pctDifferent(a, b){
  console.log('pctDifferent(): '+a+', '+b);
  return Math.round(Math.abs( a-b ) * 100);
}

//———————————————————————————————————————— currentWidth()

function currentWidth(){
  if (envInHead) return globalThis.innerWidth;
  return document.documentElement.clientWidth;
}

/*———————————————————————————————————————— resize()

    called when a resize event is triggered

    - if page is not fully loaded, return true
    - if page is made longer but not wider, return true
    - if page is zoomed more than 2%, return true

*/

function resize(){
  console.group('resize()');

  if (!pageLoaded) {console.log('page not loaded'); return true;}

  // page was just made longer
  if (currentWidth() == envPrevWidth) {console.log('page made longer'); return true;}
  
  // page was zoomed
  var d = pctDifferent(zoom(), envCurrentZoom);
  console.log('d='+d+', zoom()='+zoom()+', envCurrentZoom='+envCurrentZoom);
  if (d > envMinZoom) {
    envCurrentZoom = zoom();
    console.log('page zoomed');
    console.groupEnd();
    return true;
  }

  // it's a resize event
  aiPixel = currentWidth() / visible_width * zoom() + 'px';
  document.documentElement.style.fontSize = aiPixel;
  envPrevWidth = currentWidth();

  console.log('page resized');
  console.groupEnd();
  return true;

};

//———————————————————————————————————————— setScroll()

function setScroll(){
  if (envLoadedZoomed) return true;

  console.log('scrolling to '+xInit+', '+yInit);
  window.scrollTo(xInit, yInit);
}


//———————————————————————————————————————— fin
