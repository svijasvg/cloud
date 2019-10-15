//———————————————————————————————————————— template: rem.js

//	can't use 1 rem = 1 pixel because Microsoft browsers
//	round to 2 decimals: 1.321px is rounded to 1.32px

var illustrator_pixel = window.innerWidth / visible_width;
document.documentElement.style.fontSize = (10 * illustrator_pixel) + 'px';
