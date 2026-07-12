# bullets.co.kr

The Bullets studio site: who we are, and the four apps we ship — Cineepp,
Pilmie, Drawwii and Unrearix.

Jekyll, built automatically by GitHub Pages. There is no build pipeline: push to
`master` and the site deploys.

## Local

```sh
bundle install
bundle exec jekyll serve
```

## Where things live

| | |
|---|---|
| `_data/apps.yml` | **Every fact about the four apps** — copy, colours, store links, screenshots, legal attributions. The home grid and all four detail pages read from it. Start here. |
| `_layouts/home.html` | The home page. |
| `_layouts/app.html` | One layout drives all four app pages; `_pages/<slug>.md` is a stub that names the app. |
| `_sass/_tokens.scss` | Colours and spacing. `--bg` matches the fill of the logo's squircle on purpose. |
| `tools/import-app-assets.py` | Pulls icons and store screenshots from the app repos, optimizes them to WebP, and writes `assets/`. Run by hand; commit the output. |

App marketing copy is not written here — it comes from each app's store listing
doc (`docs/store-listing*.md` in the app repo). `_data/apps.yml` says which.
Some of that copy is legally load-bearing: the TMDB attribution on Cineepp, the
"never uploaded" promise on Drawwii, and the careful wording around playback on
Unrearix. The file explains each one.

Each app's privacy policy and terms live on that app's own domain; this site
links to them rather than copying them.

---

Originally forked from
[Automatic App Landing Page](https://github.com/emilbaehr/automatic-app-landing-page)
by Emil Baehr (MIT). None of that template's markup or styling remains, but the
licence is kept in `LICENSE` as required.
