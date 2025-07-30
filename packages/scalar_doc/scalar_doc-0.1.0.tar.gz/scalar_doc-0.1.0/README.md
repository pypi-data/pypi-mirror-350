# 🚀 Scalar DOC

A powerful, customizable, and fully native way to render OpenAPI documentation using [Scalar API Reference](https://github.com/scalar/scalar) — directly from Python 🐍.

---

## ✨ Why Scalar DOC?

**`scalar-doc`** is a lightweight Python package for generating **beautiful, interactive API documentation** from OpenAPI specs using the blazing-fast and modern [Scalar](https://scalar.dev/).

Unlike static alternatives or bulky exporters, Scalar DOC delivers:

* ✅ **100% native Python** — no Node.js or frontend tooling required
* 🎨 **Fully customizable UI** — control layout, themes, and behavior
* 🔌 **Compatible with any OpenAPI source** — JSON files, URLs, or Python dicts from tools like:

  * [FastAPI](https://fastapi.tiangolo.com/)
  * [Flask-RESTPlus](https://flask-restplus.readthedocs.io/)
  * [Django REST Framework](https://www.django-rest-framework.org/)
* ⚙️ **Zero-config or full control** — use sensible defaults or fine-tune every detail
* 🧰 **CLI support** — generate docs straight from the terminal (see below)

---

## 📦 Installation

```bash
pip install scalar-doc
```

---

## ⚙️ Usage

### 🚀 With FastAPI (or any OpenAPI dict)

```python
from fastapi import FastAPI, responses
from scalar_doc import ScalarDoc

DESCRIPTION = """
# Sidebar Section

## Sidebar SubSection

### Title

Content
"""

app = FastAPI(
    title="Test",
    description=DESCRIPTION,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.post("/foo")(lambda a: str: a + " - ok")

# Mount Scalar Docs
docs = ScalarDoc.from_spec(app.openapi(), mode="dict")

@app.get("/docs", include_in_schema=False)
def get_docs():
    return responses.HTMLResponse(docs.to_html())
```

Run your app and access `/docs` to see Scalar in action! ✨

---

### 🧰 Programmatic Usage (Python)

```python
from scalar_doc import ScalarDocs, ScalarConfiguration

# From URL
docs = ScalarDocs.from_spec("https://api.example.com/openapi.json", mode="url")
docs.set_title("My API Docs")

# Optional: configure appearance/behavior
docs.set_configuration(ScalarConfiguration(hide_sidebar=True))

# Export to HTML
docs.to_file("docs/index_from_url.html")

# From local JSON file
with open("openapi.json", "r", encoding="utf-8") as f:
    docs.set_spec(f.read(), mode="json")
    docs.to_file("docs/index_from_file.html")
```

Then open the generated HTML in your browser!

---

### 💻 CLI Usage

You can also use Scalar DOC via command-line:

```bash
scalar-doc path/to/openapi.json --mode json --output docs.html
```

Or from a remote OpenAPI spec:

```bash
scalar-doc https://api.example.com/openapi.json --output docs.html
```

> Customization via CLI is coming soon — stay tuned!

---

## 🎨 Customization Options

Fine-tune your docs' look and behavior using:

* **Theme** — Light/dark color schemes, logo, favicon
* **Header** — Logo (light/dark), external links
* **Configuration** — Toggle visibility of models, sidebar, search, examples, etc.

See the `ScalarConfiguration`, `ScalarTheme`, and `ScalarHeader` classes for full control.

### 🎵 Spotify-style Example

```python
from scalar_doc import (
    ScalarColorSchema,
    ScalarConfiguration,
    ScalarDoc,
    ScalarHeader,
    ScalarTheme,
)

spotify_docs = ScalarDoc.from_spec(
    "https://raw.githubusercontent.com/sonallux/spotify-web-api/refs/heads/main/official-spotify-open-api.yml"
)

spotify_docs.set_title("Spotify")
spotify_docs.set_header(
    ScalarHeader(
        logo_url="https://storage.googleapis.com/pr-newsroom-wp/1/2023/09/Spotify_Logo_RGB_Green.png",
        logo_url_dark="https://storage.googleapis.com/pr-newsroom-wp/1/2023/09/Spotify_Logo_RGB_White.png",
        links={"Spotify": "https://spotify.com"},
    )
)
spotify_docs.set_configuration(
    ScalarConfiguration(
        hide_download_button=True,
        show_models=False,
        expand_table_of_contents=True,
        schema_style="table",
    )
)
spotify_docs.set_theme(
    ScalarTheme(
        favicon_url="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg",
        color_scheme_light=ScalarColorSchema(
            color_1="#191414",
            color_2="#3e3e3e",
            color_3="#1DB954",
            background_1="#ffffff",
            background_2="#f0f0f0",
            background_3="#e6e6e6",
            color_accent="#1DB954",
            background_accent="#d2fbe3",
            link_color="#1DB954",
            code="#2b2b2b",
        ),
        color_scheme_dark=ScalarColorSchema(
            color_1="#ffffff",
            color_2="#aaaaaa",
            color_3="#1DB954",
            background_1="#191414",
            background_2="#121212",
            background_3="#282828",
            color_accent="#1DB954",
            background_accent="#1DB95433",
            link_color="#1DB954",
            code="#1DB954",
        ),
    )
)
```

---

## 📚 References

* 🔗 [scalar.dev](https://scalar.dev/) — Official Scalar docs
* 🔗 [github.com/scalar/scalar](https://github.com/scalar/scalar) — Underlying engine
* 🔗 [OpenAPI Initiative](https://www.openapis.org/) — Specification standard

> This library is not affiliated with Scalar, but proudly uses their open-source engine with ❤️ and proper attribution.

---

## 🤝 Contributing

Found a bug? Have an idea? Want to help improve the library?

Pull requests and issues are warmly welcome!

> ⚠️ Heads up: Some advanced features like `ScalarConfiguration` toggles are still being polished and may not reflect immediately in output. Fixes are planned for the next release.

---

## 📄 License

MIT License. See [LICENSE](./LICENSE) for details.
