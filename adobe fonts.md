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

You must be signed in at **fonts.adobe.com** to continue.

In Adobe CC app, navigate to font, then click external link icon (boxed arrow)

This will navigate to:

    https://fonts.adobe.com/fonts/acier-bat

Click on:

- \</> Add to Web Project

Adobe provides instructions [here](https://helpx.adobe.com/fonts/using/add-fonts-website.html):

You must create a new project or choose an existing project.

**where are projects managed?**

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







https://fonts.adobe.com/fonts/futura-pt
