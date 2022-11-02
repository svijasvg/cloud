//———————————————————————————————————————— template: initial_scroll.js
// makes centered over-width pages appear centered on load instead of centering late
// page_offsets set in admin // illustrator_pixel set in rem.js

//————— create full-width div

var full_width = document.createElement('div');
var pix_width = page_width * illustrator_pixel;
//var css_string = 'position:absolute; top:0; left:0; z-index:-9999; height:1000px; width:' + pix_width + 'px';
var css_string = 'position:absolute; top:0; left:0; z-index:-9999; height:1000px; width:100px';

full_width.setAttribute("style", css_string);
full_width.setAttribute("id", "initial_scroll_div");
document.body.appendChild(full_width);

//————— initial scroll

var left_margin_px = page_offsetx * illustrator_pixel;
var top_margin_px  = page_offsety * illustrator_pixel;

x = Math.round(left_margin_px);
y = Math.round(top_margin_px);

function testScroll(){ window.scrollTo(x, y); }
setTimeout(testScroll, 1);

//:::::::::::::::::::::::::::::::::::::::: COPIED

//———————————————————————————————————————— template: rem.js

// visible_width is supplied by server

if (typeof document.documentElement.clientWidth != 'undefined')
  var win_width = document.documentElement.clientWidth;
else
  var win_width = window.innerWidth;

var illustrator_pixel = win_width / visible_width;

//———————————————————————————————————————— safari pinch reload

//  in Safari, when someone pinches to zoom then reloads
//  then reloads, this corrects the page size

var firefox = (navigator.userAgent.indexOf('Firefox') > 0);
var zoom    = Math.round(window.outerWidth/win_width*100);

// keyboard zoom levels, unlikely to be pinch levels. 300 is max pinch, so left out

var levels  = [50, 67, 75, 80, 85, 90, 100, 110, 125, 150, 170, 200, 240, 400, 500];
var pinched = (firefox && typeof levels[zoom] != 'undefined');

if (pinched) illustrator_pixel = illustrator_pixel*zoom/100;

//———————————————————————————————————————— set the rem unit

document.documentElement.style.fontSize = illustrator_pixel + 'px';

//:::::::::::::::::::::::::::::::::::::::: END COPY

//———————————————————————————————————————— template: rem.js

var pix_width = page_width * illustrator_pixel;
initial_scroll_div.style.width = pix_width+'px';
