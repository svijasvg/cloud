
#:::::::::::::::::::::::::::::::::::::::: iframe_page.py

from django.http import HttpResponse
from django.core.cache import cache
from modules.cache_per_user import *
from django.shortcuts import get_object_or_404, render

@cache_per_user(60*60*24, False)
def iframe_page(request, section_code, request_slug):

  all_screens = "var all_screens = {0:'computer', 400:'mobile'}"
  current_path = "/"
  page_title = "This is the page title"

# https://medium.com/@ashishkush1122/understanding-request-object-in-in-django-39c4eb5c3139

  debug_string = request.META['HTTP_USER_AGENT']
  #  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15

  #  other headers
  #  CONTENT_LENGTH – The length of the request body (as a string).
  #  CONTENT_TYPE – The MIME type of the request body.
  #  HTTP_ACCEPT – Acceptable content types for the response.
  #  HTTP_ACCEPT_ENCODING – Acceptable encodings for the response.
  #  HTTP_ACCEPT_LANGUAGE – Acceptable languages for the response.
  #  HTTP_HOST – The HTTP Host header sent by the client.
  #  HTTP_REFERER – The referring page, if any.
  #  HTTP_USER_AGENT – The client’s user-agent string.
  #  QUERY_STRING – The query string, as a single (unparsed) string.
  #  REMOTE_ADDR – The IP address of the client.
  #  REMOTE_HOST – The hostname of the client.
  #  REMOTE_USER – The user authenticated by the web server, if any.
  #  REQUEST_METHOD – A string such as "GET" or "POST".
  #  SERVER_NAME – The hostname of the server.
  #  SERVER_PORT – The port of the server (as a string).

  debug_string = request.path # /

  debug_string = request.get_host() # svija.dev

  debug_string = request.headers["user-agent"]

  context = {
    'all_screens'  : all_screens,
    'current_path' : current_path,
    'page_title'   : page_title,
    'debug_string' : debug_string,
  }

  template = 'svija/iframe.html'
  return render(request, template, context)

# 225 66.249.66.56 - - [31/Aug/2022:17:14:33 +0200] "GET /robots.txt HTTP/1.1" 200 27 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
# 66.249.66.20 - - [31/Aug/2022:17:39:58 +0200] "GET / HTTP/1.1" 200 107394 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
#  66.249.66.142 - - [31/Aug/2022:19:09:50 +0200] "GET / HTTP/1.1" 200 107394 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
# 113.101.194.127 - - [31/Aug/2022:22:31:47 +0200] "GET / HTTP/1.1" 200 455477 "https://www.whole-search.com/cache/Google/svija.com?q=Google+global+ranking+site%3Awww.whole-search.com" "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
# 34.251.239.16 - - [01/Sep/2022:01:37:16 +0200] "GET / HTTP/1.1" 200 107394 "https://google.com" "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14"
# 66.249.84.10 - - [01/Sep/2022:03:07:37 +0200] "GET /images/apple-touch-icon.png HTTP/1.1" 200 7357 "-" "Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko Firefox/11.0 (via ggpht.com GoogleImageProxy)"
# 34.251.239.16 - - [01/Sep/2022:14:53:33 +0200] "GET / HTTP/1.1" 200 107394 "https://google.com" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36"

