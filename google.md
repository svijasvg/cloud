[logo]: http://files.svija.love/github/readme-logo.png "Svija: SVG-based websites built in Adobe Illustrator"

*Updated  9 September, 2024 · dev.svija.love*

![Svija: SVG-based websites built in Adobe Illustrator][logo]

### Google Indexing

The site is indexed — there are two pages of listings if I type site:svija.com

But it is not in first 10 pages of listings for Svija.

"With Svija, everything is possible" is shown in Google info as text on the
home page, but an exact text search turns up nothing.

Svija robots.txt:
```
user-agent: *
disallow:
sitemap:https://svija.com/sitemap.txt
```

---
### Search Console

According to search console, faq is:
- on google
- indexed
- served over HTTPS

View data about indexed pages:
- the expected pages are indexed
- est live URL: FAQ looks normal, but cut off and wrong title font

Why pages aren't indexed:
- 44 pages with redirects

[Page Speed Insights](https://pagespeed.web.dev/analysis/https-svija-com/yqjq49qcb0?utm_source=search_console&form_factor=mobile&hl=en) gives good results.

---
### Google Blacklist

https://webmasters.stackexchange.com/questions/95656/page-only-shows-up-in-google-for-site-search-but-not-even-for-a-search-for-it
- has some interesting tools

[Safe Browsing Status](https://transparencyreport.google.com/safe-browsing/search?url=svija.com) finds no unsafe content

---
### analytics.moz.com

0 ranking keywords

---
### are 404 pages being handled correctly

They are returning 404 codes, but they are still in Search Console.

I added the following to missing page:
``` 
</style>
<meta name="robots" content="noindex">
<style>
```
---
### Sitemap.txt

It is working correctly according to Search Console.

---
### Miscellaneous

- exclude /missing in robots.txt

New sites are hidden from Google by default.

- update when fixing vibe version
- list sitemap in robots.txt (add to cloud issues)
- robots.txt may be case sensitive — fix case of "user-agent" for example

according to https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt:

Google supports the following fields:

- user-agent: identifies which crawler the rules apply to.
- allow: a URL path that may be crawled.
- disallow: a URL path that may not be crawled.
- sitemap: the complete URL of a sitemap.

Many sites agree that an empty disallow has no effect (`disallow:`).

[Google Documentation](https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt)

---
### Special Characters

```
Crawlers MUST support the following special characters:

+===========+===================+==============================+
| Character | Description       | Example                      |
+===========+===================+==============================+
| #         | Designates a line | allow: / # comment in line   |
|           | comment.          |                              |
|           |                   | # comment on its own line    |
+-----------+-------------------+------------------------------+
| $         | Designates the    | allow: /this/path/exactly$   |
|           | end of the match  |                              |
|           | pattern.          |                              |
+-----------+-------------------+------------------------------+
| *         | Designates 0 or   | allow: /this/*/exactly       |
|           | more instances of |                              |
|           | any character.    |                              |
+-----------+-------------------+------------------------------+
```

---
### ideas

- did I misunderstand robots.txt NO
- check on centrefrance DONE
- can I find some text specific to our site and look for it? NOT LISTED
- check out webmaster console
- bing, kagi etc.
- difference trail2lhers.svija.site and svija.com?

---
### CSS is clearly off-limits

```
height: 20rem;
margin-top: -22rem;
```
This clearly looks like cheating.

---
### VbCA

- site:centrefrance.levillagebyca.com turns up nothing — not referenced at all.
- indexing is enabled

---
### kyaarch · stasis 02

google shows:
```
Galerie | KYAARCH

svija.site
https://kyaarch.svija.site › galerie
This website requires javascript. Either enable javascript or visit with a different browser. This website needs cookies to work. Please enable cookies or ...
```
---
### trail2lhers · dns01

Several pages listed if I search for site:svija.site

---
### pizzandiamo.fr · dns01

Robots set to hidden.

---
### victoriaskov.com · stasis01

Robots set to hidden (fixed).

---
### fleursdecoton-blatin.fr · stasis01

Indexed normally.

---
### melissa.christiaenssens.svija.site

site:melissa.christiaenssens.svija.site

no listings
not blocked by robots

---
### Most Popular Search Engines

- 95% Google
- 6% Bing
- 3% Yahoo
- Duck Duck Go
- Yandex

We are absent from Google, Bing and Yahoo, and Duck Duck Go.

We are first in Yandex, whoo hoo.

---
### La Solution

some javascript that will create CSS variables that will then resize & move the accessibility text

I changed the compromising CSS to javascript to create CSS variables.

It probably won't work, but it might help temporarily while I search for a real solution.
