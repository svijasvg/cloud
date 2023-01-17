//———————————————————————————————————————— template: window_mgmt.js

//———————————————————————————————————————— start logging

console.group('window mgmt on load');

//———————————————————————————————————————— variables

// var visible_width = 1200;   // supplied by server
var envMinDiff = 5;            // percent difference needed to count as a zoom

/*———————————————————————————————————————— get real screen size for FF & iPhone

    This has the potential problem of firefox retaining the zoom level, then
    a visitor coming back and seeing an "initially zoomed" page that
    we can't detect. */

console.log('cookie screenWidth='+getCookie('screenWidth'));
console.log('cookie screenHeight='+getCookie('screenHeight'));

// real screen width, for firefox
if (getCookie('screenWidth') == ''){
  var envRealScreenWidth = globalThis.screen.availWidth;
  setCookie('screenWidth', envRealScreenWidth, 7);
}
else
  var envRealScreenWidth = getCookie('screenWidth');

// real screen height, for iPhone
if (getCookie('screenHeight') == ''){
  var envRealScreenHeight = globalThis.screen.availHeight;
  setCookie('screenHeight', envRealScreenHeight, 7);
}
else
  var envRealScreenHeight = getCookie('screenHeight');

console.log('envRealScreenWidth='+envRealScreenWidth);
console.log('envRealScreenHeight='+envRealScreenHeight);

//———————————————————————————————————————— environmental variables

var envPrevWidth    = zoomedWidth();   // used in resize();
var envPrevZoom     = zoom();          // used in resize();

if (areDifferent(zoom(), 1)) var envLoadedZoomed = true;
                        else var envLoadedZoomed = false;

console.log('envPrevWidth='   +envPrevWidth   );
console.log('envPrevZoom='    +envPrevZoom    );
console.log('zoom(): '        +zoom());
console.log('envLoadedZoomed='+envLoadedZoomed);

//———————————————————————————————————————— set the rem unit

var rawPixel = zoomedWidth() / visible_width; // ⚠️  USED BY OTHER SCRIPTS
var  aiPixel = rawPixel * zoom();

document.documentElement.style.fontSize = aiPixel + 'px';

console.log('rawPixel='+rawPixel);
console.log('aiPixel='+aiPixel);

//———————————————————————————————————————— resize listener

  var resizeListener = window.addEventListener('resize', resize);

//———————————————————————————————————————— set scroll position

var left_margin_px = page_offsetx * aiPixel;
var top_margin_px  = page_offsety * aiPixel;

var envXinit = Math.round(left_margin_px);
var envYinit = Math.round(top_margin_px);

setScroll(); setTimeout(setScroll, 1);

//———————————————————————————————————————— end logging

console.groupEnd();
console.log('next thing');


//:::::::::::::::::::::::::::::::::::::::: methods

//———————————————————————————————————————— zoomedWidth()

function zoomedWidth(){
  var r = globalThis.innerWidth;
  return r;
}

//———————————————————————————————————————— setScroll()

function setScroll(){
  if (envLoadedZoomed) return true;
  window.scrollTo(envXinit, envYinit);
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
    var z = globalThisOuterWidth()/zoomedWidth();
  }

  // firefox
  else{
    var z = w/globalThis.screen.availWidth; 
  }

  if (!areDifferent(z, 1)) z = 1;

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
  if (!pageLoaded) {return true;}

 var zoomFactor = 1;

  // page was just made longer
  if (zoomedWidth() == envPrevWidth) {return true;}
  
  if (globalThis.innerWidth != envRealScreenHeight)
    zoomFactor = zoom();

  else
    // iPhone rotated to landscape
    console.log('iPhone rotated to landscape');

  aiPixel = zoomedWidth() / visible_width * zoomFactor;

  document.documentElement.style.fontSize = aiPixel + 'px';

  envPrevWidth = zoomedWidth();

  return true;
};

/*———————————————————————————————————————— globalThisOuterWidth()

    called by zoom()

    because iPhone returns wrong value in landscape mode */

function globalThisOuterWidth(){
  var r;

  // iPhone rotated to landscape
  if (window.innerWidth == envRealScreenHeight){
    r = window.innerWidth;
  }

  // iPhone rotated to portrait
  else if (globalThis.outerWidth == envRealScreenHeight){
    r = window.innerWidth;
  }

  else r= globalThis.outerWidth;

  return r;
}


//———————————————————————————————————————— fin
