//———————————————————————————————————————— template: rem.js

//	use 1 rem = 10 pixels because Microsoft browsers
//	round to 2 decimals: 1 rem=1.321px is rounded to 1.32px
//  this is not precise enough and leads to display errors

//  conversely, if we use 1 rem = 100pixels, various
//  measurements will have small values that will also
//  be rounded by Microsoft browsers.

//  1rem = 10px is a good medium ;-)

//———————————————————————————————————————— pinch to zoom on Safari/Mac

//  Safari/Mac had a specific issue where when someone pinches to zoom
//  and then reloads the page, and then pinches to zoom again, the
//  page size would be all wrong.

//  to fix this, we check for pinch to zoom and automatically zoom the
//  page to the right size if it's not Firefox

//  Google, Edge etc. don't have any issues because pinch-to-zoom has
//  no effect at all on the DOM

// firefox does not support pinch
var firefox = navigator.userAgent.indexOf('Firefox');

var pure = window.outerWidth/window.innerWidth*100;
var current_zoom = Math.round(pure);

// leave out 300 because it is max pinch to zoom
var zoom_levels = [50, 67, 75, 80, 85, 90, 100, 110, 125, 150, 170, 200, 240, 400, 500];
var pinched = zoom_levels.indexOf(current_zoom) < 0 && firefox;

//———————————————————————————————————————— main program

var illustrator_pixel = window.innerWidth / visible_width;
if (pinched) illustrator_pixel = illustrator_pixel*current_zoom/100;

document.documentElement.style.fontSize = (10 * illustrator_pixel) + 'px';

//———————————————————————————————————————— fin
