
/*:::::::::::::::::::::::::::::::::::::::: Vibe Data-Name.js */

/*———————————————————————————————————————— notes

  updated to allow new Illustrator SVG format

  https://www.toptal.com/developers/javascript-minifier

  github.com/svijalove/vibe
  
  ©Svija SAS, Cusset France

  When there are two elements with the same name, it's just
  debug, debug-2 for id

  empty layers are not included in SVG, so can't
  create empty layer for debug */

/*———————————————————————————————————————— EULA

    Copyright (c) Svija

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.
    
    The software is provided "as is", without warranty of any kind, express or
    implied, including but not limited to the warranties of merchantability,
    fitness for a particular purpose and noninfringement. In no event shall the
    authors or copyright holders be liable for any claim, damages or other
    liability, whether in an action of contract, tort or otherwise, arising from,
    out of or in connection with the software or the use or other dealings in
    the software.

    svija.com · hello@svija.com*/


//:::::::::::::::::::::::::::::::::::::::: initialization

var version = '1.0.27'

/*———————————————————————————————————————— start timer */

const d1 = new Date()
let start_time = d1.getTime()

/*———————————————————————————————————————— var scrollElement

    used because horizontally scrolled pages use a different
    element than vertically scrolled images

    this means that listening for scroll events is different:

    window.addEventListener('scroll') 
    document.body.addEventListener('scroll')

   var scrollElement = document.body will be in horz scrolling code */

if (typeof scrollElement == 'undefined')
  var scrollElement = window

/*———————————————————————————————————————— debugging variables

    var stem = "[data-name^='" + kind + separator + "']"
   <rect id="debug" x="120" y="97.541" class="st1" width="866.252" height="395.565"/>
   <rect id="debug_00000182491029671138469570000004975659756911234963_" x="352.422" y="546.311" class="st1" width="515.854" height="249.831"/> */

var debugOn = document.querySelectorAll('[id ^= "debug"]').length > 0

var debugMessages = []
var env_allTlines = []

/*———————————————————————————————————————— separator · types of triggers and events */

const     separator = '/'
const trigger_types = [ 'mouse', 'time', 'scroll' ]
const   event_types = [ 'click', 'over',  'away',  'ovaway', 'ovover', 'press', 'down', 'toggle', 'delay', 'point', 'zone', 'scrub' ]

/*———————————————————————————————————————— conversion dictionaries */

const entity_conversion = {
  '&lt;': '<',
  '&gt;': '>'
}

const entity_conversion_keys = Object.keys(entity_conversion)

const entity_conversion_old = {
  'x002E': '.',
  'x002D': '-',
  'x2F'  : '/',
  'x2B'  : '+',
  'x25'  : '%',
  'x3C'  : '<',
  'x3E'  : '>',
  'x2C'  : ','
}

const trigger_flag_value_to_key = {

  // name & kind are given

  // trigger flags
  'func'  : 'func'       , // no value
  'a'     : 'cursor'     , // no value
  'h'     : 'cursor'     , // no value
  'i'     : 'cursor'     , // no value
  'n'     : 'blank'      , // no value

}

const cursors = {
  'a'           : 'default',
  'h'           : 'pointer',
  'i'           : 'text',
  'default_link': 'pointer'
}

const trigger_flag_value_to_key_value = {
  'a'   : 'a',
  'h'   : 'h',
  'i'   : 'i',
  'func': true,
  'n'   : true
}

const flag_length = { 

  // so we can get value from end of flag
  // # of characters, value follows

  'blank'      : 0,
  'cursor'     : 0,
  'delay'      : 1,
  'ease'       : 0,
  'func'       : 0,
  'handoff'    : 5,
  'order'      : 0,
  'origin'     : 1,
  'rotate'     : 1,
  'autoAlpha'  : 1,
  'xmove'      : 1,
  'ymove'      : 1,
  'scale'      : 1,
  'xscale'     : 2,
  'yscale'     : 2,

}

const eases = {
  'softin' : Power1.easeIn,
  'softout': Power1.easeOut,
  'soft'   : Power1.easeInOut,
  'hard'   : 'none' 
}

const fromtos = {
  '>' : 'to',
  '<' : 'from'
}


/*———————————————————————————————————————— defaults */

const trigger_defaults = {

  'func'  : false,
  'link'  : false,
  'blank' : false,
  'vert'  : true // is scrolling trigger horizontal or vertical

}

const time_trigger_default = 5.0

const event_defaults = {
  'delay'   : 5.0, // only for time/delay anims
  'duration': 0.5,
  'fromto'  : 'to'
}


//:::::::::::::::::::::::::::::::::::::::: model definitions

//———————————————————————————————————————— class Animation

// https://www.w3schools.com/js/js_classes.asp

var animations = {}   // Animations
var functions  = []   // mouse functions called by func flag

class Animation{

  constructor( name, triggers, evnt ){

    this.name     = name     // 20-character string
    this.triggers = triggers // array of trigger_types
    this.evnt     = evnt     // array of event_types
  }

  add_trigger(obj, kind, flags){ //—————————————————————————————————————————————

    // initialize

    var zoopy  = new Trigger
    zoopy.obj  = obj
    zoopy.kind = kind

    if (zoopy.kind == 'mouse') makeClickable(zoopy.obj, true)

    // set defaults

    Object.keys(trigger_defaults).forEach(
      key => { zoopy[key] = trigger_defaults[key] }
    )
     
    if (kind=='time') zoopy['delay'] = time_trigger_default

    for(var x=2; x<flags.length; x++){ //————————————————————————————— loop through flags (kind|name|parameters...)

      // determine flag key from value
      // entity conversion not necessary for trigger_types

      // get correct key
      var val = flags[x]

      if (not_number(val))
        var key = trigger_flag_value_to_key[val]
      else if (kind == 'time') var key = 'delay'

      if (kind=='time' && key=='delay') zoopy[key] = 1 * val 
      else if (key=='func') {
        zoopy.func = true
        zoopy.args = []
        for (var y=x+1; y<flags.length; y++)
          zoopy.args.push(decodeEntities(flags[y]))
        x = 1000 // get out of loop — no other flags can follow func
      }
      else{
        var v = trigger_flag_value_to_key_value[val]
        if (val == '')
          errLog('Extra slash',  obj)
        else if (typeof v == 'undefined')
          errLog('Unknown flag "' + val + '"', obj)
        else zoopy[key] = v
      }

    } //—————————————————————————————————————————————————————————————————————-

    // is scrolling trigger horizontal or vertical

    if (kind == 'scroll')
      if (isHorizontal(obj))
        zoopy.vert = false

    // set link & parent target
 
    zoopy.link = obj.parentNode.hasAttribute('xlink:href') // true false

    if (zoopy.link && zoopy.blank)
      zoopy.obj.parentNode.setAttribute("target", "_blank")

    if (typeof this.triggers == 'undefined') this.triggers = []
    this.triggers.push(zoopy)

  }

  add_event(obj, kind, objId){

    // initialize
    var flags     = objId.slice(2)
    var flagLen   = flags.length
    var zoopy     = new Evnt
    zoopy.obj     = obj
    zoopy.kind    = kind
    zoopy.name    = this.name

    // create dictionary zoopy[key] = flag value

    for(var x=0; x<flags.length; x++){

      var flag = flags[x]

      if (flag.indexOf('_') > -1) flag = convertEntitiesOld(flag)

      var key = this.event_key_from_flag(flag, obj)

      if (typeof zoopy[key] == 'undefined')
          zoopy[key] =  this.get_flag_val(key, flag, obj)
      else
          errLog('Duplicate "'+key+'" flag ignored', zoopy.obj)

    }

    // set default fromto

    if (typeof zoopy.fromto=='undefined') zoopy.fromto = event_defaults.fromto

    // set transparency

/*  events are set to display:none by default (in CSS)
    the only exceptiont to strict logic is for simple mouseovers
    an event with no flag goes from t0 to current transparency */

    zoopy['opacity'] = +window.getComputedStyle(obj).getPropertyValue('opacity')

    if (typeof zoopy['autoAlpha'] == 'undefined'){
      var opacity  = zoopy['opacity']
      var autoAlpha = null
    }
    else{
      var opacity  = zoopy['opacity']
      var autoAlpha = zoopy['autoAlpha']
    }

    var to      = (zoopy.fromto == 'to')
    var visible = (opacity   != '0' )

// log('opacity, autoAlpha, to, visible = ' + opacity +':'+ autoAlpha +':'+ to +':'+ visible) // 0.5:null:true:true

    transparency:{

      // exception · when no flags we assume mouseovers
      if (flags.length == 0 && opacity == 0){
        zoopy['autoAlpha'] = 1
        break transparency
      }

      if (flags.length == 0 && opacity != 0){
        zoopy['autoAlpha'] = opacity
        zoopy.obj.style.opacity = 0
        zoopy['opacity']  = 0
        break transparency
      }

      // all the rest: use current transparency as starting state
      if (autoAlpha == null)
        zoopy['autoAlpha'] = zoopy['opacity']

// OLD EXCEPTIONS COMMENTED OUT
//    // exception · when visible and t100 flag
//    if (to && opacity==1 && autoAlpha==1){
//      zoopy['opacity' ] = 0
//      zoopy.obj.style.opacity = 0
//      break transparency
//    }

//    // error · zero to zero
//    if (opacity == 0 && autoAlpha == 0){
//      zoopy['opacity' ] = undefined
//      zoopy['autoAlpha'] = undefined
//      errLog('Zero to zero transparency', zoopy.obj)
//      break transparency
//    }

    }

    zoopy.opacity = 1*zoopy.opacity   // doesn't seem
    zoopy.autoAlpha = 1*zoopy.autoAlpha // to make a difference

    if (setVisible(zoopy)){
      zoopy.obj.style.visibility = 'inherit'
    }
    zoopy.obj.style.visibility = 'inherit'

////////////////////// CHANGE ZOOPY['FINAL'] TO ZOOPY.FINAL EVERYWHERE WHEN DONE












/*

    if (noFlags && !visible){  // lines 3-5 √
      zoopy['opacity' ] = 0
      zoopy['autoAlpha'] = 1
      zoopy.obj.style.display = 'none'  // zyx
    }

    else if (noFlags && visible && !transform){  // lines 7-8 √
      zoopy['opacity' ] = 0
      zoopy['autoAlpha'] = transCurrent
      zoopy.obj.style.opacity = 0
      zoopy.obj.style.display = 'none'
    }

    else if (noFlags && visible && transform){  // line 10 √
      zoopy.obj.style.display = 'block'
    }

    else if (!visible && zoopy['autoAlpha'] == 0) // lines 12-13 √
      errLog('Transparent object has "t0" flag', obj)

    else if (zoopy['transFinal'] == 0){     // lines 15-16
      zoopy['opacity' ] = transCurrent
    }

    else if (!noFlags){                      // lines 18-20
      zoopy['opacity' ] = transCurrent
      zoopy.obj.style.display = 'block'
    }

    //—————————————————————————————— sumpn sumpn
    if (zoopy.fromto == '>')
      zoopy.obj.style.opacity = zoopy.opacity
    else
      zoopy.obj.style.opacity = zoopy.transFinal
*/

/*::::::::::::::::::::::::::::::::::::::: set display based on transpinit, fromto */

    // set default duration
    if (typeof zoopy.duration=='undefined')
      zoopy.duration= event_defaults.duration
    else zoopy.duration = 1 * zoopy.duration

    // convert rotation to number
    if (typeof zoopy.rotation != 'undefined')
      zoopy.rotation = 1 * zoopy.rotation

    // convert delay to number
    if (typeof zoopy.delay!='undefined')
      zoopy.delay= 1 * zoopy.delay
    else zoopy.delay = 0

    // scrub event_types default to hard ease DEACTIVATED
//  if (zoopy.kind == 'scrub' && typeof zoopy.ease == 'undefined')
//    zoopy.ease = 'none'

    // add to evnt array
    if (typeof this.evnt == 'undefined') this.evnt = []
    this.evnt.push(zoopy)
    

  }

  set_cursor(){
  
    for (var t=0; t<this.triggers.length; t++){


      if (typeof this.triggers[t].cursor != 'undefined'){
        this.triggers[t].obj.style.cursor = cursors[this.triggers[t].cursor]
        log(this.triggers[t].obj.id +' style.cursor set to '+ cursors[this.triggers[t].cursor])
      }
  
      else{
        var is_hand = false
  
        if (this.triggers[t].link ) is_hand = true
        if (this.triggers[t].func ) is_hand = true
        if (this.kind == 'click' ) is_hand = true
        if (this.kind == 'down'  ) is_hand = true
        if (this.kind == 'toggle') is_hand = true

        if (is_hand){
          this.triggers[t].obj.style.cursor = cursors['default_link']
        }
      }
    }
  

  }

  activate_func_flag(){

    // https://stackoverflow.com/questions/359788/how-to-execute-a-javascript-function-when-i-have-its-name-as-a-string
    // https://www.geeksforgeeks.org/how-to-call-function-from-it-name-stored-in-a-string-using-javascript/

    for (var x=0; x<this.triggers.length; x++){
      if (!this.triggers[x].func) continue

      var args = this.triggers[x].args

      functions[this.name] = window['func_'+this.name]

      /* only create if necessary (could have been created on previous pass if
         a single trigger calls several events */

      if (typeof functions[this.name] == 'undefined')
        errLog('Function func_'+this.name+' not found', this.triggers[x].obj)

      else switch (this.triggers[x].kind) {
        case 'mouse' :    mouse_trigger_funcs(this.name, this.triggers[x], args); break
        case 'time'  :   time_trigger_funcs(this.name, this.triggers[x], args); break
        case 'scroll': scroll_triggers_funcs(this.name, this.triggers[x], args); break

        default:
          log('⚠️ unimplemented trig kind: "'+animations[name].triggers[0].kind+'" in animation "'+animation.name+'"')
      }
    }
  }

  delete_if_no_event(){
    for (var t=0; t<this.triggers.length; t++){
      if (typeof this.evnt == 'undefined')
        if (!this.triggers[t].func && !this.triggers[t].link){
          errLog('Trigger with no event, link or function', this.triggers[t].obj)
          delete animations[this.name]
        }
    }
    
    return true
  }

  flagDump(){
    console.group('animation ' + this.name + ':')

    Object.keys(this).forEach(key => {
      if (typeof this[key] != 'undefined')
        if (key=='name') log(key+' ('+typeof(this[key])+'): '+this[key])
        else log(key+' ('+typeof(this[key])+'): '+this[key].length+' object(s)')
    })

    for (var t=0; t<this.triggers.length; t++){
      log('\nTrigger '+t)
      Object.keys(this.triggers[t]).forEach(key => {
        if (typeof this.triggers[t][key] != 'undefined')
          if(key=='obj')log('obj (object): '+convertEntitiesOld(this.triggers[t][key].id))
          else log(key+' ('+typeof(this.triggers[t][key])+'): '+this.triggers[t][key])
      })
    }

    if (typeof this.evnt != 'undefined'){
      for (var x=0; x<this.evnt.length; x++){
        log('\nEvent ' + x)
        Object.keys(this.evnt[x]).forEach(key => {
          if (typeof this.evnt[x][key] != 'undefined')
            if(key=='obj'){
              log('obj (object): '+convertEntitiesOld(this.evnt[x][key].id))
              log('style.visibility: '+this.evnt[x].obj.style.visibility)
              log('style.opacity: '+this.evnt[x].obj.style.opacity)
            }
            else log(key+' ('+typeof(this.evnt[x][key])+'): '+this.evnt[x][key])
        })
      }
    }
    
    console.groupEnd()
  }

  event_key_from_flag(flag, obj){

/*   should return key & flag w/o key
     rename to split_key_flag
     https://stackoverflow.com/a/2917186  for how to do it

     is programmed specifically to optimize key finding
     needs to be updated when flags are modified  */

    switch(flag){
      case 'softout': return 'ease'    // whole flag
      case 'softin' : return 'ease'
      case 'soft'   : return 'ease'
      case 'hard'   : return 'ease'
      case '>'      : return 'fromto'
      case '<'      : return 'fromto'
    
    }

    switch(flag.slice(0,3)){
      case '+x%'   : return 'xscale'    // first 3 chars
      case '-x%'   : return 'xscale'
      case '+y%'   : return 'yscale'
      case '-y%'   : return 'yscale'
    }

    switch(flag.slice(0,2)){
      case '+x'    : return 'xmove'     // first 2 chars
      case '-x'    : return 'xmove'
      case '+y'    : return 'ymove'
      case '-y'    : return 'ymove'
      case 'x%'    : return 'xscale'
      case 'y%'    : return 'yscale'
      case '+%'    : return 'scale'
      case '-%'    : return 'scale'
    }

    switch(flag.slice(0,1)){
      case '%'    : return 'scale'      // first 1 char
      case '<'    : return 'rotate'
      case 'd'    : return 'delay'
      case 'o'    : return 'origin'
      case 't'    : return 'autoAlpha'
//    case 'x'    : return 'xmove'
//    case 'y'    : return 'ymove'
    }

    if (flag.slice(-1) == '>')    return 'rotate'    // /130> rotation clockwise
    if (parseFloat(flag) == flag) return 'duration'  // integer means duration

    if (flag != '')
      errLog('Unknown flag "' + flag + '"', obj)
    else
      errLog('Extra slash', obj)

    return null 
  }

  get_flag_val(key, flag, obj){
    var flag_len = flag_length[key]

    if (key=='ease')   return eases[flag]
    if (key=='fromto') return fromtos[flag]
    if (flag_len == 0) return flag
    if (key=='origin') return convert_origin(flag)

    if (key=='rotate')
      if (flag.slice(-1)=='>') return flag.slice(0, flag.length-1)
      else return 0-flag.slice(1, flag.length)
  
    if (key=='autoAlpha'){
       var v = flag.substr(flag_len)/100
       return v
    }

    if (key=='xmove' || key=='ymove')
      if (flag.slice(0,1)=='-')           // -x200
        return 0-1*flag.substr(flag_len+1)
      else if (flag.slice(0,1)=='+')      // +x200
        return flag.substr(flag_len+1)
      else return flag.substr(flag_len)  //  x200
  
    if (key=='scale' || key=='xscale' || key=='yscale'){
      var rest

      if (flag.slice(0,1)=='-')                 // -%200, -x%200
        rest = (0-flag.substr(flag_len+1))/100

      else if (flag.slice(0,1)=='+')            // +%200, +x%200
        rest = (flag.substr(flag_len+1)/100)

      else rest = (flag.substr(flag_len)/100)  //  %200, x%200

      if (!isNaN(rest)) return rest
      else{
        errLog('Invalid scaling factor', obj)
        return 1
      }
    }

    return flag.substr(flag_len)
  }


}


/*———————————————————————————————————————— class Trigger
    */

class Trigger{

  constructor( name, obj, kind, cursor, func, args, link, blank, delay, vert){

    this.name       = name         // 20-character string
    this.obj        = obj          // object reference
    this.kind       = kind         // string · kind of trig                    scroll, mouse, time 

    // flags
    this.cursor     = cursor       // string · cursor on pointerover              a, h, t (arrow, hand, text)
    this.func       = func         // boolean · calls function of same name     onclick only 
    this.args       = args         // array · args passed to function           all flags following name
    this.link       = link         // boolean · is an SVG link                  programmatically
    this.blank      = blank        // boolean · link target is _blank           n
    this.delay      = delay        // number of seconds before activation (time trig)
    this.vert       = vert         // scrolling trigger is horizontal or vertical
  }
}

/*———————————————————————————————————————— class Evnt
    */

class Evnt{

  constructor( name, obj, kind, delay, handoff, handwait, duration, ease,
               xmove, ymove, origin, rotate, scale, xscale, yscale, autoAlpha, opacity ){

    this.name        = name         // 20-character string
    this.obj         = obj          // object reference
    this.kind        = kind         // string · kind of evnt                  click, over, down, away, ovaway, ovover, down, toggle, visible

    // flags
    this.delay       = delay        // number · seconds before animation starts
    this.handoff     = handoff      // string · following animation
    this.handwait    = handwait     // number · seconds before calling following animation

    // GSAP-related flags
    this.duration    = duration     // number · duration in seconds             34.5 (1st number)
    this.ease        = ease         // animation ease                           in, out, inout, noease
    this.xmove       = xmove        // x movement                               x-30
    this.ymove       = ymove        // y movement                               y+25
    this.origin      = origin       // origin point                             o0,0 to o100,100
    this.rotate      = rotate       // number · rotation                        >20 or <45.5
    this.scale       = scale        // number · percentage to scale             %150
    this.xscale      = xscale       // number · percentage to scale x           x%20
    this.yscale      = yscale       // number · percentage to scale y           y%30
    this.autoAlpha   = autoAlpha    // number · percentage autoAlpha            o30
    this.opacity = opacity  // number · opacity/autoAlpha           programmatically
  }
}


//:::::::::::::::::::::::::::::::::::::::: program

/*———————————————————————————————————————— ▼ start logging
    */

console.groupCollapsed('Svija Vibe')

//console.log()
console.table(['apples', 'oranges', 'pears'])

/*———————————————————————————————————————— disambiguate clipping masks COMMENTED OUT

——— A clipping path has three elements:

    1. rect object (the actual path used to clip)
    2. clipPath object (with a <use tag referring to #1)
    3. clipped object (with a style="clip-path:url(# declaration referring to #2

——— problems with this:

    1. animating the mask itself (clipping path has a custom name in AI)

       the clipping masks in the SVG use duplicate ID's for the mask and the
       parent container. in order to animate the mask only, we change the IDs
       of #2 and #3 above, leaving only #1 to be animated

    2. a group is being clipped

       the clipped group is given the style="clip-path" attribute itself,
       instead of being in a sub <g>. this means that animating the 
       clipped group animates the clipping path with it

       this is why adding a second level of group solved the problem.

    3. in AI, a clipping mask is named with a minus sign - or .

       in exporting the .svg, Illustrator is inconsistent about converting
       the - or . to an entity
   
——— the script does three things:

    1. "moves" the clippedObject status to the parent <g> element
       so that when the clipped object is moved, the clipping path
       is not (problem #2 above)

    2. modifies the ID elements #2 and #3 above so that only the rect
       keeps the original ID and will thus be animated (probem #1 above)

    3. fixes the issue where a - sign is not consistently represented */

//    <defs>
//        <rect id="aiId" x="360.49" y="113.505" width="371.287" height="144.554"/>
//    </defs>
//    
//    <clipPath id="aiId_00000088841081244737966180000018036638614755142529_">
//      <use xlink:href="#aiId"  style="overflow:visible;"/>
//    </clipPath>
//    
//    <g style="clip-path:url(#aiId_00000088841081244737966180000018036638614755142529_);">
//      <image style="overflow:visible;" width="750" height="500" xlink:href="../../Animation/Links/tennis.jpg"  transform="matrix(1 0 0 1 360.49 113.505)"></image>
//    </g>

/* the solution is to get the id of the rect and make display:block
if I just calculate the ID from the other paths, it might break if
illustrator has multiple objects with the same ID's

better to get it "officially", by following the reference in the clipPath

I can get all the "use" tags and look for a similar ID */

/*log('cleaning up clipping paths…')

const clippedObjects = document.querySelectorAll("[style^='clip']")

for(var x=0; x<clippedObjects.length; x++){

  var clippedObj = clippedObjects[x]                     // object #3 above
  var pathUrl    = clippedObj.style.clipPath
  var pathId     = pathUrl.slice(6, pathUrl.length-2)

  var clipPath   = document.getElementById(pathId)      // object #2 above
  minusPeriod(clipPath, pathId)                                  // fix minus sign (fix #3 above)

  var defsId     = clipPath.firstElementChild.getAttributeNS('http://www.w3.org/1999/xlink', 'href').slice(1)

  var defsObj    = document.getElementById(defsId)

  // move clipped object status to parent <g>  (fix #1 above)
  var parentG = getParentG(clippedObj)
  if (parentG != null){
    parentG.style.clipPath = pathUrl
    clippedObj.style.clipPath = ''
    clippedObj = parentG
  }

  if (pathId.slice(0,6) != 'SVGID_'){ // IF IT HAS CUSTOM NAME /////////////////// this breaks animation/22
    try{

      // disambigate custom path names (fix #2 above)
      var newId  = 'CP'     + pathId
      var newUrl = 'url("#' + newId + '")'

      clippedObj.style.clipPath = newUrl
      clipPath.id               = newId

      try{defsObj.style.visibility = 'inherit'} catch(e){log('object ' + decodeEntities(defsId) + ' could not be set to visibility:inherit')}

    }
    catch(msg){ log('⚠️  object with ID '+convertEntitiesOld(pathId)+' could not be updated:\n'+msg+ ' (line 779)') }
  }
}

log('clipping paths verified') */

/*———————————————————————————————————————— register triggers by type
    */

console.groupCollapsed('registering triggers…')

trigger_types.forEach(kind => {
  var stem = "[data-name^='" + kind + separator + "']"
  var obj_array = Array.from(document.querySelectorAll(stem))

  // loop through adding trigger_types
  for(var x=obj_array.length-1; x>-1; x--){ // reverse order to match layer palette order
    var obj   = obj_array[x]
    var str   = obj.dataset.name
    var flags = str.split(separator)

    // doesn't have at least trig and name
    if (flags.length<2) continue 

//  // is a duplicate; AI added _00000018952208152505492020000014739121534903857057_ to ID
//  if (flags[flags.length-1].length > 50)
//    flags[flags.length-1] = flags[flags.length-1].slice(0, -52)

    //  kind = flags[0]
    var name = flags[1]

    if (typeof animations[name] == 'undefined') animations[name] = new Animation(name)
    animations[name].add_trigger(obj, kind, flags)
  }

  // log results
  if (obj_array.length != 0)log(obj_array.length+' '+ kind+' triggers registered')
  //                   else log('—› no '+kind+' trigger_types')
})

console.groupEnd()

/*———————————————————————————————————————— register events by type
    */

console.groupCollapsed('registering events…')

event_types.forEach(kind => {
  var stem = "[data-name^='" + kind + separator + "']"
  var obj_array = Array.from(document.querySelectorAll(stem))

  // loop through adding events
  for(var x=0; x<obj_array.length; x++){

    var obj   = obj_array[x]
    var str   = convertEntities(obj.dataset.name)
    var flags = str.split(separator)

    //  kind = flags[0]
    var name = flags[1]

    if (Object.keys(animations).includes(name))
      animations[name].add_event(obj, kind, flags)
    else
      errLog('Event with no trigger', obj)
  }

  // log results
  if (obj_array.length != 0) log(obj_array.length+' '+ kind+' events registered')
  //                    else log('—› no '+kind+' event_types')

})

console.groupEnd()

/*———————————————————————————————————————— set cursors and activate "func" flags
    */

console.groupCollapsed('setup & error checking…')
log('setting cursors & activating "/func" functions…')

Object.keys(animations).forEach(name => {
  animations[name].set_cursor()
  animations[name].activate_func_flag() // method of Animation class, line 327
})

/*———————————————————————————————————————— delete unused trigger_types
    */

log('checking for eventless triggers…')

Object.keys(animations).forEach(name =>
  animations[name].delete_if_no_event()
)

console.groupEnd()

/*———————————————————————————————————————— activate events by type
    */

console.groupCollapsed('activating events…')

Object.keys(animations).forEach(name => {

  // not necessary to go through all trigger_types
  // the first one is enough to set up the event

  switch (animations[name].triggers[0].kind) {
    case 'mouse' :  activate_mouse_events(animations[name]); break
    case 'time'  :   activate_time_events(animations[name]); break
    case 'scroll': activate_scroll_events(animations[name]); break

    default:
      log('⚠️ unimplemented trigger kind: "'+animations[name].triggers[0].kind+'" in animation "'+name+'"')
  }

})

console.groupEnd()

/*———————————————————————————————————————— end timer
    */

const d2 = new Date()
let end_time = d2.getTime()

log((end_time-start_time)+'ms elapsed')

/*———————————————————————————————————————— visible triggers

// https://stackoverflow.com/a/1938465  */


if (debugOn){
  trigger_types.forEach(kind => {
    var stem = "[data-name^='" + kind + separator + "']"
    var obj_array = Array.from(document.querySelectorAll(stem))
  
    // loop through adding events
    for(var x=0; x<obj_array.length; x++){
      var obj   = obj_array[x]
      obj.style.display = 'block'
      obj.style.opacity = 0.3
    }
  })
}

/*———————————————————————————————————————— reset all timelines
    */

for (var x=0; x<env_allTlines.length; x++){
  var tline = window[env_allTlines[x]]
  tline.pause(0)
}

/*———————————————————————————————————————— end console.groupCollapsed

      Svija Vibe Debugging
      • Function func_cloudModuleLink not found in cloudModule.ai › mouse/cloudModuleLink/n/fu
      • Function func_cloudForceLink not found in cloudModule.ai › mouse/cloudForceLink/func/mb   */

// remove cloud module related errors
if (debugOn && debugMessages.length > 0){
  for (var x=debugMessages.length-1; x>-1; x--){
    var str = debugMessages[x]
    if (str.indexOf('cloudModule') > 0)
      var z = debugMessages.splice(x, 1)
  }
}

if (debugOn && debugMessages.length > 0) alert('Svija Vibe Debugging\n• ' + debugMessages.join('\n• '))
console.groupEnd()

/*———————————————————————————————————————— ▲ name debugging
    */

if (typeof debug_name != 'undefined'){
	try { animations[debug_name].flagDump(); } catch (error) { log('⚠️  debug_name = \'' + debug_name + '\' — animation not found.') }
}


//:::::::::::::::::::::::::::::::::::::::: program trigger "func" functions

/*———————————————————————————————————————— mouse_trigger_funcs(name, triggers, args)
    */

function mouse_trigger_funcs(name, triggers, args){
  triggers.obj.addEventListener('click', functions[name].bind(null, ...args)) 
}

/*———————————————————————————————————————— time_trigger_funcs(name, triggers, args)
    */

function time_trigger_funcs(name, triggers, args){
  setTimeout(functions[name].bind(null, ...args), triggers.delay*1000)
}

/*———————————————————————————————————————— scroll_triggers_funcs(name, triggers, args)
    */

function scroll_triggers_funcs(name, triggers, args){

  var obj = triggers.obj

//var rect = obj.getBBox()             // get bounding box of trig object
  var rect = transformedRect(obj)      // get bounding box of trig object, including transformations

  var trig_top = rect['y']             // top

  scrollElement.addEventListener('scroll', lstn_scroll_func.bind(null, name, triggers, trig_top, args)) 
}


//:::::::::::::::::::::::::::::::::::::::: activate events

/*———————————————————————————————————————— activate_mouse_events(animation)
    */

function activate_mouse_events(animation){

  if (typeof animation.evnt == 'undefined')
    return true  // is link or function

  for (var x=0; x<animation.evnt.length; x++){
    switch (animation.evnt[x].kind) {
      case undefined: break // if it's just a link or func
  
      case 'click' : add_mouse_single(animation, x, 'pointerup'  ); break
      case 'press' : add_mouse_single(animation, x, 'pointerdown'); break
      case 'over'  : add_mouse_single(animation, x, 'pointerover'); break
      case 'away'  : add_mouse_single(animation, x, 'pointerout' ); break // or pointerleave
  
      // special cases
      case 'ovaway': add_mouse_ovaway(animation, x); break
      case 'ovover': add_mouse_ovover(animation, x); break
      case 'down'  :   add_mouse_down(animation, x); break
      case 'toggle': add_mouse_toggle(animation, x); break
  
      default:
        errLog('Unknown mouse event', animation.evnt[x])
    }
  }

  log('mouse events activated')
}

/*———————————————————————————————————————— activate_time_events(animation)
    */

function activate_time_events(animation){

  if (typeof animation.evnt == 'undefined')
    return true  // is link or function

  for (var x=0; x<animation.evnt.length; x++){
    switch (animation.evnt[x].kind) {
    case 'delay':
      add_time_delay(animation, x)
      break

    default:
      if (typeof animation.evnt[x].kind != 'undefined')
           errLog('Unknown time event', animation.evnt[x])
      else errLog('Missing time event', animation.evnt[x])
    }
  }

  log('time events activated')
}

/*———————————————————————————————————————— activate_scroll_events(animation)
    */

function activate_scroll_events(animation){

  if (typeof animation.evnt == 'undefined') return true   // is link or function

  for (var x=0; x<animation.evnt.length; x++){
    switch (animation.evnt[x].kind) {
    case 'point':
      addScrollPoint(animation, x)
      break

    case 'zone':
      addScrollZone(animation, x)
      break

    case 'scrub':
      addScrollScrub(animation, x)
      break

    default:
      if (typeof animation.evnt[x].kind != 'undefined')
           errLog('Unknown scroll event', animation.evnt[x])
      else errLog('Missing scroll event', animation.evnt[x])
    }
  }

  log('scroll events activated')
}


//:::::::::::::::::::::::::::::::::::::::: addEventListener type functions

/*———————————————————————————————————————— add_time_delay(animation)
    */

function add_time_delay(animation, x){

  delay  = animation.triggers[0].delay * 1000
  params = gsapParams(animation.evnt[x])

  createTline(animation.name+x, animation.evnt[x], params)
  setTimeout(lstn_play, delay, animation.name+x, animation.evnt[x])

}

/*———————————————————————————————————————— add_mouse_single(animation, x, type)
    */

function add_mouse_single(animation, x, type){

  params = gsapParams(animation.evnt[x])

  for (var t=0; t<animation.triggers.length; t++){

    createTline(animation.name+x, animation.evnt[x], params)

    animation.triggers[t].obj.addEventListener(type, lstn_play.bind(null, animation.name+x, animation.evnt[x]), false)
  }
}

/*———————————————————————————————————————— add_mouse_ovaway(animation, x)

    */
// rotation is not cumulative (rotating to 90° twice just turns to 90°)

function add_mouse_ovaway(animation, x){

  params = gsapParams(animation.evnt[x])

  for (var t=0; t<animation.triggers.length; t++){
    createTline(animation.name+x, animation.evnt[x], params)
    animation.triggers[t].obj.addEventListener('pointerover',  lstn_play.bind(null, animation.name+x, animation.evnt[x]   ), false);
    animation.triggers[t].obj.addEventListener('pointerout',   lstn_reverse.bind(null, animation.name+x , animation.evnt[x]), false);
  }

}

/*———————————————————————————————————————— add_mouse_down(animation, x)
    */

// rotation is not cumulative (rotating to 90° twice just turns to 90°)

function add_mouse_down(animation, x){

  params = gsapParams(animation.evnt[x])

  for (var t=0; t<animation.triggers.length; t++){

    createTline(animation.name+x, animation.evnt[x], params);

    animation.triggers[t].obj.addEventListener('pointerdown', lstn_play.bind(null, animation.name+x, animation.evnt[x]), false);

    animation.triggers[t].obj.addEventListener('pointerup',   lstn_reverse.bind(null, animation.name+x , animation.evnt[x]                         ), false);
  }

}

/*———————————————————————————————————————— add_mouse_toggle(animation, x)

    */

function add_mouse_toggle(animation, x){

  params = gsapParams(animation.evnt[x]);

  for (var t=0; t<animation.triggers.length; t++){
    createTline(animation.name+x, animation.evnt[x], params);
    animation.triggers[t].obj.addEventListener('pointerup', lstn_mouse_toggle.bind(null, animation.name+x, animation.evnt[x]), false);
  }
}

/*———————————————————————————————————————— add_mouse_ovover(animation, x)

    same as add_mouse_toggle */

// rotation is not cumulative (rotating to 90° twice just turns to 90°)

function add_mouse_ovover(animation, x){

  params = gsapParams(animation.evnt[x]);

  for (var t=0; t<animation.triggers.length; t++){
    createTline(animation.name+x, animation.evnt[x], params);
    animation.triggers[t].obj.addEventListener('pointerover', lstn_mouse_toggle.bind(null, animation.name+x, animation.evnt[x]), false);
  }
}

/*———————————————————————————————————————— addScrollPoint(animation,x)

    can have multiple triggers that set off the animation

    it is the fact that the "point" crosses the top border of the window
    that triggers the animation — not if it's visible already or not */

function addScrollPoint(animation, whichEvent){

  for (var t=0; t<animation.triggers.length; t++){

    var obj  = animation.triggers[t].obj
//  var rect = obj.getBBox()              // get bounding box of trig object
    var rect = transformedRect(obj)      // get bounding box of trig object, including transformations
    var vert = animation.triggers[t].vert

    if (vert)
      var startPx = rect['y']                  // top of box, in pixels
    else
      var startPx = rect['x']                  // left of box, in pixels

log('—————————————————————————————————-- startpx: '+startPx)

    var params = gsapParams(animation.evnt[whichEvent])
    createTline(animation.name+whichEvent, animation.evnt[whichEvent], params)

    scrollElement.addEventListener('scroll', listenScrollPoint.bind(null, animation, whichEvent, vert, startPx)) 

  }
}

/*———————————————————————————————————————— addScrollScrub(animation,x)
    */

function addScrollScrub(animation, whichEvent){

  for (var t=0; t<animation.triggers.length; t++){

    var obj  = animation.triggers[t].obj
    var rect = transformedRect(obj)      // get bounding box of trig object, including transformations
//  var rect = obj.getBBox()                // get bounding rect of trig object
    var vert = animation.triggers[t].vert

    if (vert){
      var startPx = rect['y'] < 0 ? 0 : rect['y']  // top
      var endPx = startPx + rect['height']    // bottom
    }
    else{
      var startPx = rect['x'] < 0 ? 0 : rect['x']  // top
      var endPx = startPx + rect['width']    // bottom
    }

    var params = gsapParams(animation.evnt[whichEvent])

    createTline(animation.name+whichEvent, animation.evnt[whichEvent], params)
    scrollElement.addEventListener('scroll', listenScrollScrub.bind(null, animation, whichEvent, vert, startPx, endPx, 0)) 

    // in case something should already be visible
    listenScrollScrub(animation, whichEvent, vert, startPx, endPx, params, 0) 
  }
}

/*———————————————————————————————————————— addScrollZone(animation,x)
    */

function addScrollZone(animation, whichEvent){

  for (var t=0; t<animation.triggers.length; t++){

    var obj  = animation.triggers[t].obj
//  var rect = obj.getBBox()              // get bounding rect of trig object
    var rect = transformedRect(obj)      // get bounding box of trig object, including transformations
    var vert = animation.triggers[t].vert

    if (vert){
      var startPx = rect['y'] < 0 ? 0 : rect['y']  // top
      var endPx = startPx + rect['height']    // bottom
    }
    else{
      var startPx = rect['x'] < 0 ? 0 : rect['x']  // top
      var endPx = startPx + rect['width']    // bottom
    }

    var params = gsapParams(animation.evnt[whichEvent])

    createTline(animation.name+whichEvent, animation.evnt[whichEvent], params)
    scrollElement.addEventListener('scroll', listenScrollZone.bind(null, animation, whichEvent, vert, startPx, endPx)) 

    // in case something should already be visible
    listenScrollZone(animation, whichEvent, vert, startPx, endPx) 
  }
}


//:::::::::::::::::::::::::::::::::::::::: functions called by events

/*———————————————————————————————————————— lstn_scroll_func(name, triggers, trig_top, args)

    this was not finished betriggers it involves adding new variables and
    making the triggers functionality more complex.

    since most of that code will have to be rewritten when loop, reset and reverse
    are added, I decided to hold off (nobody will be using this in the near future).

    also: consider changing to "when triggers is entirely visible"
    instead of "when top crosses top" */

function lstn_scroll_func(name, triggers, trig_top, args){

  var page_top     = document.documentElement.scrollTop || document.body.scrollTop
  var pixel_height = window.innerHeight

  var rem_top = page_top / aiPixel
/*

    for this to execute:

    1. scroll triggers has to be below top of page, then
    2. scroll triggers has to be above top of page, and
    3. function cannot already have been set off by the 1-2 transition

    need a boolean variable specific to this triggers above/below (is_above), set on load
    need a boolean variable specific to this triggers already done (is_done), initialized false on load

*/

  if (trig_top < rem_top)
    if (typeof functions[name] != 'undefined'){
      functions[name](...args) 
      delete functions[name]
    }


}

/*———————————————————————————————————————— listenScrollPoint(animation, which_event, vert, startPx)

// https://stackoverflow.com/questions/4096863/how-to-get-and-set-the-current-web-page-scroll-position

/*    special cases:
 
      • top is visible to start with
      • evnt transparency default is visible to start with */

// called every time a scroll evnt

      // tline.totalTime(0)
      // tline.totalTime(tline.totalDuration())

  // goes on when trig object top scrolls up past top of page
  

function listenScrollPoint(animation, whichEvent, vert, startPx){

  if (vert)
    var pageStart = document.documentElement.scrollTop  || document.body.scrollTop
  else
    var pageStart = document.documentElement.scrollLeft || document.body.scrollLeft

  var obj        = animation.evnt[whichEvent].obj
  var tlineName  = animation.name + whichEvent + '_timeline'
  var tline      = window[tlineName]

  pageStart = pageStart / aiPixel

  if (startPx < pageStart)
    if(!tline.isActive() && tline.totalTime() == 0)    // if hasn't yet run, play it
      playTimeline(tline, 0.01)
}

/*———————————————————————————————————————— listenScrollScrub(animation, x, trig_top, trig_bot, params)

    executed for the first time the first time on load
    and thereafter each time the window is scrolled

    ways to get to correct position:
    - seek(seconds) · allows relative jumps
    - time(seconds) · doesn't include repeats & delays
    - totalTime() · includes repeats & delays (what I want)

    ways to get timeline length
    - .totalDuration()

    https://greensock.com/docs/v3/GSAP/Timeline/totalTime()
    https://greensock.com/forums/topic/8287-most-efficient-way-of-setting-timeline-playhead/

    "first" is used to know if it was requestd from outside the function, or recursively
    this has been added to double the frequency of checking for scroll trigger_types
    betriggers the experience on mobile was bad bad bad
*/

var scrub_foix = 8 // how many extra calls are made compared to scroll trigger_types
var scrub_rate = 10 // how many ms between extra calls

function listenScrollScrub(animation, whichEvent, vert, startPx, endPx, params, fois){

  if (vert){
    var pageStart = document.documentElement.scrollTop || document.body.scrollTop
    var pageSize  = window.innerHeight
  }
  else{
    var pageStart = document.documentElement.scrollLeft || document.body.scrollLeft
    var pageSize  = window.innerWidth
  }

  pageStart = pageStart / aiPixel

  var obj       = animation.evnt[whichEvent].obj
  var tlineName = animation.name + whichEvent + '_timeline'
  var tline     = window[tlineName]

  if (typeof tline == 'undefined'){
    log(tlineName+' created')
    window[tlineName] = new gsap.timeline({paused:true})
    var tline = window[tlineName]

    tline[animation.evnt[whichEvent].fromto](obj, params)

  }

  // % of bar above top of window = % of timeline

  var triggerActive = false
  
  // trig is activated
  if (startPx < pageStart && endPx > pageStart){
    triggerActive = true

//  makeClickable(obj, true) //—————————————————————————————————————————————————————————————————-- is this too much?
    var triggerSize = endPx - startPx
    var passed      = pageStart - startPx
    var pcent       = passed/triggerSize
    pcent = Math.round(pcent * 10000)/10000 // percent + 2 decimals
    var newTime = tline.totalDuration() * pcent

    tline.totalTime(newTime)
  
  }

  else {

    // if trig object is below top of page, snap to 0
    if (startPx > pageStart){
      tline.totalTime(0)
    }

    // if trig object is above top of page, snap to 100
    if (endPx < pageStart){
      tline.totalTime(tline.totalDuration())
//    if (params['autoAlpha'] == 0) makeClickable(obj, false)
    }
  }

  // re-request same function to double frequency

  if (triggerActive && fois < scrub_foix)
    setTimeout(listenScrollScrub, scrub_rate, animation, whichEvent, startPx, endPx, params, fois+1)
}

/*———————————————————————————————————————— listenScrollZone(animation, x, trig_top, trig_bot, params)
    */

  // goes on when trig top scrolls up past top of page
  // goes off when trig object bottom < bottom of page

/*    called on load then on each scroll trig

   https://stackoverflow.com/questions/4096863/how-to-get-and-set-the-current-web-page-scroll-position

      special cases:
 
      • top is visible to start with
      • evnt transparency default is visible to start with */

// called every time a scroll evnt

function listenScrollZone(animation, whichEvent, vert, startPx, endPx, params){

  if (vert){
    var pageStart = document.documentElement.scrollTop || document.body.scrollTop
    var pageSize  = window.innerHeight
  }
  else{
    var pageStart = document.documentElement.scrollLeft || document.body.scrollLeft
    var pageSize  = window.innerWidth
  }

  var pageEnd     = pageStart + pageSize

  pageStart       = pageStart / aiPixel
  pageEnd         = pageEnd   / aiPixel

  var obj         = animation.evnt[whichEvent].obj
  var tlineName   = animation.name + whichEvent + '_timeline'
  var tline       = window[tlineName]

  var tlReversed  = tline.reversed()
  var tlPlaying   = tline.isActive()

  if (startPx > pageStart && endPx < pageEnd) var triggerActive = true
                                         else var triggerActive = false

  if (tline.totalTime() == tline.totalDuration()) var tlPosition    = 'end'
                 else if (tline.totalTime() == 0) var tlPosition    = 'beginning'
                                             else var tlPosition    = 'middle'

  if(triggerActive){
    if (!tlPlaying && tlPosition != 'end') tline.play()
    if ( tlPlaying && tlReversed)          tline.play()
  }
  else{
    if (!tlPlaying && tlPosition != 'beginning') tline.reverse()
    if ( tlPlaying && !tlReversed)               tline.reverse()
  }

}

/*———————————————————————————————————————— lstn_mouse_toggle(obj, params)
    */

function lstn_mouse_toggle(namex, evntx, params){

  var obj      = evntx.obj
  var tlineName = namex + '_timeline'
  var tline    = window[tlineName]

  if (tline.isActive())
    if (tline.reversed()) tline.play() // was playing backwards: play forwards
    else tline.reverse()               // was playing forwards: play backwards
  else{
    if (tline.totalTime() == 0){       // was stopped at beginning
//    makeClickable(obj, true)         // play forwards
      playTimeline(tline)
    }
    else{                              // was stopped at end
//    makeClickable(obj, true)         // play backwards
      tline.reverse()
    }
  }

}

/*———————————————————————————————————————— lstn_play(obj, params)
    */

//nction lstn_play(animation, params){
function lstn_play(namex, evntx){

  obj = evntx.obj

  var funcName = namex + '_timeline'
  var tline    = window[funcName]

  // play if it's not playing or if it's reversed
  if (!tline.isActive() || (tline.isActive() && tline.reversed())){
//  makeClickable(obj, true)
    tline.play()
  }
}

/*———————————————————————————————————————— lstn_reverse(obj, params)
    */

//nction lstn_reverse(animation){
function lstn_reverse(namex, evntx){
// NEED TO MAKE OBJECT VISIBLE IF IT WAS MADE NON-EXISTANT
  var funcName = namex + '_timeline'
//makeClickable(evntx.obj, true)
  window[funcName].reverse()
}


//:::::::::::::::::::::::::::::::::::::::: utility functions

/*———————————————————————————————————————— makeClickable(obj, exists)

    used only for triggers, which are not animated */

function makeClickable(obj, bool){
//log(convertEntitiesOld(obj.id)+' bool set to '+bool)

  if (bool){
    obj.style.pointerEvents = 'visiblePainted'
  //obj.style.visibility    = 'inherit'
  }
  else{
    obj.style.pointerEvents = 'none'
    //obj.style.pointerEvents = 'none'
  //obj.style.visibility    = 'hidden'
  }
}

/*———————————————————————————————————————— convert_origin(origin)

    the _x2C_ is not converted when the flags are read betriggers
    flags are only converted if they have entities in first
    three characters */

// bug is betriggers when , is in first three characters it's converted, otherwise not

function convert_origin(origin){
  if (typeof origin == 'undefined') return "50% 50%"

  origin = origin.slice(1)

  var parts = origin.split(',')

//if (origin.indexOf(',') > 0)
//  var parts = origin.split(',')
//else
//  var parts = origin.split('_x2C_')

  return parts.join('% ') + '%'
}

/*———————————————————————————————————————— gsapParams(evnt)
    */

function gsapParams(evntx){

  var params = {}

  params['duration']          = evntx.duration==0 ? 0.001:evntx.duration

  if (typeof evntx.ease      != 'undefined') params['ease'           ] = evntx.ease; else params['ease'] = Power1.easeInOut 

//if (typeof evntx.delay     != 'undefined') params['delay'          ] = evntx.delay        
  if (typeof evntx.origin    != 'undefined') params['transformOrigin'] = evntx.origin       

  else params['transformOrigin'] = '50% 50%'

  if (typeof evntx.xmove     != 'undefined') params['x'              ] = '+=' + evntx.xmove 
  if (typeof evntx.ymove     != 'undefined') params['y'              ] = '+=' + evntx.ymove 

  if (typeof evntx.scale     != 'undefined') params['scale'          ] = '*=' + evntx.scale 
  if (typeof evntx.xscale    != 'undefined') params['scaleX'         ] = '*=' + evntx.xscale
  if (typeof evntx.yscale    != 'undefined') params['scaleY'         ] = '*=' + evntx.yscale

  if (typeof evntx.autoAlpha != 'undefined') params['autoAlpha'      ] = evntx.autoAlpha  
  if (typeof evntx.rotate    != 'undefined') params['rotation'       ] = '+=' + evntx.rotate

  return params
}

/*———————————————————————————————————————— log(arg)
    */

function log(arg){
  console.log(arg)
}

/*———————————————————————————————————————— errLog(arg)
    */

function errLog(arg, obj){

  if (typeof obj != 'undefined'){
    var id   = convertEntities(obj.dataset.name)
    if (id.length > 50) id = id.slice(0, -52)

    arg += ' in ' + svgName(obj) + '.ai' + ' › ' + id
  }

  debugMessages.push(arg)
  log('⚠️  '+arg)
}

/*———————————————————————————————————————— not_number(x)
    */

function not_number(x) {
  return parseFloat(x) != x
}

/*———————————————————————————————————————— convertEntities(str)

  apparently, &amp is automatically converted to just & */

function convertEntities(str){


//log('convertEntities: ' + str)

  var needed = str.indexOf('&') > 0
  if (!needed) return str

  else return htmlDecode(str)
}

/*———————————————————————————————————————— htmlDecode(input)
    */

function htmlDecode(input) {
  var doc = new DOMParser().parseFromString(input, "text/html");
  return doc.documentElement.textContent;
}

/*———————————————————————————————————————— convertEntitiesOld(in)

    id="toggle_x2F_name15_x2F_-y10_x2F_x_x2B_30_x2F_t100" */

function convertEntitiesOld(str){

  var parts = str.split('_')
  
  for (var x=1; x<parts.length; x+=1){
    if (Object.keys(entity_conversion_old).includes(parts[x]))
      parts[x] = entity_conversion_old[parts[x]]
  }

  str2= parts.join('')

  // log('—————————————————————————————— 😈 conversion from '+str+' to '+str2)
  return str2

}

/*———————————————————————————————————————— decodeEntities(arg)

    used for args passed to func trigger flag

    converts illustrator style entites to html entites
    _x22_ to &#x22; to get normal entity

    then converts those to regular text
    &#x22; to ! */

/* breaks for four-character entities, like . and - */

function decodeEntities(arg){
  if (typeof arg == 'undefined') return ''

  const regex = /_x([0-9A-Z]{2})_/g

  var html = arg.replace(regex, function($1){
    var x = $1.toLowerCase() 
        x = x.replaceAll('_x','&#x')
        return x.replaceAll('_', ';')
  })

  html = convertEntitiesOld(html)
  html = html.replaceAll('_', ' ')

  var tmpObject = document.createElement('textarea')

  tmpObject.innerHTML = html
  var val = tmpObject.value
  tmpObject.remove()

  return val
}

/*———————————————————————————————————————— minusPeriod(clip_path)

    fix illustrator bug with clipping masks with a - in the name

    In the SVG code, the path definition looks like this:
        <rect id="clipping-path" ... >

    but the reference to it looks like this:
        <use xlink:href="#clipping_x002D_path" ... >

    https://illustrator.uservoice.com/forums/601447-illustrator-desktop-bugs/suggestions/45420952-clipping-mask-broken-in-svg-export-if-name-contain */

function minusPeriod(clip_path, pathId){
  // fix illustrator bug
  // reported at: https://illustrator.uservoice.com/forums/601447-illustrator-desktop-bugs/suggestions/45420952-clipping-mask-broken-in-svg-export-if-name-contain
  
//  try{
//    alert(pathId+': '+typeof clip_path +':'+ typeof clip_path.innerHTML) // object : string
//  }
//  catch(msg){
//    alert(pathId+': '+'error')
//    return
//  }

  var first_child = clip_path.innerHTML
  var correct_id  = first_child.split('"')[1].slice(1)
  
  if (correct_id.indexOf('_x002D_') > 0 || correct_id.indexOf('_x002E_') > 0){
    var wrong_id = correct_id.replace('_x002D_', '-').replace('_x002E_', '.');
    var path = document.getElementById(wrong_id);
    if (path != null)
      path.id  = correct_id;
  }
}


/* <use xlink:href="#delay_x2F_time1_x2F_3_x2F__x3C__x2F__x002D_y150" style="overflow:visible;"></use> */

/*———————————————————————————————————————— getElementsByRegex(pattern)
    */


// https://stackoverflow.com/a/1938465
function getElementsByRegex(pattern){
   var arrElements = []   // to accumulate matching elements
   var re = new RegExp(pattern)   // the regex to match with

   function findRecursively(aNode) { // recursive function to traverse DOM
      if (!aNode) 
          return
      if (aNode.id !== undefined && aNode.id.search(re) != -1)
          arrElements.push(aNode)  // FOUND ONE!
      for (var idx in aNode.childNodes) // search children...
          findRecursively(aNode.childNodes[idx])
   }

   findRecursively(document) // initiate recursive matching
   return arrElements // return matching elements
}

/*———————————————————————————————————————— createTline(namex, evntx, params)
    */

function createTline(namex, evntx, params){

  var funcName = namex + '_timeline'
  var tline    = window[funcName]

  if (typeof tline == 'undefined'){
    window[funcName] = new gsap.timeline({paused:true})
    var tline = window[funcName]
    tline.pause(0.1) // prevent flash from clipping mask — reset at end of setup

//  log(namex+'——————————————————————-: '+evntx.delay)
    tline[evntx.fromto](evntx.obj, params, evntx.delay)

  env_allTlines[env_allTlines.length] = funcName
  }
}

/*———————————————————————————————————————— svgName(obj)
    */

function svgName(obj){
  while (obj.tagName != 'svg')
    var obj = obj.parentElement

  var objId = obj.id
  if (objId.substr(0,4) == 'svg_') objId = (objId.substr(4))

  return convertEntities(objId)
}

/*———————————————————————————————————————— containsTransform(trigger) COMMENTED OUT
    */

/* function containsTransform(trigger){

  if ( typeof trigger.xmove     == 'undefined' &&
       typeof trigger.ymove     == 'undefined' &&
       typeof trigger.rotate    == 'undefined' &&
       typeof trigger.scale     == 'undefined' &&
       typeof trigger.xscale    == 'undefined' &&
       typeof trigger.yscale    == 'undefined'  ) return false

  return true
} */

/*———————————————————————————————————————— getParentG()

    accepts object <g... tag in an SVG
    returns the parent <g... tag

    used to move the style="clip-path... to the parent tag,
    in order to avoid a problem where the clip path was animated
    along with its contents */

function getParentG(obj){
  // create array of parent objects
  // max length 3 (à voir)
  // go up array until find G or get to end of array
  // return G or null
  var parts = []

  if (typeof obj.parentElement != 'undefined'){
    parts.push(obj.parentElement)
    if (typeof obj.parentElement.parentElement != 'undefined'){
      parts.push(obj.parentElement.parentElement)
      if (typeof obj.parentElement.parentElement.parentElement != 'undefined'){
        parts.push(obj.parentElement.parentElement.parentElement)
      }
    }
  }
  for (var x=0; x<parts.length; x++)
    if (parts[x].tagName == 'g') return parts[x]

  return null
}

/*———————————————————————————————————————— dumpKeys(obj)
    */

function dumpKeys(obj){
  var str = ''

  for (var i in obj){
    try{
//    str += '\n'+i+': '+obj[i].typename
      str += '\n'+i+': '+obj[i].typename+', '+obj[i]
    }
    catch(e){
      str += '\n'+i+': error'
    }
  }
  alert(str)
}

/*———————————————————————————————————————— setVisible(anim)

    will set display:none or display:block depending on
    whether it should be initially hidden

    objects are set to 'none' when arriving here

    see google spreadsheet for logic
    https://docs.google.com/spreadsheets/d/1wq1By47vzXZzdvb6JZS3AqR8mhwZ3c2ZSoF0eR1m25Y/edit#gid=601106820   */

function setVisible(anim){
  if (typeof anim.opacity == 'undefined'        ) return true // if no change in transparency
  if (anim.opacity  > 0                         ) return true // if starts visible
  if (anim.autoAlpha > 0 && anim.fromto == 'from') return true // if starts visible

  return false
}

/*———————————————————————————————————————— isHorizontal(obj)

    https://stackoverflow.com/questions/18147915/get-width-height-of-svg-element

    returns true if the width of the object is
    greater than the height of the object */

function isHorizontal(obj){
  var rect = obj.getBoundingClientRect()
  var width = rect.width
  var height = rect.height + .001

  if (width > height) return true
  else return false
}

/*———————————————————————————————————————— playTimeline(tline)

    used to delay playing timelane slightly to fix a problem
    where content inside clipping masks flashed before being
    positioned correctly. */

function playTimeline(tline, pos){
   if (typeof pos == 'undefined') pos = 0
   tline.pause(pos)                            // set to .01 so the next time we don't restart by mistake
   setTimeout(playTimelineDelayed, 5, tline)   // set to 5ms so the playhead has time to advance
}

function playTimelineDelayed(tline){ tline.play() }

/*———————————————————————————————————————— transformedRect(rect, trans)

   accepts an svg element and returns a rect
   taking into account the transformation
   used to correct scroll triggers */

function transformedRect(obj){

  var objBox = obj.getBBox()                       // array x, y, width, height

  var mat = obj.getAttribute('transform')          // string or null

  if (mat == null) return objBox                   // no transform
  if (mat.slice(0, 6) != 'matrix') return objBox   // transform is not matrix

  matVals = mat.slice(7,-1).split(' ')             // remove all but values, split at spaces
  if (matVals.length != 6) return objBox           // not 6 values

  x = objBox['x']
  y = objBox['y']
  w = objBox['width']
  h = objBox['height']

  var cornNew = {}

  cornNew['tl'] = applyTransformation([  x, y  ], matVals)
  cornNew['tr'] = applyTransformation([x+w, y  ], matVals)
  cornNew['bl'] = applyTransformation([  x, y+h], matVals)
  cornNew['br'] = applyTransformation([x+w, y+h], matVals)

  var minX = Math.min(cornNew['tl'][0], cornNew['tr'][0], cornNew['bl'][0], cornNew['br'][0])
  var maxX = Math.max(cornNew['tl'][0], cornNew['tr'][0], cornNew['bl'][0], cornNew['br'][0])

  var minY = Math.min(cornNew['tl'][1], cornNew['tr'][1], cornNew['bl'][1], cornNew['br'][1])
  var maxY = Math.max(cornNew['tl'][1], cornNew['tr'][1], cornNew['bl'][1], cornNew['br'][1])

  w = Math.abs(maxX - minX)
  h = Math.abs(maxY - minY)

  return {'x': minX, 'y': minY, 'width':w, 'height':h}

}

/*———————————————————————————————————————— applyTransformation(corner, matVals)

    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform

    applies the calculation in the gray box
    called by transformedRect() */

function applyTransformation(corner, matVals){
  let [a, b, c, d, e, f] = matVals

  var oldX = corner[0]
  var oldY = corner[1]

  newX = a * oldX + c * oldY + 1*e
  newY = b * oldX + d * oldY + 1*f

  return [newX, newY]
}

/*———————————————————————————————————————— alertRect(obj, rect)

    gives an alert with rect size
    used by applyTransformation */

function alertRect(obj, rect){
  name = convertEntitiesOld(obj.id)
  x = Math.round( rect['x'])
  y = Math.round( rect['y'])
  w = Math.round( rect['width'])
  h = Math.round( rect['height'])
  alert(name + ' is '+w+'x'+h+'px, left '+x+' & top '+y)
}


//:::::::::::::::::::::::::::::::::::::::: fin


