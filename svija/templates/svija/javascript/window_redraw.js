//———————————————————————————————————————— template: window_redraw.js
counter=0;

var wn_precision   =  50; // higher is more sensitive to redrawing

var wn_storedRatio = get_ratio(wn_precision); // width:height
var wn_storedWidth = window.innerWidth;

window.addEventListener("resize", resizeWindow);

function resizeWindow(){
  if (!page_loaded)                        return false; // page still loading
  if (window.innerWidth == wn_storedWidth) return false; // height only was changed
  if (!ratio_changed(wn_storedRatio))      return false; // zoomed, not resized

  var illustrator_pixel = window.innerWidth / visible_width;
  document.documentElement.style.fontSize = (10 * illustrator_pixel) + 'px';
};  

//———————————————————————————————————————— functions

function get_ratio(precision){
  var w = window.innerWidth;
  var h = window.innerHeight;
  var r = Math.round(w/h * precision);
  return r;
}

function ratio_changed(old_ratio){
  new_ratio = get_ratio(wn_precision);
  if (new_ratio == old_ratio) return false;
  else return true;
}

//———————————————————————————————————————— fin
