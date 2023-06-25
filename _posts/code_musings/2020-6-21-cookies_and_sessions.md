---
layout: post
title: Cookies and Sessions
permalink: code_musings/cookies_and_sessions
---
This post summarises how cookies and sessions work, and is primarily for me to be a quick reference. [Mozilla's dev site](https://developer.mozilla.org/en-US/docs/Web/HTTP) has some pretty in depth discussions on this.  

HTTP is stateless, but not sessionless. Being stateless means that there is no link between two requests being carried out on the same connection. So a browser can remember if a user has been logged in etc. 

Cookie are a small piece of [data](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies) that a server sends to the web-browser. After receiving a HTTP request, server can send a "Set-Cookie" header with the response
