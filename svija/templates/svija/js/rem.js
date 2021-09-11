//———————————————————————————————————————— template: rem.js

// visible_width is supplied by server

var illustrator_pixel = window.innerWidth / visible_width;

//———————————————————————————————————————— safari pinch reload

//  in Safari, when someone pinches to zoom then reloads
//  then reloads, this corrects the page size

var firefox = navigator.userAgent.indexOf('Firefox');

var pure = window.outerWidth/window.innerWidth*100;
var current_zoom = Math.round(pure);

// keyboard zoom levels, unlikely to be pinch levels. 300 is max pinch, so left out

var zoom_levels = [50, 67, 75, 80, 85, 90, 100, 110, 125, 150, 170, 200, 240, 400, 500];
var pinched = zoom_levels.indexOf(current_zoom) < 0 && firefox;

if (pinched) illustrator_pixel = illustrator_pixel*current_zoom/100;

//———————————————————————————————————————— set the rem unit

document.documentElement.style.fontSize = (10 * illustrator_pixel) + 'px';
