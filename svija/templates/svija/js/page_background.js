//———————————————————————————————————————— page_background.js

try {
  var firstSVG = document.body.getElementsByTagName('svg')[0]
  var classID = '.st' + firstSVG.id + 0
  var firstObj = document.querySelector(classID) // returns first element of this class

  var cssColor = getComputedStyle(firstObj).fill

  //if (cookiesEnabled()){
  if (cssColor != 'none'){
    document.body.parentElement.style.backgroundColor = cssColor // change html style
    document.body.style.backgroundColor = cssColor
  }
} catch (error) { var rien = 0 }
