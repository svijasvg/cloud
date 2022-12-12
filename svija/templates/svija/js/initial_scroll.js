//———————————————————————————————————————— template: initial_scroll.js

// makes centered over-width pages appear centered on load instead of centering late
// page_offsets set in admin // aiPixel set in rem.js

//————— initial scroll

var left_margin_px = page_offsetx * aiPixel;
var top_margin_px  = page_offsety * aiPixel;

x = Math.round(left_margin_px);
y = Math.round(top_margin_px);

function testScroll(){ window.scrollTo(x, y); }

testScroll();
setTimeout(testScroll, 1);

//———————————————————————————————————————— fin
