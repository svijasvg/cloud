[logo]: http://files.svija.love/github/readme-logo.png "Svija: SVG-based websites built in Adobe Illustrator"

*Updated  14 December, 2022 · dev.svija.love*

![Svija: SVG-based websites built in Adobe Illustrator][logo]

### Adobe Fonts

So, I will add an Adobe font to the home page at svija.dev.

1. go to Character panel, click in font field
2. click **Find More** and wait for it to intialize
3. activate Acier BAT / text gris (click on cloud)
4. cloud w/ double arrow means "activating"

Activation takes a long time — possibly because iPad is downloading iOS 16.1 ?

Oops, I had deactivated the CC app on startup :-(

CC says installed, I try to reinstall and it takes a looooong time.

I quit AI and restart *au cas où*.

Looking at https://helpx.adobe.com/fonts/kb/troubleshoot-font-activation.html

restarting computer & router fixed everything

font is installed, and on the home page.

---
### Svija Admin

In the Fonts admin, I see:

    AcierBATText-Gris

---
### Adobe Fonts in Web Projects

You must be signed in at **fonts.adobe.com** to continue.

In Adobe CC app, navigate to font, then click external link icon (boxed arrow)

This will navigate to:

    https://fonts.adobe.com/fonts/acier-bat

Click on:

- \</> Add to Web Project

Adobe provides instructions [here](https://helpx.adobe.com/fonts/using/add-fonts-website.html):

You must create a new project or choose an existing project.

Projects are managed at [My Fonts › Web Projects](https://fonts.adobe.com/my_fonts#web_projects-section).

Click **Create** to get the following information:

    <link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">

Fonts added:

```
font-family: acier-bat-gris,sans-serif;
font-weight: 400;
font-style: normal;
```

BOTH fields have little copy-box icons. Clicking works but provides no feedback.

ADDITIONALLY, there is a note **If you'd like to use fonts in HTML email, use the @import link.**.

Clicking the **@import** link displays the following code:

```
<style>
  @import url("https://use.typekit.net/jpl1zaz.css");
</style>
```

Finally, the aforementioned **jpl1zaz.css** contains:

```
/*
 * The Typekit service used to deliver this font or fonts for use on websites
 * is provided by Adobe and is subject to these Terms of Use
 * http://www.adobe.com/products/eulas/tou_typekit. For font license
 * information, see the list below.
 *
 * acier-bat-gris:
 *   - http://typekit.com/eulas/00000000000000007735dfaf
 *
 * © 2009-2022 Adobe Systems Incorporated. All Rights Reserved.
 */
/*{"last_published":"2022-12-14 13:47:57 UTC"}*/

@import url("https://p.typekit.net/p.css?s=1&k=jpl1zaz&ht=tk&f=27707&a=24326271&app=typekit&e=css");

@font-face {
font-family:"acier-bat-gris";
src:url("https://use.typekit.net/af/b2b981/00000000000000007735dfaf/30/l?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n4&v=3") format("woff2"),url("https://use.typekit.net/af/b2b981/00000000000000007735dfaf/30/d?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n4&v=3") format("woff"),url("https://use.typekit.net/af/b2b981/00000000000000007735dfaf/30/a?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n4&v=3") format("opentype");
font-display:auto;font-style:normal;font-weight:400;font-stretch:normal;
}

.tk-acier-bat-gris { font-family: "acier-bat-gris",sans-serif; }
```

---
### Current Font Implementation

The program is found at `views/modules/get_fonts.py`:

For each enabled font object:
1. if the font source contains slashes, just keep the end
2. if it's a google font  
• make style lowercase and remove spaces  
• replace spaces in family name with +
• do *not* add source to CSS
3. if source contains 'woff2', add source to CSS
4. if source contains 'woff', add source to CSS
5. if source contains a ',' add local font source to CSS

When done, add all Google fonts to google_link string.

Returns a **google stylesheet link** and list of **@font-face's** for CSS 

---
### What can I copy and Paste

The goal is to make it as easy as possible for the user.

The fewest possible clicks.

If I can read the css file, I can get its contents, and modify the "font-family" attribute
to the correct name.

Planned process:

1. the user clicks the copy icon to copy the following:
```
<link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">
```
2. the user pastes that line into a new Adobe CSS field (1488 bytes)

3. on first request, the field is modified:  
• the stylesheet is fetched  
• remove @import url("…")  
• remove the class statement at the end  
• simplify the src:url statement to contain only the woff version  
• replace the first line with /* 221214\n \*\n

This all depends on being able to read the contents of the stylesheet
