//———————————————————————————————————————— template: rem.js

//	can't use 1 rem = 1 pixel because Microsoft browsers
//	round to 2 decimals: 1.321px is rounded to 1.32px

// <html> fontsize = one REM
var ten_pixels = 10 * window.innerWidth/page_visible;
document.documentElement.style.fontSize = ten_pixels + 'px';
