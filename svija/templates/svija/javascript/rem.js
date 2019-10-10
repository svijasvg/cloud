//———————————————————————————————————————— serverside: rem.js

//	we can't use 1 rem = 1 pixel because Microsoft browsers
//	only use two decimal places of accuracy for the font-size
//	definition: 1.321px is rounded to 1.32px

// set value of one REM
var ten_pixels = 10 * window.innerWidth/page_visible;
document.documentElement.style.fontSize = ten_pixels + 'px';
alert(ten_pixels);
