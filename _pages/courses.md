---
layout: archive
title: "Courses"
permalink: /courses/
author_profile: true
---

{% include base_path %}
{% comment %} Course data lives in _data/courses.yml {% endcomment %}

<div class="courses">

<nav class="courses-jump" aria-label="Jump to school">
{% for school in site.data.courses %}
  {% assign count = 0 %}
  {% for t in school.terms %}{% assign count = count | plus: t.courses.size %}{% endfor %}
  <a href="#{{ school.id }}">{{ school.school }}{% comment %} <span>{{ count }}</span>{% endcomment %}</a>
{% endfor %}
</nav>

<p class="courses-styleguide"><i class="fas fa-fw fa-pen-nib" aria-hidden="true"></i>How the notes are written: note style guides for <a href="{{ base_path }}/notes/style/jekyll/">Markdown (Jekyll)</a> · <a href="{{ base_path }}/notes/style/obsidian/">Markdown (Obsidian)</a> · <a href="{{ base_path }}/notes/style/handwritten/">Handwritten</a></p>

{% for school in site.data.courses %}
{% assign count = 0 %}
{% for t in school.terms %}{% assign count = count | plus: t.courses.size %}{% endfor %}
<section class="course-school" id="{{ school.id }}">
  <h2 class="course-school__name">{{ school.school }}<span class="course-school__meta">{{ school.years }}{% comment %} · {{ count }} courses{% endcomment %}</span></h2>

  {% if school.note %}
  <p class="course-school__note">{{ school.note | markdownify | remove: '<p>' | remove: '</p>' | strip }}</p>
  {% endif %}

  {% for t in school.terms %}
  <div class="course-term">
    <h3 class="course-term__name">{{ t.term }}</h3>
    <ul class="course-list">
      {% for c in t.courses %}
      {% assign kinds = "" | split: "" %}
      {% if c.kind %}
        {% assign kinds = c.kind | join: ',' | split: ',' %}
      {% elsif c.url %}
        {% if c.url contains 'drive.google.com' %}{% assign kinds = kinds | push: 'pdf' %}
        {% elsif c.url contains '/posts/' %}{% assign kinds = kinds | push: 'article' %}
        {% else %}{% assign kinds = kinds | push: 'md' %}{% endif %}
      {% endif %}
      <li class="course">
        <span class="course__code">{{ c.code }}</span>
        <span class="course__title">
          {% if c.url %}<a href="{% unless c.url contains '://' %}{{ base_path }}{% endunless %}{{ c.url }}">{{ c.title }}</a>{% else %}{{ c.title }}{% endif %}
          {% if c.extra %}<span class="course__extra">{{ c.extra }}</span>{% endif %}
        </span>
        {% if kinds.size > 0 %}<span class="course__badges">{% for k in kinds %}<span class="course__badge course__badge--{{ k }}">{% case k %}{% when 'md' %}Markdown{% when 'pdf' %}PDF{% when 'tex' %}TeX{% when 'article' %}Article{% else %}{{ k }}{% endcase %}</span>{% endfor %}</span>{% endif %}
      </li>
      {% endfor %}
    </ul>
  </div>
  {% endfor %}
</section>
{% endfor %}

</div>
