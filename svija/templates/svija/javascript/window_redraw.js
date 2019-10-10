//———————————————————————————————————————— template: window_redraw.js

var start_delay    = 1.5; // seconds before starting
var wn_delay       = 0.5; // seconds between redraws
var wn_precision   =  50; // higher is more sensitive to redrawing
var wn_already     =   0; // redraw already programmed 

var wn_storedRatio = wn_ratio(); // width:height
var wn_storedWidth = window.innerWidth;

//————— main function

function resizeWindow(){
	var hrf = window.location.pathname; // /fr/accueil or /fm/accueil

	if (hrf.substr(2,1) == 'm')              return false; // mobile site
	if (window.innerWidth == wn_storedWidth) return false; // height only was changed
	if (wn_ratio() == wn_storedRatio)        return false; // zoomed, not resized
	if (wn_already)                          return false; // redraw already programmed

	wn_already = 1;
	setTimeout(wn_redraw, wn_delay * 1000);
};	

//————— add listener

setTimeout(startListener, start_delay * 1000);

function startListener(){
  window.addEventListener("resize", resizeWindow);
}

//————— secondary functions

function wn_redraw(){
	wn_already = 0;
	window.location.reload();
}

function wn_ratio(){
	var w = window.innerWidth;
	var h = window.innerHeight;
	var r = Math.round(w/h * wn_precision);
	return r;
}
