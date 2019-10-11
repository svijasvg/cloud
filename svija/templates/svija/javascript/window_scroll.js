//———————————————————————————————————————— template: window_scroll.js

// page_offsets set in admin
// ai set in rem.js

var left_margin_px = page_offsetx * ai_to_browser;
var top_margin_px  = page_offsety * ai_to_browser;

document.body.scrollLeft = Math.round(left_margin_px);
document.body.scrollTop  = Math.round(top_margin_px);
