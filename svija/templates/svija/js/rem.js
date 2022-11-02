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
