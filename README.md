# Four Seasons Across China

An interactive, English-language website built entirely with Python, HTML, CSS, and JavaScript. It uses only Python's standard library, so no third-party packages or virtual environment are required.

The homepage presents four seasons as photographic entry points. Each image opens a page with a seasonal photograph, a quotation, and its author.

## Seasons

| Season | Location | Quotation |
| --- | --- | --- |
| Spring | Kunming, Yunnan | “The earth laughs in flowers.” — Ralph Waldo Emerson |
| Summer | Hainan | “Deep summer is when laziness finds respectability.” — Sam Keen |
| Autumn | Jiuzhaigou, Sichuan | “Autumn is a second spring when every leaf is a flower.” — Albert Camus |
| Winter | Tibet | “If winter comes, can spring be far behind?” — Percy Bysshe Shelley |

## Run locally

This project was tested with Python 3.13, but it uses language features available in recent Python 3 versions.

```powershell
cd "C:\Users\捞把月\Documents\Codex\2026-10-29\wo\outputs\four-seasons-china"
python app.py
```

Open `http://127.0.0.1:5000`.

No `pip install` command is needed.

If the `python` command is not available on the current Windows computer, run:

```powershell
D:\python.exe app.py
```

## Run the tests

```powershell
python -m unittest discover -s tests -v
```

## How Python is used

- `app.py` starts an HTTP server with Python's built-in `http.server`.
- Python defines the data for all four seasons.
- Python generates the homepage cards and season pages from HTML templates.
- Python serves the CSS, JavaScript, and image files.
- `/api/seasons` returns the season data as JSON.
- Invalid routes return a custom 404 page.

## Main features

- Four photographic homepage links
- Previous and next season navigation
- Keyboard navigation with number keys and arrow keys
- Swipe navigation on touch screens
- Responsive desktop, tablet, and mobile layouts
- Reduced-motion support and visible keyboard focus styles
- JSON API and health-check endpoint

## Submission files

- `Project_Report.pdf` - visually checked final report
- `Project_Report.docx` - editable report copy
- `Project_Report.md` - plain-text report source
- `SUBMISSION_FORM_TEXT.md` - copy-ready English project description
- `SUBMISSION_GUIDE_ZH.md` - Chinese instructions for GitHub and deployment
- `previews/` - desktop and mobile screenshots

## Project structure

```text
four-seasons-china/
├── app.py
├── render.yaml
├── templates/
│   ├── index.html
│   ├── season.html
│   └── 404.html
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── images/
├── previews/
│   └── *.png
└── tests/test_app.py
```

## Image use

The four photographs were provided by the project author for this coursework website. Confirm that each image may be published publicly before deploying the project. Keep any required photographer or source credit available in a separate project note.

## Deployment

The included `render.yaml` starts the site with:

```text
python app.py
```

Point the deployment platform to the project root. The server reads the platform's `PORT` environment variable automatically.
