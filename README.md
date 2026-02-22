# Chuiyang Meng Personal Website

This repository is ready for GitHub Pages deployment.

## Option A (Recommended): Personal site

Use repository name:

`<your-github-username>.github.io`

Then your site URL will be:

`https://<your-github-username>.github.io/`

## Option B: Project site

Use any repository name, for example:

`personal-website`

Then your site URL will be:

`https://<your-github-username>.github.io/personal-website/`

## Deploy Steps

1. Create a new GitHub repository.
2. Push this project to branch `main`.
3. In GitHub, open `Settings` -> `Pages`.
4. Set source to `GitHub Actions`.
5. Wait for workflow `Deploy GitHub Pages` to finish.
6. Open the URL shown in Pages settings.

## Local Preview

Run:

```bash
python3 -m http.server 8000
```

Then open:

`http://localhost:8000`

