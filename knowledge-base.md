
*Updated 14 December, 2023 ·  dev.svija.love*

![Svija: SVG-based websites built in Adobe Illustrator][logo]

[logo]: http://files.svija.love/github/readme-logo.png "Svija: SVG-based websites built in Adobe Illustrator"

### Knowledge Base

### Localization

Reused translations are listed at the top of `admin.py`.

1. modifiy `models.py` etc. by adding `_( 'string' )`
   close the file
2. in `svija` directory do `django-admin makemessages --all`
3. `vi -O models.py locale/en/*/*.po`

if necessary copy to the opposite language

4. django-admin compilemessages

Then for each site:

5. ./manage.py makemigrations
6. ./manage.py migrate
7. service uwsgi restart

---
### Useful Links

- [good tips for webapps on iPhone](https://firt.dev/pwa-design-tips/#notch-and-iphone-x-support)
- [HN security suggestions](https://news.ycombinator.com/item?id=34098369)
- [HN accessibiility tips](https://news.ycombinator.com/item?id=33302783)
- [HN password requirements link](https://news.ycombinator.com/item?id=34098369)
- [ecommerce Django packages](https://djangopackages.org/grids/g/ecommerce/)
- [page progress bar](https://www.city-journal.org/html/dodging-trump-bullet-10850.html)
- [server hardening](https://news.ycombinator.com/item?id=37892028)

---
### Bug Fixes

<details><summary>PostgreSQL Failure</summary>

----------------------------------------
Link to fix: [github.com/docker-library](https://github.com/docker-library/postgres/issues/415)

The command that worked:
```
localedef -i en_US -f UTF-8 en_US.UTF-8
```
Based on suggestions by Akamai, I tried:
```
systemctl status postgresql@14-main.service
```
This returned:
```
× postgresql@14-main.service - PostgreSQL Cluster 14-main

     Loaded: loaded (/lib/systemd/system/postgresql@.service; enabled-runtime; vendor preset: enabled)
     Active: failed (Result: protocol) since Thu 2023-12-14 09:24:03 CET; 2min 26s ago
    Process: 1838 ExecStart=/usr/bin/pg_ctlcluster --skip-systemctl-redirect 14-main start
             (code=exited, status=1/FAILURE)
        CPU: 131ms

[1843] LOG:  invalid value for parameter "lc_messages": "en_US.UTF-8"
[1843] LOG:  invalid value for parameter "lc_monetary": "en_US.UTF-8"
[1843] LOG:  invalid value for parameter "lc_numeric": "en_US.UTF-8"
[1843] LOG:  invalid value for parameter "lc_time": "en_US.UTF-8"
[1843] FATAL:  configuration file "/etc/postgresql/14/main/postgresql.conf" contains errors

[1838]: pg_ctl: could not start server
[1838]: Examine the log output.

systemd[1]: postgresql@14-main.service: Can't open PID file /run/postgresql/14-main.pid (yet?) after start:
            Operation not permitted
systemd[1]: postgresql@14-main.service: Failed with result 'protocol'.
systemd[1]: Failed to start PostgreSQL Cluster 14-main.
```
This caused me to remember that I had seen the following errors when logging in to the server:
```
-bash: warning: setlocale: LC_ALL: cannot change locale (en_US.UTF-8)
-bash: warning: setlocale: LC_ALL: cannot change locale (en_US.UTF-8)
```
Linode also suggested:
```
sudo systemctl start postgresql@14-main.service
```
This returned:
```
Job for postgresql@14-main.service failed
because the service did not take the steps required by its unit configuration.
See "systemctl status postgresql@14-main.service"
and "journalctl -xeu postgresql@14-main.service" for details.
```
[Google Doc](https://docs.google.com/document/d/1aKoiILInZcUytrSPUqhSOInwsAKRstXX7VCc6kvuESI/edit#heading=h.f1enxlgdh64j) with my debugging steps.

</details>
<details><summary>page was not centered on load</summary>

---
#### page was not centered on load

> applies to pages that are wider than the browser window

The cause was the redirect from mobile to desktop on new windows. The mobile version loads, then reloads immediately while scrolled to 0,0.

Browser default behavior is to return to the same scrolling position as before when the page is reloaded.

**fix:** add `history.scrollRestoration = 'manual';` to the JS right before reloading the page.

</details>
<details><summary>page reloaded constantly</summary>

---
#### page reloaded constantly

> applies to pages on any site where both domain and subdomains are used

The cause was that Django was using cookie values associated with the parent domain (**screen_code** cookies were set for both base.svija.dev and svjia.dev).

**fix:** added a function to setCookie that deletes parent-domain cookies if appropriate.
</details>
<details><summary>'module' object is not callable</summary>

---
After refactoring the main page views, I got this error when I called CachedPageView.py from HomePageView.py

**fix:** include CachedPageView in __init__.py before calling it from HomePageView.py
</details>

---
### Etiquette

<details><summary>label guidelines</summary>

---
- colored labels designate category
- black labels are ?
- white labels are informational
</details>

---
### For the Future

<details><summary>funny license text about cat</summary>

---
This page is copyright 2005 by Graeme Cole. What are you allowed to do with it? Pfft. Anything within the realms of common sense, really. I don't want to prescribe rigidly what people can and can't do with it, so I've decided on a benchmark. It's this: you're allowed to do with this page anything you wouldn't mind me doing with your cat. So yes, you can photoshop it for comedy effect, you can copy bits of it for illustrative purposes and so on, but you can't steal it and pass it off as your own."

https://greem.co.uk/otherbits/jelly.html
</details>
<details><summary>share sheet icon</summary>

![share sheet site icon](https://user-images.githubusercontent.com/74959853/155168567-871d1a5d-7e4a-447c-9b28-1f33400f3b62.png)

</details>

---
### Technical Resources

<details><summary>safari font-size info</summary>

---
- https://stackoverflow.com/questions/72903407/svg-text-textlength-not-working-on-mobile-safari
- https://stackoverflow.com/questions/11768364/svg-scaling-issues-in-safari
- https://bugs.webkit.org/show_bug.cgi?id=56543

as of 230724:

- 16.5.2 (WebKit 18615.2.9.11.10) · Ventura
- 17.0 (WebKit 18616.1.22.1) · Safari Technology Preview · Release 174
- 17.0 (WebKit 19616.1.20.11.3) · Sonoma

</details>
<details><summary>embedded SVG's</summary>

---
https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Basic_Transformations

"In contrast to HTML, SVG allows you to embed other svg elements seamlessly. This way you can also create new coordinate systems by utilizing the viewBox, width and height of the inner svg element."
```
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="100" height="100">
  <svg width="100" height="100" viewBox="0 0 50 50">
    <rect width="50" height="50" />
  </svg>
</svg>
```

</details>
<details><summary>get/set scroll position</summary>

---
https://stackoverflow.com/questions/4096863/how-to-get-and-set-the-current-web-page-scroll-position

The currently accepted answer is incorrect - document.documentElement.scrollTop always returns 0 on Chrome. This is because WebKit uses body for keeping track of scrolling, whereas Firefox and IE use html.
</details>
<details><summary>ozake loading times</summary>

<img width="760" alt="next generation image formats" src="https://user-images.githubusercontent.com/74959853/155168435-2d547890-4591-406c-abec-5cbf391f273b.png">

</details>

---
### Code

<details><summary>Horizontal Scrolling Code </summary>

CSS
```
html, body {
  overflow-y:hidden;
  overflow-x:hidden; /* necessary so page doesn't scroll up slightly when scrolling sideways */
}

body{
  position:static;
}
```
body JS
```
var speed = 4
var scrollElement = document.body // put in head JS if problems

let passiveIfSupported = false;

try {
  window.addEventListener(
    "test",
    null,
    Object.defineProperty({}, "passive", {
      get() {
        passiveIfSupported = { passive: true };
      },
    })
  );
} catch (err) {}

scrollElement.addEventListener("wheel", (evt) => {
    evt.preventDefault();
    evt.stopPropagation();
    scrollElement.scrollLeft += evt.deltaY * speed;
},     passiveIfSupported);
```

**menu functions**

*requires **/func** for each link in menu:*
```
var arrets = [0, 1200, 2400, 4615, 6910, 9385, 11860]

//:::::::::::::::::::::::::::::::::::::::: called by Illustrator

function func_trig01(){ pageAvance(arguments.callee) }
function func_trig02(){ pageAvance(arguments.callee) }
function func_trig03(){ pageAvance(arguments.callee) }
function func_trig04(){ pageAvance(arguments.callee) }
function func_trig05(){ pageAvance(arguments.callee) }
function func_trig06(){ pageAvance(arguments.callee) }
function func_trig07(){ pageAvance(arguments.callee) }
function func_trig08(){ pageAvance(arguments.callee) }
function func_trig09(){ pageAvance(arguments.callee) }

//:::::::::::::::::::::::::::::::::::::::: program

//———————————————————————————————————————— correct for REM

for (var x=0; x<arrets.length; x++)
  arrets[x] = arrets[x] * aiPixel

//———————————————————————————————————————— called by func's

function pageAvance(func){

// https://www.geeksforgeeks.org/how-to-get-currently-running-function-name-using-javascript/

  var str = func.toString()
  var firstParen = str.indexOf('(') - 2

  stop = str.substr(firstParen, 2) * 1 - 1

  var totalTime = 0.5 // seconds total movement
  var interStep = 5 // ms between each movement
  var steps = totalTime*1000 / interStep

  var diff  = arrets[stop] - html.scrollLeft
  var step  = diff/steps

  for (var x=0; x<steps; x++){
    var last = false
    if (x == steps-1){
      last = true
      step = arrets[stop]
    }
    setTimeout(doStep, interStep*x + 1, step, last)
  }

}

//———————————————————————————————————————— scroll by increment

function doStep(step, last){
  if (last)
    html.scrollLeft = step
  else
    html.scrollLeft += step
}

//:::::::::::::::::::::::::::::::::::::::: fin

```
---
from other issue:

![capture 63](https://user-images.githubusercontent.com/74959853/224969343-77f01e59-6959-4858-b768-7a1ff703bf72.jpg)

the `overflow` css can be in the stylesheet for the page in question.

the `position` css *is* necessary (the Antretoise footer was not at the bottom of the page when I commented it out).

it can also be in the specific stylesheet for the page.

</details>

---
### Triage

<details><summary>list 1</summary>

---
- in addition to the normal web page being open and normally usable, there is the animation lab page that can be resized etc.
- need to decide which layout is best: wide & short, A4, or tall & thin
- the point is to be able to work on an animation and see its effects
- to make it easier, we need to be able to see where objects are at all times

panes:
- main programming workspace A- A+ buttons
- list of page scripts containing animation information from page (choose which one to modify)
- list of SVG's › (or one pane for each svg)
- list of user-created ID's in each SVG (2 pane for both)
- prefs : hightlighting style (background, outline, color, transparency, blinking)
- GSAP tips windows
- list of pagescripts anim info  with activate or no or checkboxes & edit button & new button & copy button
- made for a big monitor? Svija pages work at small sizes, there's no reason you couldn't reduce the svija
- should work on 1280x800 screen, even if the Svija page is tiny
- prefs : rows & colums of text (button "update")

- animation lab
- animation lab has list of non .st0 id's, choose your formatting to highlight
- javascript in main doc to launch anim lab
- choose key combination in admin
- anim lab w rem, responsive mais A+ A-

- how will animations be loaded / updated? choice of pagescripts
- list of page

</details>
<details><summary>list 2</summary>

---
- https://github.com/graphite-project/graphite-web/issues/668
- export GRAPHITE_ROOT=/opt/graphite
- PYTHONPATH=$GRAPHITE_ROOT/webapp django-admin.py dumpdata --settings=graphite.settings > sqllite_graphite_dump.json
- this should be easy to test.
- ./manage.py dumpdata > working.json
- took 1 second to run for Ozake, not a huge hit for once a day
- The basic theory is that backups are made when the page is loaded (depending on admin prefs), and downloaded every time the site is synced.
- We are going to benefit by rewriting the sync script to add a lite mode, only download or upload one file (would be nice to add dependencies in Links and Fonts at some point)
- not: models.py/admin.py:
- setting for interval between backups
- which backups to make: 1 day, 1 week, 1 month, 3 months, 1 year
- total number of backups to keep in stock (if smaller than prev. set to prev.)
- better just to configure the program, just have interval (manik could be weekly, staffeur monthly etc.)
- make a backup every day & 1/7 of the time don't replace – it make it older
- when it's a week old it , ¼ of the time don't replace, let it age
- when that one's a month old, ⅓ of the time don't replace, let it age
- when that one's three months old, ¼ of the time don't replace, let it age
- views.py:
- when page is loaded, check if a restore is called for (either in settings, restore on next visit, or because a restore db is present
- if there's a restore programmed, do it (adding comment in source code?)
- don't forget to run the postgresql script or try --natural to get rid of problem data
- if there's not a restore programmed, check dump interval
- if the most recent dump in /backups/ is not within the interval
- create a dump in/backups/
- delete databases that don't meet the "keep" requirement\*
- sync script:
- if sync up or sync down:
- do not touch anything in the /SYNC/backups folder
- sync the backups folder down
- also allow sync up only new for colleagues working on project
- also allow sync down by filename for colleagues working on project
- possible to not download backups (might take a long time if there are many)
- lite mode for working on one page
- restore:
- from admin page?
- upload a file, would be best
- restore on next visit from [filename]
- if you upload a fresh db in SYNC folder (not in sub folder)
- it will automatically replace the existing site (with backup made of existing)
- call files backup.svj
- views don't get called when cached… need to make sure that cache is emptied frequently enough to generate dumps
- backups are in root folder like SYNC, not in same folder as SYNC

</details>
<details><summary>list 3</summary>

---
- when page loads, in SVG, replace image reference:
- Links/home-hero-DSC_0020.jpg 
- with image width & resolution info
- treated/home-hero-DSC_0020-1680X20Q75D [day, second].jpg
- need parameters in admin/responsive for image quality & size
- page width = 1680
- pixel size = 20x (skip decimal, 20 = 2)
- quality = 0-100
- if Image is missing, go get original image and create correct size & quality
- models.py › responsive
- image resolution compared to SVG width (2x, etc.) 2-digit integer
- image quality (0-100)
- admin.py › responsive
- image resolution compared to SVG width (2x, etc.)
- image quality (0-100)
- views.py, when image is requested:
- check that referrer is site not hacker
- check uploaded image to get modified date
- check in /cached-images/ to see if appropriate image exists with correct date
- if it exists: use it
- else: treat the image then return the new image
- delete same image with wrong date
- need a way to clear image cache : page view URL with check for admin?
- need a way to exempt an image (just name it \_x ?) so that overriding is possible

</details>
<details><summary>list 4</summary>

---
———————————————————————————————————————— small improvements

- admin module with all prefixes and all-page list
- cross-site html in Svija? allow inclusing of html from other sites
- automatic conversion to flag in modules & pages (use entities in program)
- might want to remove 2-character limit for prefixes to allow things like "realisations". if I create multiple prefixes (realisations, fr) in a a single language/responsive, does it create an error for the default page? probably not because the site has a default prefix
- skip css by adding form fields: bottom align footer, give vertical positioning for second (after header) svg's
- rediriger une adresse telle que /contact à /en/contact selon la langue par défaut
- auto-create snippet if there's not one already
- need links between same pages in different languages
- /r shows most recent SVG with default settings
- french descriptions for all fieldsets
- hiddtn table with common flag emoji, add automatically
- add forgot password link
- https://stackoverflow.com/questions/2272002/adding-forgot-password-feature-to-django-admin-site
- admin.py hide if empty show if data
- html in snippet, go back to accessibility

———————————————————————————————————————— housekeeping possibilites

- link do housekeeping now
- in admin need list of uploaded files svg & folders
- in admin need list of svgs & folders, printout of all uploads?
- add function to page load for admins only or scheduled: datadump
- - remove "update needed" from source if google font is checked
- - backup database dump
- add edit history (names, dates & times)
- add sizes to svg's for pages, check placed images for sizes
- svg filesizes in admin, warning banners on pages, admin menu when logged in

———————————————————————————————————————— investigate

- use css or other to make web pages printable IT'S ENOUGH TO NOT HAVE A MARGIN
- fetch JS & promises

———————————————————————————————————————— big improvements

- swipe navigation
- img serving
- animation lab popup to develop animations : show id's of each SVG element, work with JS in a separate window, keep at end, save to page, to file etc.
- add integration of sound effects
- bulk actions (mark pages as active): https://docs.djangoproject.com/en/2.2/ref/contrib/admin/actions/
- add database creation script to backup so with all files, you have everything to recreate the site
- admin menu when logged in w dropdown page list
- automatic menu generation
- admin module / top bar w/ all pages

- not trivial: dans les pages admin, ajouter puce "archivé" pour chaque page, et par défaut de ne pas montrer les pages archivées : https://stackoverflow.com/questions/851636/default-filter-in-django-admin

- capacity de télécharger PDF du site entier (pour modes d'emploi, par exemple)

- need links between same pages in different languages

- in admin need list of uploaded files svg & folders
- print hierarchie with pipe characters in monospaced font?

- add languages, see:
- https://stackoverflow.com/questions/21469470/how-can-i-change-django-admin-language
- in comments

- dans les pages admin, remplacer date créé par date modifié
- https://stackoverflow.com/questions/37540744/django-datetime-default-value-in-migrations
- if I add date modified, I have to do manual migrations the fist time

- change anim lab becomes object finder
- add real return email addresses
- download .zip's of modules

———————————————————————————————————————— huge improvements

- capacity de télécharger PDF du site entier (pour modes d'emploi, par exemple)
- dans les pages admin, ajouter puce "archivé" pour chaque page, et par défaut de ne pas montrer les pages archivées : https://stackoverflow.com/questions/851636/default-filter-in-django-admin

- accepter PDF comme input have a list of font widths for substituting common fonts
- version of program as mac/pc app to host site locally

———————————————————————————————————————— working from here down

- https://stackoverflow.com/questions/6541477/ordering-choices-in-modelform-manytomanyfield-django/6541738#6541738
- https://stackoverflow.com/questions/8992865/django-admin-sort-foreign-key-field-list

———————————————————————————————————————— done

- permettre d'utiliser les scripts & seo téléchargés aussi bien que les scripts collés dans les pages admin
- fix ID's of svg pages in illustrator, right now they're just "Pagename"
- fonts family & style not recorded correctly when missing
- fixed caching issues
- change font name to CSS ref.
- language choice in cookie warning doesn't do anything
- permettre des espaces dans les noms de fichiers SVG etc.
- change custom scripts to user scripts in page admin
- use "slug" where appropriate
- fix capitalization of "Add another Svg file" in admin › page
- wrong label for templates in admin.py (shows URL, notname)
- need to check if menu is oversized, too
- in svg_cleaner reduce oversiized SVG's to page width, other stay the same
- change Links to lower case
- svija help table like notes but w URL for original page, redirect /a
- fix incorrect text "load zindex" on page admin
- FIX ON DELETE link use PROTECT
- change button color so green is save red is delete
- changes to admin.py are not reflected witouth starting uwsgi
- jp cache probs ?
- help text in french (started)
- fixed admin colors to match screenshots of Django defaults
- use defailt live for new page in modeld.py
- cookie module
- admin reduce text contrast
- change rezise so it just updates rem & pixel
- strip out x & y coords for non x=0 tspans
- check AI script removes PDF compat & compression
- add function at end of source to do onload
- spaces in svg filenames won't work
- integrate cookie warning in admin.py
- need an error code for mail sending problems - maybe diffrerent messages for each type of error.
- print the name of the script before each script: when reading source, should be easy to recognize the source of each script
- in addition to .st0 style definitions, replace "#SVGID_4_" definitions

</details>
<details><summary>list 5</summary>

---
- horizontal scrolling wrong after page resize (go into full screen to see)
- ¬ need a way to reset scroll position on resize (horizontally)
- in svg_cleaner.py, if the svg is an empty file (not fully saved for example) the following error will result: local variable 'svg_ID' referenced before assignment. the problem is at line 65: svg_ID = parts2[0] -- return small svg with error message CREATE SMALL SVG ON THE FLY "LOADING INCOMPLETE"
- SVG title shadows on /try are wrong size if page is reloaded on pinch to zoom
- ^M in any text pasted into a field, with returns ckeditor is not the problem, because it happens with language›source comments
- weird text spacing in chrome
- opacity masks broken? 

- housekeeping : add flag emoji, if present, to module & page names (replace * or •)

- confirm that DT missing will redirect to mobile missing
- with same address

- way to group pages for scripts etc.
- svija feature to get scroll position as percentage (percentage read of a page, for example) useable by all
- add js to cache cleared to return to previous page
- make SVG obey z-index

- need a setting (with responsive) for offset x & y for main page
-     so that you can have a module above the page

- small admin module top left corner to clear cache

- add page field total size, updated during housekeeping
- auto search woff
- draggable menu like palette?
- feature imort page/module from zip
- /plus auto add svg's created in lmpast 24 hougrs
- SYNCH/zip or stnc/add
- admin menu on al pages when logged in, like Mac dock
- importe page or module
- invisible div is 1000px high
- need to calculate page height by height of first svg, pass it into
- templates/svija/javascript/initial_scroll.js

- /em/ has trailing slash

- in responsive, in /admin, in responsive I need to check for onresize for mobile,
- so if phone is rotated it will reload as desktop version or redraw

———— not sure
- make menu disappear on zoom, maybe · depends on menu JS

———— admin
- blurb of helpful text for main categories link better link real answer
-   https://stackoverflow.com/questions/6231294/form-field-description-in-django-admin
-   https://stackoverflow.com/questions/7241000/django-short-description-for-property
-   https://stackoverflow.com/questions/42826287/model-description-in-django-admin

- templates/javascript/on_resize.js could scroll to where cursor is
- right now, zooming keeps the top left corner stationary
- this should be fixed AFTER loading in zoomed state is fixed

- message in Admin from msg.svija.com, use xhr request like in mail script
- robots txt choice visible in page title if not live "checkbox alert in title"
- page source in terminal has ^M in comments, have checked and they are added by program (not from pasting)
- need to make specific errors for first part of pageview: missing prefix etc.
- right now, all fonts are loaded. would be better to load only fonts in svg
- add x & y offset for footers etc. (could have footer on side!)
- svija auto conversion svg to form
-   placeholder text in ai with layer id to replace w html text or form, convert an SVG element to HTML automatically

————— responsive : 4 parts
- 0. add default responsive for missing content, option to return 404
- 3. svija mobile, if blank use DT version

———— swipe nav
- arrow key navigation (implies page order, 0= don't include)

————— auto menus
- auto html menus module, add to docs

</details>
<details><summary>list 6</summary>

---
See the various files for explanations.

### lots of issues there:

- fix for invisible page (using windowwidth before focussed)                       
- P3 color broken                                                                  
- vertical & horizontal offset in page parameters have no effect                   
- resizing screws up scrolling: change monitor res from 1280x800 to 2048xN and page is off center
- when beta.svija.com loads, it is shifted to the left initially                   
- script load order general to particular, pages load last                         
- a missing page on mobile 

### fixes

- permettre des espaces dans les noms de fichiers SVG etc. : [stack overflow](https://stackoverflow.com/questions/50794316/handle-spaces-in-the-url-parameter-using-re-path)
- bug no accents in image names                                                    
- check for monitor resolution to test for mobile: if theres no windowwidth, it's a mobile and we never resize
- create custom error for prefixes only work in pairs : if you do fr without fm the page can't load
- in PlacedView view, need to check that it's a valid prefix                       
- fix views.py def PlacedView so that image source comes from settings             
- offset x in pixels is not taken into account when page overrides system settings 
- fix prefix model so there is a pulldown for default page redirect : [stack overflow](https://stackoverflow.com/questions/2642613/what-is-related-name-used-for-in-django)

### verifications

- check that meta_canonical.py is using the prefix list for correct equivalences   
- chrome fonts?                                                                    
- admin page layout: https://stackoverflow.com/questions/8668723/django-grouping-columns-in-django-admin-section                                    
- do local fonts like Arial work? set up Arial by default                          
- menu redraw js in mobile version comes from where?                               
- what are correct metatags for different resolutions?                             
- check cascades for menus, packages, templates so pages don't get deleted         
- in svg_cleaner reduce oversiized SVG's to page width, other stay the same
### unfinished

- /fr/ is hardcoded                                                                                                                               
- postgre_setup.sql has CET timezone hard coded                                    
- need to modify mobile.js to handle multiple responsive's                         
- javascript depends on mobile/desktop width, but responsive can use any width     
- /modules/meta_canonical.py does not handle more than two resolutions             
- main urls.py fr en de etc. (check for existing language rather than just FR)     
- & fr & fm are hardcoded in responsive.js & responsive.js in ozake.com/scripts has hard-coded languages

</details>

