---
layout: page
title: Privacy
description: "How the Bullets website handles your data, and where to find the privacy policy and terms for each Bullets app."
updated: July 2026
include_in_header: false
---

## This website

This site is a static website. It has no accounts, no comment forms and no
shopping cart, so there is nothing here for you to sign up for and nothing for
us to store about you.

We do not run analytics, advertising or third-party tracking scripts on this
site, and we do not set cookies.

The site is hosted on GitHub Pages. Like any web host, GitHub records standard
technical information when a page is requested — such as your IP address and
browser — in order to serve the page and protect the service. That data is
handled by GitHub under
[GitHub's Privacy Statement](https://docs.github.com/site-policy/privacy-policies/github-privacy-statement),
and we do not have access to it.

If you email us at
[{{ site.email }}](mailto:{{ site.email }}), we will have whatever you choose to
put in that email. We use it to answer you, and nothing else.

## Our apps

Each app has its own privacy policy and terms of service, because each app
handles data differently. Those documents are the authoritative ones for the
app in question.

| App | Privacy policy | Terms |
|---|---|---|
{%- for app in site.data.apps %}
| [{{ app.name }}]({{ app.slug | prepend: '/' | append: '/' | relative_url }}) | {% if app.privacy_url %}[Privacy policy]({{ app.privacy_url }}){% else %}—{% endif %} | {% if app.terms_url %}[Terms]({{ app.terms_url }}){% else %}—{% endif %} |
{%- endfor %}

## Contact

Questions about any of this go to
[{{ site.email }}](mailto:{{ site.email }}).
