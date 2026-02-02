## Portfolio website (Hugo Academic)

This repo is the **source** for my personal website (Markdown + config), built with **Hugo Academic**.

- **Live site**: `https://vipanchikatthula.github.io/`
- **Deploy output**: generated into `public/` (a git submodule that points to `vipanchikatthula/vipanchikatthula.github.io`)

### Why there are 2 commits (source vs generated)

This setup intentionally keeps two repos in sync:

- **Commit/push this repo (`academic-kickstart/`)**: this saves the *editable source* (Markdown, config, images).  
  This is what makes future updates easy — next time you can just pull this repo, edit content, and rebuild.

- **Commit/push `public/`**: this saves the *generated static site* (HTML/CSS/JS) into the GitHub Pages repo.  
  GitHub Pages serves **only** these generated files, so pushing `public/` is what actually updates the live website.

### How to edit content (common updates)

- **Resume PDF**
  - Replace: `static/files/resume.pdf`
  - The site links already point to `/files/resume.pdf`.

- **Profile picture**
  - Replace: `content/authors/admin/avatar.jpg`

- **Bio / intro / description**
  - Edit: `content/authors/admin/_index.md`
    - front matter fields like `name`, `role`, `bio`
    - the Markdown text below the front matter

- **Contact info (remove phone/location, etc.)**
  - Edit: `config/_default/params.toml`
  - Clear fields by setting to empty strings:
    - `phone = ""`
    - `address = { ... }` (clear the parts you don’t want shown)

- **Add a publication**
  - Create: `content/publication/<slug>/index.md`
  - Optional: `content/publication/<slug>/cite.bib` (for the Cite button)
  - Optional: `content/publication/<slug>/featured.jpg` (thumbnail)

### How to build, preview locally, and deploy

See `DEPLOY.md` for the full workflow:
- set up `.venv` with `uv`
- build the site locally
- preview in Chrome
- commit/push changes for **both** repos:
  - commit/push this repo (source changes)
  - commit/push `public/` (generated site) to update GitHub Pages

### License

Copyright 2017-present [George Cushen](https://georgecushen.com).

Released under the [MIT](https://github.com/sourcethemes/academic-kickstart/blob/master/LICENSE.md) license.
