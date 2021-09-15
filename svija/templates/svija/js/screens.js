//———————————————————————————————————————— template: screens.js

// browser information for server-side use

setCookie('screen', 'cp', 7);

//———————————————————————————————————————— old js

// redirects to desktop  if window is not in portrait mode
// mobile & desktop scripts are the same except for the first and last lines

var cutoff = 0.9;
var ratio  = window.innerWidth / window.innerHeight;
var portrait = ratio < cutoff;

// get url information

var parts = page_url.split('/');
var pge   = parts[4].replace('#', '');

// supplied by system: var responsives = {'desktop':'fr', 'mobile':'fm'};

//if    (portrait) location.href = '/' + responsives['Mobile' ] + '/' + pge;
if (!portrait) location.href = '/' + responsives['Computer'] + '/' + pge;

//———————————————————————————————————————— new js

// in js above:
// var responsive_code = "cp";
// var screens = {'cp':'0', 'mb':'400'};
