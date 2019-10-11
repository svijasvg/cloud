//———————————————————————————————————————— template: window_scroll.js

// page_offsets set in admin
// ai set in rem.js

rem_to_pix = window.innerWidth/page_visible; // flash fix
var left_margin_px = page_offsetx * rem_to_pix;
var top_margin_px  = page_offsety * rem_to_pix;

document.body.scrollLeft = Math.round(left_margin_px);
document.body.scrollTop  = Math.round(top_margin_px);
