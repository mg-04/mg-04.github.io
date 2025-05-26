---
#layout: post
title:  "Welcome to Jekyll!"
date:   2024-12-20 15:59:30 -0500
permalink: /posts/2024/12/welcome/
tags:
  - misc
excerpt: >
 This is a log page.
---

# 2024-12-20
Welcome!

A few notes for the commands:
`bundle exec jekyll serve --port <port>` serves the site locally to `<port>`

# 2025-1-9 Customizing Page Menu Titles

Each Jekyll page has a header including menu entries to every Jekyll page. However, 
- We may not want every page to be linked in the menu bar
- We may want the text of the links to differ from the page titles

It's a very simple modification on the `minima` theme I'm currently using
1. In the yaml header of all pages, define a new variable, `menu_title`.
```yaml
---
layout: page
title: "Ming Gong"
permalink: /cv
menu_title: "CV"
---
```
2. Locate the html source files of `minima`, namely the `_includes` and `_layouts` folder
3. Copy the two folders over to your page directory
4. In the following section of `_includes/header.html`, change `my_page.title` to `my_page.menu_title`:

    ```html
    {% raw %} <div class="trigger">
        {%- for path in page_paths -%}
        {%- assign my_page = site.pages | where: "path", path | first -%}
        {%- if my_page.menu_title -%}
        <a class="page-link" href="{{ my_page.url | relative_url }}">{{ my_page.menu_title | escape }}</a>
        {%- endif -%}
        {%- endfor -%}
    </div> {% endraw %}
    ```

Now we have a way to separately set page title, menu title, and permalink!

## P.S. How to quote Jekyll code in Jekyll

When formatting the html code block above, Liquid parses curly braces as variables.

You need to escape curly braces with `{{ "{" }}% raw %}` and `{{ "{" }}% endraw %}`


but this won't work directly if you try this yourself, because the escape sequences *themselves* need to be escaped...

I consulted [this](https://stackoverflow.com/a/12948815), which works but its logic is *incredibly* hard to grasp. After some work,  I figured out a much more clear way:
- Escape every instance or group of `{{ "{" }}` with `{{ "{{" }} "{{ "{" }}" }}`
- Everything else, such as `%` and `}` can be typed as plain text

With this, you can play with some fun recursive RegEx

- `{{ "{" }}% raw %}`
- `{{ "{{ " }}"{{ "{" }}" }}% raw %}`
- `{{ "{{" }} "{{ "{{" }} " }}"{{ "{{" }} "{{ "{" }}" }}" }}% raw %}` (I need to evaluate one more time to type this out)

Jae Jae please make this into a CS Theory exam problem and make them design a DFA translator for that :)

**Conclusion:** 
- To escape a large block, use `{{ "{" }}% raw %}` and `{{ "{" }}% endraw %}`
- To escape a few "{{ "{" }}"s, or "{{ "{" }}% raw %}" itself, use `{{ "{{" }} "{{ "{" }}" }}`

# 2025-5-26 New Site
Run
```sh
bundle exec jekyll serve -l -H localhost --port 4002  --force_polling
```
Don't forget `--force_polling` for live regeneration on Windows




