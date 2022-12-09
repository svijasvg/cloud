/*———————————————————————————————————————— on_resize.js

   templates/svija/javascript/on_resize.js

   adapts content to window on resize but not zoom */

//———————————————————————————————————————— predefined values

// var illustrator_pixel set in rem.js

//———————————————————————————————————————— variables

var ratioRange = 50;                    // higher is more sensitive to redrawing
var prevRatio  = get_ratio(ratioRange); // width/height
var prevWidth  = window.visualViewport.width;

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
  prevRatio = get_ratio(ratioRange); // width/height
  var prevWidth = window.visualViewport.width;
};


//:::::::::::::::::::::::::::::::::::::::: functions

//———————————————————————————————————————— isZoomed()

function isZoomed(){
  var r = get_ratio(ratioRange);
  if (r != prevRatio) return false;

  return true;
}

//———————————————————————————————————————— get_ratio(precision)

function get_ratio(precision){
  var w = window.visualViewport.width;
  var h = window.visualViewport.height;
  var r = Math.round(w/h * precision);
  return r;
}


//———————————————————————————————————————— fin
