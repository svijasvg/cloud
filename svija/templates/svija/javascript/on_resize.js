//———————————————————————————————————————— template: window_redraw.js

// adapts content to window on resize but not zoom
// var illustrator_pixel set in rem.js

var win_precision    = 50; // higher is more sensitive to redrawing
var win_stored_ratio = get_ratio(win_precision); // width:height
var win_stored_width = window.innerWidth;

window.addEventListener("resize", resizeWindow);

function resizeWindow(){
  if (!page_loaded)                          return false; // page still loading
  if (window.innerWidth == win_stored_width) return false; // height was changed
  if (window_zoomed())                       return false; // zoomed, not resized

  var illustrator_pixel = window.innerWidth / visible_width;
};  

//———————————————————————————————————————— functions

function window_zoomed(){
  new_ratio = get_ratio(win_precision);
  if (new_ratio == win_stored_ratio) return true;
  else return false;
}

function get_ratio(precision){
  var w = window.innerWidth;
  var h = window.innerHeight;
  var r = Math.round(w/h * precision);
  return r;
}

//———————————————————————————————————————— fin
