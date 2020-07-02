//———————————————————————————————————————— template: rem.js

//	can't use 1 rem = 1 pixel because Microsoft browsers
//	round to 2 decimals: 1.321px is rounded to 1.32px

var illustrator_pixel = window.innerWidth / visible_width;
document.documentElement.style.fontSize = (10 * illustrator_pixel) + 'px';


//———————————————————————————————————————— diagnostics

//alert('outer: '+window.outerWidth);

function title_status(){
   win_inner_w = window.innerWidth
   win_inner_h = window.innerHeight
   win_outer_w = window.outerWidth
   win_outer_h = window.outerHeight

   t = 'inner: ' + win_inner_w + 'x'+win_inner_h + ' outer: ' + win_outer_w + 'x'+win_outer_h 
   document.title=t;
}

setInterval(title_status, 0.5);

