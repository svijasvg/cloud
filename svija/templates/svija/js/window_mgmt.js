//———————————————————————————————————————— template: window_mgmt.js

//———————————————————————————————————————— variables

// visible_width      // supplied by server
var envMinDiff = 5;   // percent difference needed to count as a zoom

//———————————————————————————————————————— running from <head>?

if (typeof envInHead == 'undefined') var envInHead = true;
                                else var envInHead = false;

/*———————————————————————————————————————— get real screen size for FF & iPhone

    This has the potential problem of firefox retaining the zoom level, then
    a visitor coming back and seeing an "initially zoomed" page that
    we can't detect. */

// real screen width, for firefox
if (envInHead){
  if (getCookie('screenWidth') == ''){
    var envRealScreenWidth = globalThis.screen.availWidth;
    setCookie('screenWidth', envRealScreenWidth, 7);
  }
  else
    var envRealScreenWidth = getCookie('screenWidth');
}

// real screen height, for iPhone
if (envInHead){
  if (getCookie('screenHeight') == ''){
    var envRealScreenHeight = globalThis.screen.availHeight;
    setCookie('screenHeight', envRealScreenHeight, 7);
  }
  else
    var envRealScreenHeight = getCookie('screenHeight');
}


//———————————————————————————————————————— environmental variables

var envPrevWidth    = zoomedWidth();                 // used in resize();
var envPrevZoom     = zoom();                         // used in resize();
var envLoadedZoomed = false;

if (areDifferent(zoom(), 1)) envLoadedZoomed = true;

//———————————————————————————————————————— set the rem unit

var aiPixel = zoomedWidth() / visible_width; // ⚠️  NEEDED IN OTHER SCRIPTS
    aiPixel = aiPixel * zoom();

document.documentElement.style.fontSize = aiPixel + 'px';

//———————————————————————————————————————— log initial values

if (!envInHead){
  console.group('window mgmt on load');
  console.log('envRealScreenWidth='+envRealScreenWidth);
  console.log('page zoom on load: '+zoom());
  console.log('envPrevWidth='+envPrevWidth);
  console.log('aiPixel='+aiPixel); 
  console.groupEnd();
}

//———————————————————————————————————————— resize listener

if (envInHead)
  var resizeListener = window.addEventListener('resize', resize);

//———————————————————————————————————————— set scroll position

if(!envInHead){
  var left_margin_px = page_offsetx * aiPixel;
  var top_margin_px  = page_offsety * aiPixel;
  
  var xInit = Math.round(left_margin_px);
  var yInit = Math.round(top_margin_px);
  
  setScroll(); setTimeout(setScroll, 1);
}


//:::::::::::::::::::::::::::::::::::::::: methods

//———————————————————————————————————————— zoomedWidth()

function zoomedWidth(){

//if (window.navigator.userAgent.indexOf('Android')>0) alert(x);
  var r;

  if (envInHead) r = globalThis.innerWidth;
  else r = document.documentElement.clientWidth;

//  if (window.navigator.userAgent.indexOf('Android')>0) alert(r); // correct on android

  console.log('zoomedWidth() returns '+r);
  return r;
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

/*———————————————————————————————————————— zoom(w)

    close values mean scrollbars, so we return 1 */

function zoom(){

  // android screen was rotated
  if (globalThis.screen.availWidth == envRealScreenHeight){
    envRealScreenHeight = globalThis.screen.availHeight;
    envRealScreenWidth  = globalThis.screen.availWidth;
  }

  var w = envRealScreenWidth;               // this is just to make
  if (w == globalThis.screen.availWidth){   // sure it's not firefox
    console.log('zoom not firefox');
    var z = globalThisOuterWidth()/zoomedWidth();
  }

  // firefox
  else{
    console.log('zoom firefox');
    var z = w/globalThis.screen.availWidth; 
  }

  if (!areDifferent(z, 1)) z = 1;

  console.log('zoom() returning '+z);
  return z;
}

//———————————————————————————————————————— pctDifferent(a, b);

//    returns % difference between two numbers like 1.1, 1

function pctDifferent(a, b){
  return Math.round(Math.abs( a-b ) * 100);
}

/*———————————————————————————————————————— resize()

    called when a resize event is triggered */

function resize(){
  if (!pageLoaded) {console.log('page not loaded'); return true;}

 var zoomFactor = 1;

  // page was just made longer
  if (zoomedWidth() == envPrevWidth) {console.log('page made longer'); return true;}
  
  if (globalThis.innerWidth != envRealScreenHeight)
    zoomFactor = zoom();

  else
    // iPhone rotated to landscape
    console.log('iPhone rotated to landscape');

  aiPixel = zoomedWidth() / visible_width * zoomFactor;

  document.documentElement.style.fontSize = aiPixel + 'px';

  envPrevWidth = zoomedWidth();
  console.log('page resized: width='+zoomedWidth()+', zoom='+zoom());

  return true;
};

/*———————————————————————————————————————— globalThisOuterWidth()

    called by zoom()

    because iPhone returns wrong value in landscape mode */

function globalThisOuterWidth(){
  var r;

  // iPhone rotated to landscape
  if (window.innerWidth == envRealScreenHeight){
    console.log('iPhone turned to landscape');
    r = window.innerWidth;
  }

  // iPhone rotated to portrait
  else if (globalThis.outerWidth == envRealScreenHeight){
    console.log('iPhone turned to portrait');
    r = window.innerWidth;
  }

  else r= globalThis.outerWidth;

  console.log('globalThisOuterWidth() returns '+r);
  return r;
}


//———————————————————————————————————————— fin
