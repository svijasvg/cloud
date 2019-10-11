//———————————————————————————————————————— template: rem.js

//	can't use 1 rem = 1 pixel because Microsoft browsers
//	round to 2 decimals: 1.321px is rounded to 1.32px
// <html> fontsize = one REM

var ai_to_browser = window.innerWidth/page_visible_width;
document.documentElement.style.fontSize = (10 * ai_to_browser) + 'px';
