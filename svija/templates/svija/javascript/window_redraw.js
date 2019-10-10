//———————————————————————————————————————— serverside: window_redraw.js

// need to do it only when it's not a vertical-only resize

//---------------------------------------- redraw window when it's resized
//---------------------------------------- and only if desktop, not mobile

// redraw if resize is not proportional (then it's a zoom)

var start_delay    = 1.5; // seconds before starting
var wn_delay       = 0.5; // seconds between redraws
var wn_precision   =  50; // higher is more sensitive to redrawing

var wn_already     = 0;
var wn_storedRatio = wn_ratio();
var wn_storedWidth = window.innerWidth;

//---------------------------------------- add listener

setTimeout(startListener, start_delay * 1000);

function startListener(){
  window.addEventListener("resize", resizeWindow);
}

function resizeWindow(){
	var hrf = window.location.pathname; // /fr/accueil or /fm/accueil
	if (hrf.substr(2,1) == 'm')              return false; // mobile site

	if (window.innerWidth == wn_storedWidth) return false; // height only was changed
	if (wn_ratio() == wn_storedRatio)        return false; // zoomed, not resized
	if (wn_already)                          return false; // redraw already programmed

	wn_already = 1;
	setTimeout(wn_redraw, wn_delay * 1000);
};	

//---------------------------------------- reload the window

function wn_redraw(){
	wn_already = 0;
	window.location.reload();
}

//---------------------------------------- ratio of width to height

function wn_ratio(){
	var w = window.innerWidth;
	var h = window.innerHeight;
	var r = Math.round(w/h * wn_precision);
	return r;
}
