
//———————————————————————————————————————— animations-1.0.2.js

/*———————————————————————————————————————— notes

    _x2B_ plus sign    link to next anim
    _x3E_ greaterthan  rotate clockwise
    _x3C_ lessthan     rotate counter clkws

    _x3D_ equals       deprecated

for tying in to javascript, can I add something?

user|Submit
I need to add listener, AND CSS for cursor:pointer

for cursor: add a flag |v for visible hand cursor TO ACTION
for javascript: add flag |function TO ACTION

user|submit|v|func = ???

  triggers:
    scroll
    user
    delay

  actions:
    click
    msover
    msout
    msovout
    toggle
    anim (for scroll & delay) 

https://docs.google.com/spreadsheets/d/1_INTDgE9-XKC63PSlRClXJDoC7afz6V7FFB3hiN7bhE/edit#gid=1328156795
https://docs.google.com/document/d/1nImxZ6IgWFqDx6cOtrN-s9yZu564oMAxRxPwx_9lXSs/edit
https://www.freecodecamp.org/news/how-javascript-implements-oop/

// utf-8 entities
☀  9728  2600     BLACK SUN WITH RAYSTry it
☗  9751  2617     BLACK SHOGI PIECETry it
☤  9764  2624     CADUCEUSTry it
☻  9787  263B     BLACK SMILING FACETry it
♚  9818  265A     BLACK CHESS KINGTry it
♛  9819  265B     BLACK CHESS QUEENTry it
♜  9820  265C     BLACK CHESS ROOKTry it
♝  9821  265D     BLACK CHESS BISHOPTry it
♞  9822  265E     BLACK CHESS KNIGHTTry it
♟  9823  265F     BLACK CHESS PAWNTry it
♠  9824  2660  &spades;  BLACK SPADE SUITTry it
♣  9827  2663  &clubs;  BLACK CLUB SUITTry it
♥  9829  2665  &hearts;  BLACK HEART SUITTry it
♦  9830  2666  &diams;  BLACK DIAMOND SUITTry it
♻  9851  267B     BLACK UNIVERSAL RECYCLING SYMBOLTry it
♼  9852  267C     RECYCLED PAPER SYMBOLTry it
⚈  9864  2688     BLACK CIRCLE WITH WHITE DOT RIGHTTry it
⚉  9865  2689     BLACK CIRCLE WITH TWO WHITE DOTSTry it
⛋  9931  26CB     WHITE DIAMOND IN SQUARETry it
⛒  9938  26D2     CIRCLED CROSSING LANESTry it

————————————————————————————————————————*/
//———————————————————————————————————————— start timer

const d1 = new Date();
let start_time = d1.getTime();
console.log("animations-1.0.1.js");

//———————————————————————————————————————— separator, types of triggers and actions

const  separator = '_x2F_'; // regular slash
const   triggers = [  'user',   'delay', 'scroll'                             ];
const    actions = [ 'click',  'msover', 'msout', 'msovout', 'toggle', 'anim' ];

//———————————————————————————————————————— conversion dictionaries

const flag_value_to_key = {

  // name & kind are given

  // trigger flags
  'func'  : 'func'       , // no value
  'a'     : 'cursor'     , // no value
  'h'     : 'cursor'     , // no value
  't'     : 'cursor'     , // no value
  'n'     : 'blank'      , // no value

  // GSAP-related flags
  'in'    : 'ease'       , // no value
  'out'   : 'ease'       , // no value
  'inout' : 'ease'       , // no value
  'noease': 'ease'       , // no value

  'x'     : 'xmove'      , // value follows
  'y'     : 'ymove'      , // value follows
  'f'     : 'fixed'      , // value follows
  '_x3C_' : 'rotate'     , // value follows
  '_x3E_' : 'rotate'     , // value follows
  '_x25_' : 'scale'      , // value follows
  'x_x25_': 'xscale'     , // value follows
  'y_x25_': 'yscale'     , // value follows
  'o'     : 'opacity'    , // value follows

  '_x2B_' : 'handoff'      // value follows
}

const key_length = { 

  // so we can get value from end of flag
  // # of characters, value follows

  'cursor'     : 0,
  'func'       : 0,
  'blank'      : 0,
  'handoff'    : 5,
  'ease'       : 0,
  'xmove'      : 1,
  'ymove'      : 1,
  'fixed'      : 1,
  'rotate'     : 5,
  'scale'      : 5,
  'xscale'     : 6,
  'yscale'     : 6,
  'opacity'    : 1

}

const eases = {
  'in'    : Power1.easeIn,
  'out'   : Power1.easeOut,
  'inout' : Power1.easeInOut,
  'noease': "none" 
}

const cursors = {
  'a'           : 'default',
  'h'           : 'pointer',
  't'           : 'text',
  'default_link': 'pointer'
}

const opacity_opposites = {
  0 : 100,
  100 : 0 
}

const trigger_flag_value_to_key_value = {
  'a'   : 'a',
  'h'   : 'h',
  't'   : 't',
  'func': true,
  'n'   : true
}


//———————————————————————————————————————— defaults

//  'link_cursor': 'h',                // hand cursor (links)

const trigger_defaults = {

  'trigger'    : null,
  't_kind'     : null,
  'cursor'     : null,
  'func'       : false,
  'args'       : null,
  'link'       : false,
  'blank'      : false,

}

const action_defaults = {

  'action'     : null, 
  'a_kind'     : null,
  'delay'      : 0,
  'handoff'    : null,
  'handwait'   : null,
  'duration'   : 0.5,
  'ease'       : null,
  'xmove'      : null,
  'ymove'      : null,
  'fixed'      : null,
  'rotate'     : null,
  'scale'      : null,
  'xscale'     : null,
  'yscale'     : null,
  'opacity'    : null,
  'current'    : null
}



//:::::::::::::::::::::::::::::::::::::::: DATA STRUCTURE

//———————————————————————————————————————— class Animation

// https://www.w3schools.com/js/js_classes.asp

var animations = {};   // list of Animation's
var functions  = [];   // list of user functions called by buttons

class Animation{

  constructor( name, trigger, t_kind, cursor, func, args, link, blank, action,
               a_kind, delay, handoff, handwait, duration, ease, xmove, ymove,
               fixed, rotate, scale, xscale, yscale, opacity, current ){

    this.name       = name;         // 20-character string

    // trigger-specified
    this.trigger    = trigger;      // object reference
    this.t_kind     = t_kind;       // string · kind of trigger                  scroll, user, delay
    this.cursor     = cursor;       // string · cursor on mouseover              a, h, t (arrow, hand, text)
    this.func       = func;         // boolean · calls function of same name     onclick only 
    this.args       = args;         // array · args passed to function           all flags following name
    this.link       = link;         // boolean · is an SVG link                  programmatically
    this.blank      = blank;        // boolean · link target is _blank           n

    // action-specified
    this.action     = action;       // object reference
    this.a_kind     = a_kind;       // string · kind of action                   click, msover, mosout, msovout, toggle, visible
    this.delay      = delay;        // number · seconds before animation starts  33 (2nd number)
    this.handoff    = handoff;      // string · following animation
    this.handwait   = handwait;     // number · seconds before calling following animation

    // GSAP-related
    this.duration   = duration;     // number · duration in seconds              34.5 (1st number)
    this.ease       = ease;         // animation ease                            in, out, inout, noease
    this.xmove      = xmove;        // x movement                                x-30
    this.ymove      = ymove;        // y movement                                y25
    this.fixed      = fixed;        // fixed point                               0f0 to 100f100
    this.rotate     = rotate;       // number · rotation                         >20 or <45.5
    this.scale      = scale;        // number · percentage to scale              %150
    this.xscale     = xscale;       // number · percentage to scale x            x%20
    this.yscale     = yscale;       // number · percentage to scale y            y%30
    this.opacity    = opacity;      // number · percentage opacity               o30
    this.current    = current;      // number · current visibility/opacity       programmatically
  }

  add_trigger(obj, kind, flags){

    // set defaults

    Object.keys(trigger_defaults).forEach(
      key => { this[key] = trigger_defaults[key]; }
    );

    // initialize

    this.trigger    = obj;
    this.t_kind     = kind;

    // loop through flags (kind|name|parameters...)

    for(var x=2; x<flags.length; x++){

      // determine flag key from value
      // entity conversion not necessary for triggers

      var val = flags[x];
      var key = flag_value_to_key[val];

      // if not function, set flag

      if (key != 'func')
        this[key] = trigger_flag_value_to_key_value[val];

      // if function, add arguments to "args"
      else {
        this.func = true;
        this.args = [];
        for (var y=x+1; y<flags.length; y++)
          this.args.push(flags[y]);

        x = 1000; // get out of loop — no other flags can follow func
      }
      
    // set link & parent target

    this.link = obj.parentNode.hasAttribute('xlink:href'); // true false
    if (this.link && this.blank)
      this.trigger.parentNode.setAttribute("target", "_blank");


    }

    // log trigger add results

//  console.log('——— trigger '+this.name+' — '+
//    ' cursor: '+this.cursor+
//    ' func: '+this.func+
//    ' args: '+this.args+
//    ' link: '+this.link+
//    ' blank: '+this.blank);


  }

  add_action(obj, kind, flags){


    // set defaults

    Object.keys(action_defaults).forEach(key =>
      { this[key] = action_defaults[key]; }
    );

    // initialize

    this.action   = obj;
    this.a_kind   = kind;

    // loop through flags (kind|name|parameters...)

    var is_duration = true;

    for(var x=2; x<flags.length; x++){

      // get key
      var key  = null;
      var flag = flags[x];

      [key, is_duration] = this.get_key(flag, is_duration);

      // assign value to flag
      this[key] = this.get_val(key, flag);
//    console.log(this.name+': '+key+' = '+this[key]);

    }

    // special cases (so absence of flags behaves as expected)
    if (this.xmove   == null &&
        this.ymove   == null &&
        this.rotate  == null &&
        this.scale   == null &&
        this.xscale  == null &&
        this.yscale  == null &&
        this.opacity == null){

      if (this.a_kind=='msover' || this.a_kind=='anim' || this.a_kind=='toggle' || this.a_kind=='msovout') this.opacity = 100;
      if (this.a_kind=='msout'                                                    ) this.opacity = 0;

    }

  }

  delete_if_no_action(){
  
    if (this.a_kind == undefined && !this.func && !this.link){
      console.log('trigger '+this.name+' deleted (no action, link or function)');
      delete animations[this.name];
      return true;
    }
    return false;
  }

  turn_on_if_on(){
    if (!this.action) return true;
  
  /* will check for unspecified opacities and set them accoringly.

  it will not affect specified opacities */   


    var make_visible = false;

    if (this.a_kind == 'msout') make_visible = true;
    if (this.opacity != null)   make_visible = false;
    if (this.opacity == 0)      make_visible = true;

    if (!make_visible) return true; 
    
    this.action.style.opacity = 1;
    this.action.style.display = 'block';
    set_clickable(this.action, true);

  }

set_cursor(){
  if (this.cursor != null){
    this.trigger.style.cursor = cursors[this.cursor];
  }
  else{
    var is_hand = false;

    if (this.trigger.link   ) is_hand = true;
    if (this.trigger.func   ) is_hand = true;

    if (this.a_kind == 'click' ) is_hand = true;
    if (this.a_kind == 'toggle') is_hand = true;

    if (is_hand){
      this.trigger.style.cursor = cursors['default_link'];
    }
  }
}

  dump_flags(){
    Object.keys(this).forEach(key => {
      console.log(key+', '+typeof(this[key])+': '+this[key]);
    });
    
    console.log('\n\n');
  }

  get_key(flag, is_duration){

  // is programmed specifically to optimize key finding
  // needs to be updated when flags are modified

    try {
      var first = flag.substr(0,1);

      // has to be rewritten when flags are modified
      // the point is to avoid a loop
      switch(first){
        case 'a':                            key = 'cursor' ; break;
        case 'h':                            key = 'cursor' ; break;
        case 'i':                            key = 'ease'   ; break;
        case 't':                            key = 'cursor' ; break;
        case 'f': if (flag=='func'         ) key = 'func'   ; else key = 'fixed'  ; break;
        case 'n': if (flag=='noease'       ) key = 'ease'   ; else key = 'blank'  ; break;
        case 'o': if (flag=='out'          ) key = 'ease'   ; else key = 'opacity'; break;
        case 'x': if (flag.substr(1,1)=='_') key = 'xscale' ; else key = 'xmove'  ; break;
        case 'y': if (flag.substr(1,1)=='_') key = 'yscale' ; else key = 'ymove'  ; break;
        case '_': key = flag_value_to_key[flag.substr(0,5)]; break;

      default:
        // presume it's a number
        if (is_duration){
          key = 'duration';
          is_duration = false;
        }
        else key = 'delay';

      }
      return [key, is_duration];
    }
    catch (error) {
      console.log('⚠️  unknown flag: '+this.name+'.'+flag +':'+flag.substr(0,5)+':');
      return [null, false];
    }


  }

  get_val(key, flag){
    var key_len = key_length[key];
    if (key_len == 0) return flag;
    else return flag.substr(key_len);
  }

  activate_function(){

    // https://stackoverflow.com/questions/359788/how-to-execute-a-javascript-function-when-i-have-its-name-as-a-string
    // https://www.geeksforgeeks.org/how-to-call-function-from-it-name-stored-in-a-string-using-javascript/

    if (!this.func) return true;

    // var args = this.args;

    // TODO need to check if function exists, or will throw error:
    functions[this.name] = window['func_'+this.name];

    clog('activating function '+this.name);
    this.trigger.addEventListener('click', functions[this.name].bind(null, 'fuckin-a')); 
  }


}


//:::::::::::::::::::::::::::::::::::::::: PROGRAM

//———————————————————————————————————————— register triggers

console.log('\n——— registering triggers ———');

triggers.forEach(kind => {
  var stem = "[id^='" + kind + separator + "']";
  var obj_array = Array.from(document.querySelectorAll(stem));

  // loop through adding triggers
  for(var x=0; x<obj_array.length; x++){
    var obj = obj_array[x];
    var flags = obj.id.split(separator);

    // doesn't have at least trigger and name
    if (flags.length<2) continue; 

    //  kind = flags[0];
    var name = flags[1];
    animations[name] = new Animation(name);
    animations[name].add_trigger(obj, kind, flags);
  }

  // log results
//if (obj_array.length == 0)
//  console.log('—› no '+kind+' triggers');
//else
//  console.log(obj_array.length+' '+ kind+' triggers');


});

//———————————————————————————————————————— register actions

console.log('\n——— registering actions ———');

actions.forEach(kind => {
  var stem = "[id^='" + kind + separator + "']";
  var obj_array = Array.from(document.querySelectorAll(stem));

  // loop through adding actions
  for(var x=0; x<obj_array.length; x++){
    var obj = obj_array[x];
    var flags = obj.id.split(separator);

    //  kind = flags[0];
    var name = flags[1];

    if (Object.keys(animations).includes(name))
      animations[name].add_action(obj, kind, flags)
    else
      console.log('—› '+kind+' action '+name+' has no trigger (not registered)');

  }

  // log results
  if (obj_array.length == 0) console.log('—› no '+kind+' actions');
                        else console.log(obj_array.length+' '+ kind+' actions registered');

});

//———————————————————————————————————————— turn on "default on" elements, set cursors, and activate functions  · deactivated

console.log('\n——— turning on "default on" elements & settings cursors ———');

Object.keys(animations).forEach(name => {
  animations[name].turn_on_if_on();
  animations[name].set_cursor();
  animations[name].activate_function();
})

//———————————————————————————————————————— delete unused triggers · DISABLED

//  console.log('\n——— deleting actionless animations ———');

//  Object.keys(animations).forEach(name =>
//    animations[name].delete_if_no_action()
//  )

//———————————————————————————————————————— enable actions

console.log('\n——— activating animations ———');

Object.keys(animations).forEach(name => {

  if (animations[name].t_kind=='user') // 2ms
    activate_user(animations[name]);  

  if (animations[name].t_kind=='delay') // 2ms
    activate_delay(animations[name]);

  if (animations[name].t_kind=='scroll') // 11ms
    activate_scroll(animations[name]);

})

//———————————————————————————————————————— debugging & end timer

const d2 = new Date();
let end_time = d2.getTime();

clog('\n———————————————————— finished in '+(end_time-start_time)+'ms\n\n');

//animations['ha'].dump_flags();


//:::::::::::::::::::::::::::::::::::::::: BUILD EACH ACTION

//———————————————————————————————————————— activate_user(animation)

function activate_user(animation){

  switch (animation.a_kind) {
  case undefined: break; // if it's just a link or func
  case 'click':
    user_click(animation);
    break;
  case 'msover':
    user_msover(animation);
    break;
  case 'msout':
    user_msout(animation);
    break;
  case 'msovout':
    user_msovout(animation);
    break;
  case 'toggle':
    user_toggle(animation);
    break;

  default:
    clog('⚠️ unimplemented user a_kind:'+animation.a_kind+'in animation '+animation.name);
  }

  clog('user animations activated');
}

//———————————————————————————————————————— activate_delay(animation)

function activate_delay(animation){

  switch (animation.a_kind) {
  case 'anim':
    delay_anim(animation);
    break;

  default:
    clog('⚠️ unknown delay a_kind:'+a_kind);
  }

  clog('delay animations activated');
}

//———————————————————————————————————————— activate_scroll(animation)

function activate_scroll(animation){

  switch (animation.a_kind) {
  case 'anim':
    scroll_anim(animation);
    break;

  default:
    console.log('⚠️ unknown scroll a_kind:'+a_kind);
  }

  clog('scroll animations activated');
}


//:::::::::::::::::::::::::::::::::::::::: ACTIONS

//———————————————————————————————————————— delay_anim(animation)

function delay_anim(animation){

  delay  = animation.delay * 1000;
  params = gsap_params(animation);
  setTimeout(create_anim.bind(null, animation, params), delay);

}


//———————————————————————————————————————— user_msover(animation)

function user_msover(animation){

  params = gsap_params(animation);

  animation.trigger.addEventListener('mouseover', create_anim.bind(null, animation, params), false);

}

//———————————————————————————————————————— user_msout(animation)

function user_msout(animation){

  params = gsap_params(animation);
  animation.trigger.addEventListener('mouseout', create_anim.bind(null, animation, params), false);

}

//———————————————————————————————————————— user_click(animation)

// TODO clicking twice continues movement instead of doing nothing

function user_click(animation){

  params = gsap_params(animation);

  if (animation.opacity == null)
    params['opacity'] = 1;

  animation.trigger.addEventListener('click', create_anim.bind(null, animation, params), false);

}

//———————————————————————————————————————— user_msovout(animation)

// rotation is not cumulative (rotating to 90° twice just turns to 90°)

function user_msovout(animation){

  params1 = gsap_params(animation);
  params2 = anti_params(animation);

  animation.trigger.addEventListener('mouseover',  create_anim.bind(null, animation, params1), false);
  animation.trigger.addEventListener('mouseout',  reverse_anim.bind(null, animation         ), false);

}

//———————————————————————————————————————— user_toggle(animation)

function user_toggle(animation){

  params = gsap_params(animation);
  animation.trigger.addEventListener('click', create_toggle_anim.bind(null, animation, params), false);

}


//———————————————————————————————————————— scroll_anim(animation)

function scroll_anim(animation){

  var obj = animation.trigger;

  var box = obj.getBBox();      // get bounding box of trigger
  var t = box['y'];             // top
  var b = t + box['height'];    // bottom
  var params = gsap_params(animation);

  window.addEventListener('scroll', create_scroll_anim.bind(null, animation, t, b, params)); 
}


//:::::::::::::::::::::::::::::::::::::::: ACTION-RELATED

//———————————————————————————————————————— create_scroll_anim(animation, trig_top, trig_bot)

// https://stackoverflow.com/questions/4096863/how-to-get-and-set-the-current-web-page-scroll-position

/*    special cases:
 
      • top is visible to start with
      • action opacity default is visible to start with */

// called every time a scroll action

function create_scroll_anim(animation, trig_top, trig_bot, params){

  var page_top     = document.documentElement.scrollTop || document.body.scrollTop;
  var pixel_height = window.innerHeight;
  var page_bot     = page_top + pixel_height;

  var rem_top = page_top / illustrator_pixel;
  var rem_bot = page_bot / illustrator_pixel;

  var obj      = animation.action;
  var funcName = animation.name + '_timeline';
  var tline    = window[funcName];

// activated if top of trigger bar is not > bot of page
//          and bot of trigger bar is not < top of page

  if (trig_top < rem_bot && trig_bot > rem_top){
    if (typeof tline != "undefined"){
      if (tline.reversed()) tline.play();       //  if reversed play it
    }
    else{
      //  doesn't exist: create & play it
      window[funcName] = new gsap.timeline({paused:true});
      var tline = window[funcName];
      tline.to(obj, params);
      tline.play();
    }
  }

  // trigger is deactivated
  else{
    if (typeof tline == "undefined") return true;                    //  doesn't exist: do nothing
    if (!tline.isActive() && !tline.reversed()) tline.reverse();     //  paused not reversed (at end): reverse it
    else if (tline.isActive() && tline.reversed()) tline.reverse();  //  playing not reversed: reverse it */
    return true;
  }

}

//———————————————————————————————————————— create_toggle_anim(obj, params)

// only called when clicked

function create_toggle_anim(animation, params){

  var obj      = animation.action;
  var funcName = animation.name + '_timeline';
  var tline    = window[funcName];

  // create & play if doesn't exist
  if (typeof tline == "undefined"){

    window[funcName] = new gsap.timeline({paused:true});
    var tline = window[funcName];
    tline.to(obj, params);
    tline.play();

  } else {

    if (tline.reversed()) tline.play();
    else tline.reverse();

  }
}


//:::::::::::::::::::::::::::::::::::::::: GENERIC

//———————————————————————————————————————— reverse_anim(obj, params)

function reverse_anim(animation){
  var funcName = animation.name + '_timeline';
  window[funcName].reverse();
}

//———————————————————————————————————————— create_anim(obj, params)

function create_anim(animation, params){

  obj = animation.action;

  var funcName = animation.name + '_timeline';

  // create if it doesn't exist
  if (typeof window[funcName] == "undefined"){
    window[funcName] = new gsap.timeline({paused:true});
    window[funcName].to(obj, params);
  }

  // play if it's not playing
  if (!window[funcName].isActive())
//if (!window[funcName].isActive() && !window[funcName].reversed()) // apparently it's still reversed after the end
    window[funcName].play();

  // make unclickable to avoid layering conflicts
  if (params.opacity==0) set_clickable(obj, false);
                    else set_clickable(obj, true );
}

//———————————————————————————————————————— opposite_visibility(animation, duration, ease)

function opposite_visibility(animation, duration, ease){
  alert('toggle has not been programmed yet');
  change_visibility(animation, duration, animation.current, ease);
}

//———————————————————————————————————————— change_visibility(duration, opacity, ease)

// need to add display:none or set cursor painted to off

function change_visibility(animation, duration, opacity_prev, ease){

  name        = animation.name;
  action      = animation.action;
  opacity_new = opacity_opposites[opacity_prev];

  // gsap
  opacity     = opacity_new / 100;
  ease        = eases[ease];

//console.log('change_visibility(): '+name+' running: duration='+duration+', opacity='+opacity+', ease '+animation.ease);

  gsap.to(action, { duration:duration, autoAlpha:opacity, ease:ease });

  animation.current = opacity_new;
  if (opacity == 0) set_clickable(animation.action, true);
               else set_clickable(animation.action, false);
}

//———————————————————————————————————————— set_clickable(obj, clickable)

function set_clickable(obj, clickable){
  if (clickable)
    obj.style.pointerEvents = 'visiblePainted';
  else
    obj.style.pointerEvents = 'none';
}

//———————————————————————————————————————— convert_transform(fixed)

function convert_transform(fixed){
  if (fixed == null) return "50% 50%";

  var parts = fixed.split(',');
  result = parts.join('% ') + '%';
  return result;
}

//———————————————————————————————————————— gsap_params(animation)

function gsap_params(animation){

  var params = {};

  params['duration'       ] = animation.duration;
  params['transformOrigin'] = convert_transform(animation. fixed);

  if (animation.ease    == null) params['ease'     ] = Power1.easeInOut      ;
                            else params['ease'     ] = eases[animation.ease] ;

  if (animation.xmove   != null) params['x'        ] = '+=' + animation.xmove;
  if (animation.ymove   != null) params['y'        ] = '+=' + animation.ymove;

  if (animation.scale   != null) params['scale'    ] = animation.scale   / 100;
  if (animation.xscale  != null) params['scaleX'   ] = animation.xscale  / 100;
  if (animation.yscale  != null) params['scaleY'   ] = animation.yscale  / 100;

  if (animation.opacity != null) params['autoAlpha'] = animation.opacity / 100;
  if (animation.rotate  != null) params['rotation' ] = animation.rotate;

  return params;
}

//———————————————————————————————————————— anti_params(animation)

function anti_params(animation){

  var params = {};

  params['duration'       ] = animation.duration;
  params['transformOrigin'] = convert_transform(animation. fixed);

  if (animation.ease    == null) params['ease'     ] = Power1.easeInOut      ;
                            else params['ease'     ] = eases[animation.ease] ;

  if (animation.xmove   != null) params['x'        ] = '-=' + animation.xmove;
  if (animation.ymove   != null) params['y'        ] = '-=' + animation.ymove;

  if (animation.scale   != null) params['scale'    ] = 100 / animation.scale ;
  if (animation.xscale  != null) params['scaleX'   ] = 100 / animation.xscale;
  if (animation.yscale  != null) params['scaleY'   ] = 100 / animation.yscale;

  if (animation.opacity != null) params['autoAlpha'] = 1 - (animation.opacity/100);
  if (animation.rotate  != null) params['rotation' ] = 0;

  return params;
}

//———————————————————————————————————————— clog(arg)

function clog(arg){ console.log(arg) }


//———————————————————————————————————————— fin

