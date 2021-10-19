//———————————————————————————————————————— template: screens.js

//———————————————————————————————————————— system js

// var screen_code = "cp";
// var all_screens = {0:'cp', 400:'mb'};

//———————————————————————————————————————— get pixel width of window

// this is temporary

var cutoff = 0.9;
var ratio  = window.innerWidth / window.innerHeight;
if (ratio < cutoff) pixel_width = 300;
else pixel_width = 1200;

//———————————————————————————————————————— find best fit

var correct_screen_code = all_screens[0];
var min_value = 1000000;

for (const [key, value] of Object.entries(all_screens)) {
  if (pixel_width < key && pixel_width < min_value){
    min_value = key;
    correct_screen_code = value;
  }
}

//———————————————————————————————————————— set cookie & redirect

setCookie('screen_code', correct_screen_code, 7);

if (screen_code != correct_screen_code){
  setTimeout(window.location.reload.bind(window.location), 50);
}
