---
layout: archive
title: "Sitemap"
permalink: /sitemap/
author_profile: true
---

{% include base_path %}
{% comment %}
  Plain title lists. (archive-single.html renders excerpts, and excerpts of notes that
  start with {% include toc %} bring their TOC sidebar along, which broke this page.)
{% endcomment %}

A list of all the posts and pages found on the site. For you robots out there, there is an [XML version]({{ base_path }}/sitemap.xml) available for digesting as well.

<div class="sitemap" markdown="0">

<h2>Pages</h2>
<ul>
{% assign pages_sorted = site.pages | where_exp: "p", "p.title" | sort: "title" %}
{% for p in pages_sorted %}
  {% unless p.url contains '404' or p.url == '/sitemap/' %}
  <li><a href="{{ base_path }}{{ p.url }}">{{ p.title }}</a></li>
  {% endunless %}
{% endfor %}
</ul>

<h2>Posts</h2>
<ul>
{% for p in site.posts %}
  <li><a href="{{ base_path }}{{ p.url }}">{{ p.title }}</a> <span class="sitemap__date">{{ p.date | date: "%b %Y" }}</span></li>
{% endfor %}
</ul>

{% for collection in site.collections %}
{% unless collection.output == false or collection.label == "posts" or collection.docs.size == 0 %}
<h2>{{ collection.label | capitalize }}</h2>
<ul>
{% assign docs_sorted = collection.docs | sort: "title" %}
{% for p in docs_sorted %}
  <li><a href="{{ base_path }}{{ p.url }}">{{ p.title | default: p.url }}</a></li>
{% endfor %}
</ul>
{% endunless %}
{% endfor %}

</div>
