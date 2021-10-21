//———————————————————————————————————————— page_background.js

try {
  var firstSVG = document.body.getElementsByTagName('svg')[0];
  var classID = '.st' + firstSVG.id + 0;
  var bgcolor = document.querySelector(classID);
  var bgfill = getComputedStyle(bgcolor).fill;
  document.body.style.backgroundColor = bgfill;
} catch (error) { var rien = 0;}
