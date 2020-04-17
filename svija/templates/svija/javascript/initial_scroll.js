//———————————————————————————————————————— template: initial_scroll.js

// page_offsets set in admin
// illustrator_pixel set in rem.js

//————— create full-width div

var full_width = document.createElement('div');
var pix_width = page_width * illustrator_pixel;
var css_string = 'position:absolute; top:0; left:0; z-index:-9; height:10px; width:' + pix_width + 'px';

full_width.setAttribute("style", css_string);
document.body.appendChild(full_width);

//————— initial scroll

var left_margin_px = page_offsetx * illustrator_pixel;
var top_margin_px  = page_offsety * illustrator_pixel;

x = Math.round(left_margin_px);
y = Math.round(top_margin_px);

window.scrollTo(x, y);
