//———————————————————————————————————————— template: screens.js

//———————————————————————————————————————— system js

// var screen_code = "cp";
// var screens = {'cp':'0', 'mb':'400'};

//———————————————————————————————————————— get pixel width of window

// this is temporary

var cutoff = 0.9;
var ratio  = window.innerWidth / window.innerHeight;
if (ratio < cutoff) pixel_width = 300;
else pixel_width = 1200;

//———————————————————————————————————————— find best fit

var this_screen_code = 'cp';
var min_value = 1000000;

for (const [key, value] of Object.entries(screens)) {
  if (pixel_width < value && pixel_width < min_value){
    min_value = value;
    this_screen_code = key;
  }
}

//———————————————————————————————————————— set cookie & redirect

setCookie('screen', this_screen_code, 7);

alert(screen_code + ' : ' + this_screen_code);

if (screen_code != this_screen_code)  location.reload();
