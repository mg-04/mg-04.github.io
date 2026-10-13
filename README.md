# mg-04.github.io

Source for **[mg-04.github.io](https://mg-04.github.io)**, the personal site of Ming Gong (ECE PhD student, Carnegie Mellon University): research, teaching, projects, course notes, and blog posts.

Built with Jekyll on the [Academic Pages](https://github.com/academicpages/academicpages.github.io) template (itself a fork of [Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/)). Template documentation is kept [below](#academic-pages).

## Site sections

| Nav item | Source | Notes |
|---|---|---|
| Home | `_pages/home.md` | Bio, research interests, teaching timeline |
| Research | `_publications/` | Papers, posters, reports |
| Teaching | `_teaching/` | Grouped by school; `materials:` adds study-guide links |
| Projects | `_projects/` | Filterable by tag; `highlights` tag pins favorites |
| Courses | `_data/courses.yml` | Rendered by `_pages/courses.md` |
| Blog Posts | `_posts/` | Year timeline with tag filter |
| Resume / CV | `_articles/resume.md`, `_articles/cv.md` | Served at `/resume/` and `/cv/` |
| About this site | `_pages/about.md` | Hub for pages outside the menu; linked from the home page footer |

## Repository layout

```
_articles/        Course notes (typed markdown) and the resume/CV, grouped by semester and course
_courses/         Course landing pages (/courses/<slug>), in <school>_<term>/ folders (e.g. columbia_f25/)
_data/            courses.yml (course list), tag_labels.yml (tag display names), navigation.yml
_includes/        Template partials, plus tag-filter.html and tag-label.html
_pages/           Main pages (home, about, courses, teaching, projects, blog list, ...);
                    site/ holds archives, sitemap, 404; template/ holds Academic Pages demo pages
_posts/ _projects/ Year folders (_posts/2025/, _projects/2025/); URLs come from each file's permalink
_publications/ _teaching/ _talks/   Other Jekyll collections
_sass/            Theme styles; site customizations live in _custom.scss and theme/_dark.scss
docs/             Note-taking style guides (served under /notes/style/: jekyll, obsidian, handwritten)
files/            Downloadable files (PDFs), e.g. files/teaching/<course>/
images/           Site images: posts/<post>/, teaching/<course>/, projects/, research/, vlsi/, ...
```

## Adding content

- **Blog post**: add `_posts/YYYY/YYYY-M-D-slug.md` with `title`, `date`, `permalink`, `tags` (from `ece`, `teaching`, `vlsi`, `sr`, `misc`), an `excerpt`, and optionally `teaser:` for the list thumbnail (otherwise the first image in the post is used). Follow `docs/style.md`.
- **Project**: add `_projects/YYYY/<slug>.md` with `permalink: /projects/<slug>/`, `tags` (e.g. `vlsi`, `digital`, `analog`, `os`, `networking`, `embedded`, `software`, `architecture`, `math`, `physics`, `misc`; add `highlights` to feature it) and a `teaser`.
- **Course**: add one line to `_data/courses.yml`. Set `kind` to `md`, `pdf`, `tex`, or `article` (or a list) to pick the badge; without it the badge is inferred from the URL.
- **Teaching**: add `_teaching/<year>-<course>.md` with `venue` (used to group by school), `type`, `course_id`, and optional `materials:` / `materials_label:`.
- **Tag display names**: acronyms go in `_data/tag_labels.yml`; other tags are shown capitalized.
- **Images**: put them under `images/` in a folder named after the post, course, or project, with descriptive file names.

## Running locally

```sh
bundle install
bundle exec jekyll serve --port 4001
```

Jekyll only reads `_config.yml` at startup, so restart the server after editing it. Setup details for each OS (and Docker / Dev Container options) are in the template section below.

---

# Academic Pages
**Academic Pages is a GitHub Pages template for personal and professional portfolio-oriented websites.**

![Academic Pages template example](images/homepage.png "Academic Pages template example")

## Getting Started

1. Register a GitHub account if you don't have one and confirm your e-mail (required!)
1. Click the "Use this template" button in the top right.
1. On the "New repository" page, enter your public repository name as "[your GitHub username].github.io", which will also be your website's URL.
1. Set site-wide configuration and add your content.
1. Upload any files (like PDFs, .zip files, etc.) to the `files/` directory. They will appear at https://[your GitHub username].github.io/files/example.pdf.
1. Check status by going to the repository settings, in the "GitHub pages" section
1. (Optional) Use the Jupyter notebooks or python scripts in the `markdown_generator` folder to generate markdown files for publications and talks from a TSV file.

See more info at https://academicpages.github.io/

## Running the template locally

```sh
bundle exec jekyll serve --port 4001
```

When you are initially working on your website, it is very useful to be able to preview the changes locally before pushing them to GitHub. To work locally you will need to:

1. Clone the repository and made updates as detailed above.

### Using a different IDE
1. Make sure you have ruby-dev, bundler, and nodejs installed
    
    On most Linux distribution and [Windows Subsystem Linux](https://learn.microsoft.com/en-us/windows/wsl/about) the command is:
    ```bash
    sudo apt install ruby-dev ruby-bundler nodejs
    ```
    If you see error `Unable to locate package ruby-bundler`, `Unable to locate package nodejs `, run the following:
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```
    then try run `sudo apt install ruby-dev ruby-bundler nodejs` again.

    On MacOS the commands are:
    ```bash
    brew install ruby
    brew install node
    gem install bundler
    ```
1. Run `bundle install` to install ruby dependencies. If you get errors, delete Gemfile.lock and try again.

    If you see file permission error like `Fetching bundler-2.6.3.gem ERROR:  While executing gem (Gem::FilePermissionError) You don't have write permissions for the /var/lib/gems/3.2.0 directory.` or `Bundler::PermissionError: There was an error while trying to write to /usr/local/bin.`
    Install Gems Locally (Recommended):
    ```bash
    bundle config set --local path 'vendor/bundle'
    ```
    then try run `bundle install` again. If succeeded, you should see a folder called `vendor` and `.bundle`.

1. Run `jekyll serve -l -H localhost` to generate the HTML and serve it from `localhost:4000` the local server will automatically rebuild and refresh the pages on change.
    You may also try `bundle exec jekyll serve -l -H localhost` to ensure jekyll to use specific dependencies on your own local machine.

If you are running on Linux it may be necessary to install some additional dependencies prior to being able to run locally: `sudo apt install build-essential gcc make`

### Using Docker

Working from a different OS, or just want to avoid installing dependencies? You can use the provided `Dockerfile` to build a container that will run the site for you if you have [Docker](https://www.docker.com/) installed.

You can build and execute the container by running the following command in the repository:

```bash
chmod -R 777 .
docker compose up
```

You should now be able to access the website from `localhost:4000`.

### Using the DevContainer in VS Code

If you are using [Visual Studio Code](https://code.visualstudio.com/) you can use the [Dev Container](https://code.visualstudio.com/docs/devcontainers/containers) that comes with this Repository. Normally VS Code detects that a development container configuration is available and asks you if you want to use the container. If this doesn't happen you can manually start the container by **F1->DevContainer: Reopen in Container**. This restarts your VS Code in the container and automatically hosts your academic page locally on http://localhost:4000. All changes will be updated live to that page after a few seconds.

## Maintenance

Bug reports and feature requests to the template should be [submitted via GitHub](https://github.com/academicpages/academicpages.github.io/issues/new/choose). For questions concerning how to style the template, please feel free to start a [new discussion on GitHub](https://github.com/academicpages/academicpages.github.io/discussions).

This repository was forked (then detached) by [Stuart Geiger](https://github.com/staeiou) from the [Minimal Mistakes Jekyll Theme](https://mmistakes.github.io/minimal-mistakes/), which is © 2016 Michael Rose and released under the MIT License (see LICENSE.md). It is currently being maintained by [Robert Zupko](https://github.com/rjzupkoii) and additional maintainers would be welcomed.

### Bugfixes and enhancements

If you have bugfixes and enhancements that you would like to submit as a pull request, you will need to [fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) this repository as opposed to using it as a template. This will also allow you to [synchronize your copy](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork) of template to your fork as well.

Unfortunately, one logistical issue with a template theme like Academic Pages that makes it a little tricky to get bug fixes and updates to the core theme. If you use this template and customize it, you will probably get merge conflicts if you attempt to synchronize. If you want to save your various .yml configuration files and markdown files, you can delete the repository and fork it again. Or you can manually patch.

---
<div align="center">
    
![pages-build-deployment](https://github.com/academicpages/academicpages.github.io/actions/workflows/pages/pages-build-deployment/badge.svg)
[![GitHub contributors](https://img.shields.io/github/contributors/academicpages/academicpages.github.io.svg)](https://github.com/academicpages/academicpages.github.io/graphs/contributors)
[![GitHub release](https://img.shields.io/github/v/release/academicpages/academicpages.github.io)](https://github.com/academicpages/academicpages.github.io/releases/latest)
[![GitHub license](https://img.shields.io/github/license/academicpages/academicpages.github.io?color=blue)](https://github.com/academicpages/academicpages.github.io/blob/master/LICENSE)

[![GitHub stars](https://img.shields.io/github/stars/academicpages/academicpages.github.io)](https://github.com/academicpages/academicpages.github.io)
[![GitHub forks](https://img.shields.io/github/forks/academicpages/academicpages.github.io)](https://github.com/academicpages/academicpages.github.io/fork)
</div>
