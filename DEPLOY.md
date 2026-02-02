## Your current setup (how this repo deploys)

- **This repo (`academic-kickstart/`)** is the *source* (Markdown + config).
- **`public/`** is a git **submodule** that points to your GitHub Pages repo:
  `vipanchikatthula/vipanchikatthula.github.io`.
- **`themes/academic/`** is a git **submodule** for the Academic theme.

The workflow is always:

1) edit content in this repo
2) run Hugo → it writes the generated static site into `public/`
3) commit + push in **two places**:
   - commit/push this repo (source changes)
   - commit/push `public/` (generated site) to update GitHub Pages

---

## One-time setup (per new machine)

### 1) Fetch submodules (theme + public deploy repo)

```bash
cd "academic-kickstart"
git submodule update --init --recursive
```

### 2) Install Hugo (pinned to your theme era)

Your theme submodule is from March 2020, and your old Netlify config pinned Hugo 0.66.0.
On Apple Silicon, Homebrew may be blocked in some networks, so this repo uses a local Hugo binary.

```bash
cd "academic-kickstart"
mkdir -p .bin
curl -fL "https://github.com/gohugoio/hugo/releases/download/v0.66.0/hugo_extended_0.66.0_macOS-64bit.tar.gz" -o .bin/hugo.tar.gz
tar -xzf .bin/hugo.tar.gz -C .bin
chmod +x .bin/hugo
./.bin/hugo version
```

### 3) (Optional) Python virtualenv for helper commands

This repo includes a small helper script at `tools/deploy.py`.

```bash
cd "academic-kickstart"
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

---

## Day-to-day: edit → build → preview locally → commit → push

### 1) Edit content (examples)

- **Resume PDF**: replace `static/files/resume.pdf`
- **Profile photo**: replace `content/authors/admin/avatar.jpg`
- **Bio/intro text**: edit `content/authors/admin/_index.md`
- **Contact fields (email/phone/address)**: edit `config/_default/params.toml`
- **Add a publication**: add a folder under `content/publication/<slug>/index.md` (and optional `cite.bib`, `featured.jpg`)

### 2) Build the site (generate into `public/`)

```bash
cd "academic-kickstart"
./.bin/hugo --gc --minify
```

This regenerates the static site into `public/`.

### 3) Preview locally before pushing

#### Preview the generated site (`public/`) exactly as GitHub Pages will serve it

```bash
cd "academic-kickstart/public"
python3 -m http.server 8000
```

Open `http://localhost:8000/` in Chrome. Stop with Ctrl+C.

#### Preview via Hugo dev server (auto-reload while editing)

```bash
cd "academic-kickstart"
./.bin/hugo server --disableFastRender --i18n-warnings
```

Open `http://localhost:1313/` in Chrome.

### 4) Commit changes in the source repo (`academic-kickstart/`)

```bash
cd "academic-kickstart"
git status
git add -A
git commit -m "Update portfolio content"
git push
```

### 5) Commit + push the generated site (`public/` → GitHub Pages)

```bash
cd "academic-kickstart/public"
git add -A
git commit -m "Rebuild site"
```

Push to GitHub Pages repo (the submodule is often on a detached HEAD, so this form is safest):

```bash
cd "academic-kickstart/public"
git push origin HEAD:master
```

GitHub Pages updates from that repo’s `master` branch.

---

## Optional: “one command” deploy helper (build + commit + push `public/`)

From this repo root:

```bash
cd "academic-kickstart"
source .venv/bin/activate
python tools/deploy.py deploy --message "Rebuild site" --branch master
```

---

## If `git push` fails (most common cause: not authenticated)

This environment may not be able to prompt for GitHub credentials, but your normal terminal can.

Fix options:

- **Use GitHub Desktop** to sign in, then retry `git push`
- **Use a Personal Access Token (PAT)** (recommended if you use HTTPS):
  - Create a token with repo access
  - Then push from your own terminal (avoid pasting tokens into logs/history)
- **Use SSH** if your network allows port 22 and you have keys set up

### If you see proxy errors

If you get errors like `Could not resolve proxy: ...`, temporarily disable proxy for the push:

```bash
cd "academic-kickstart/public"
env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY -u all_proxy -u ALL_PROXY \
git push origin HEAD:master
```

