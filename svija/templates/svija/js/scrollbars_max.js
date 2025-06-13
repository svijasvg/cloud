//———————————————————————————————————————— template: scrollbars.js
/*
https://www.toptal.com/developers/javascript-minifier
*/

/*———————————————————————————————————————— notes

    This just resets the aiPixel value after scrollbars
    have been drawn. Otherwise, PC pages have horizontal
    scrollbars because the page is always slightly too wide */

//———————————————————————————————————————— environmental variables

envPrevWidth = zoomedWidthBody();  // used in resize();
envPrevZoom  = zoom();             // used in resize();

//———————————————————————————————————————— set the rem unit

var rawPixel = zoomedWidthBody() / visible_width; // ⚠️  NEEDED IN OTHER SCRIPTS
     aiPixel = rawPixel * zoom();

document.documentElement.style.fontSize = aiPixel + 'px';

setScroll(); setTimeout(setScroll, 1);

//:::::::::::::::::::::::::::::::::::::::: methods

//———————————————————————————————————————— zoomedWidthBody()

function zoomedWidthBody(){
  return document.documentElement.clientWidth;
}


//———————————————————————————————————————— fin
