# Four Seasons Across China Final Project Report

## Project Overview

Four Seasons Across China is an interactive website created for my Web Technologies final project. The site presents one representative landscape for each season: spring in Kunming, summer in Hainan, autumn in Jiuzhaigou, and winter in Tibet. The homepage gives each season a photographic entry point. Clicking an image opens a page with a larger version of that photograph, an English quotation, and the author's name.

The final version uses Python, HTML, CSS, and JavaScript. Python is implemented with the standard library only. The website does not require Flask, Jinja, a database, or any third-party package. This choice keeps the project easy to run and makes every main part of the website visible in a small number of files.

## Project Goals

The first goal was to make the interaction immediately understandable. A visitor should know what to click without reading a long instruction.

The second goal was to give the four seasons clearly different visual identities. Each location has a distinct climate and landscape, and the photograph, page colour, and quotation work together to communicate that difference.

The third goal was to practise the main parts of a web project: HTML structure, CSS layout and animation, JavaScript interaction, Python routing, template rendering, static file delivery, testing, and responsive design.

## Project Content

| Season | Location | Visual focus | Quotation |
| --- | --- | --- | --- |
| Spring | Kunming, Yunnan | Cherry blossoms and traditional architecture | The earth laughs in flowers. Ralph Waldo Emerson |
| Summer | Hainan | Palm trees, blue sky, and the coast | Deep summer is when laziness finds respectability. Sam Keen |
| Autumn | Jiuzhaigou, Sichuan | Autumn forest reflected in clear water | Autumn is a second spring when every leaf is a flower. Albert Camus |
| Winter | Tibet | Snow-covered mountains and reflected morning light | If winter comes, can spring be far behind? Percy Bysshe Shelley |

The seasonal pages keep the content minimal. The large photograph supports the location, while the quotation provides a short literary response to the season. The English text matches the intended audience and keeps the site consistent.

## Website Design

The homepage uses a warm paper background, dark typography, and a four-card image grid. The cards have a strong vertical format so that each photograph remains the main visual element. On hover or keyboard focus, the image enlarges slightly and a small arrow appears. This gives visible feedback before navigation.

Each season page has two main areas on desktop screens. The photograph occupies the larger left area, and the quotation occupies the right area on a colour taken from the image. Previous and next links at the bottom support continuous exploration. The design changes to a single vertical layout on smaller screens, where the image appears first and the quotation follows below.

The interface avoids a traditional navigation-heavy template. The photographs themselves act as the main navigation, which matches the original idea of a simple image-based interactive website.

## System Architecture

The project has three layers:

| Layer | Responsibility | Implementation |
| --- | --- | --- |
| Client | Displays the interface and handles short interactions | HTML, CSS, JavaScript |
| Python application | Chooses the page, prepares HTML, and serves files | http.server and pathlib |
| Content | Stores seasonal text and image paths | Python dictionaries and local files |

When the browser requests `/`, Python returns the homepage. When it requests `/season/spring`, Python reads the seasonal data, reads the season HTML template, replaces the placeholders, and returns the completed page. Requests beginning with `/static/` return CSS, JavaScript, or image files with the correct MIME type. The `/api/seasons` endpoint returns the same content as JSON.

## Python Implementation

All seasonal content is stored in the `SEASONS` dictionary inside `app.py`. For each season, the dictionary stores the page name, location, image, alternate text, quotation, author, and colour values. Changing content does not require editing a separate page for every season.

The `render_template` function reads an HTML file and replaces placeholders such as `{{NAME}}` and `{{QUOTE}}`. Text values are escaped with Python's `html.escape` before insertion. This keeps the Python part short while still allowing one shared season template to produce four different pages.

The `SiteHandler` class extends `BaseHTTPRequestHandler`. It supports GET and HEAD requests, returns the correct content type, and checks that static files remain inside the static directory. The server reads the `PORT` environment variable so the same file can run locally or on a hosting platform.

## Interaction and Accessibility

The website uses JavaScript for small enhancements. Number keys one through four open the corresponding season from the homepage. Arrow keys move between seasons, and Escape returns to the homepage. On touch screens, a horizontal swipe changes seasons. These shortcuts do not replace normal links, so the website still works if JavaScript is unavailable.

Images include descriptive alternative text. Links and cards have visible keyboard focus outlines. The reduced-motion media query removes most transitions for visitors who prefer less animation. Layouts use responsive CSS rather than separate desktop and mobile pages.

## Testing and Results

I tested both the Python responses and the visual layout.

| Test | What it checks | Result |
| --- | --- | --- |
| Homepage test | All four seasons appear on the homepage | Passed |
| Season page tests | Spring, summer, autumn, and winter return HTTP 200 | Passed |
| Invalid route test | An unknown season returns HTTP 404 | Passed |
| API test | The JSON endpoint returns four records | Passed |
| Static image test | An image returns HTTP 200 with the JPEG type | Passed |
| Health check | The server reports that it is running | Passed |

The six automated tests run with `python -m unittest discover -s tests -v`. I also checked the homepage and all four season pages in a desktop browser and checked the season layout at a mobile viewport. The screenshots included with the project show the final layouts.

## Design Challenges and Solutions

The first challenge was choosing photographs that created an immediate seasonal contrast. A one-region set of four Hainan images did not show enough visual change. Using four locations solved this problem while giving the website a clear subtitle: one country and four different seasons.

The second challenge was delivering the same visual result without a framework. Flask would have provided templates and routes automatically, but it would also hide much of the request handling from a beginner. The standard library version makes the request flow explicit: inspect the URL, choose content, build the response, and send a status and content type.

The third challenge was responsive image layout. The source photographs have different dimensions and orientations. CSS `object-fit: cover` provides a consistent visual area while preserving the subject. Separate object positions keep important parts of each photograph visible after cropping.

## Conclusion

The final website meets the main project goal: a visitor can understand the four-season structure quickly, click a photograph, and move through the content without unnecessary steps. The project combines Python, HTML, CSS, and JavaScript in a way that remains small enough to explain during a presentation.

The final implementation also demonstrates a complete delivery process. It includes reusable templates, static assets, automated tests, responsive behaviour, a health endpoint, a JSON API, visual previews, and deployment configuration. The website can run locally with one Python command and is ready to be uploaded to GitHub and deployed as a public web service.

