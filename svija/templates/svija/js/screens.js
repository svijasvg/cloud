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

var correct_screen_code = all_screens[0][1];
var min_value = 1000000;

for (var x=0; x<all_screens.length; x++){
  key   = all_screens[x][0];
  value = all_screens[x][1];
  if (pixel_width < key && pixel_width < min_value){
    min_value = key;
    correct_screen_code = value;
  }
}

//———————————————————————————————————————— set cookie & redirect

setCookie('screen_code', correct_screen_code, 7);

//alert('server: ' + screen_code + ', calculated: ' + correct_screen_code);

if (screen_code != correct_screen_code){
  if (window.location.href.indexOf('?')>0)
    alert(document.cookie);
  location.reload();
  //setTimeout(window.location.reload.bind(window.location), 5);
}
