import json
import os
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Literal, Optional


@dataclass
class ScalarConfiguration:
    # Confirmed working
    hide_internal: bool = False
    hide_download_button: bool = False
    show_sidebar: bool = True
    show_webhooks: bool = True
    show_examples: bool = True
    default_auth: Optional[str] = None
    allowed_auth: Optional[List[str]] = None
    auth_persist: bool = False
    proxy: Optional[str] = None
    expand_authentication: bool = False
    expand_table_of_contents: bool = False
    dark_mode_invert_colors: bool = False
    enable_search: bool = True
    persist_auth: bool = False

    # Known to not currently work
    layout: Optional[Literal["sidebar", "stacked"]] = field(
        default=None, metadata={"note": "Not working"}
    )
    show_models: bool = field(default=True, metadata={"note": "Not working"})
    try_it: bool = field(default=True, metadata={"note": "Not working"})
    show_errors: bool = field(default=True, metadata={"note": "Not working"})
    show_export: bool = field(default=False, metadata={"note": "Not working"})
    render_style: Optional[Literal["view", "read", "sidebar", "full"]] = field(
        default=None, metadata={"note": "Not working"}
    )
    expand_responses: bool = field(default=False, metadata={"note": "Not working"})
    schema_style: Optional[Literal["table", "tree"]] = field(
        default=None, metadata={"note": "Not working"}
    )
    allowed_methods: Optional[
        List[Literal["get", "post", "put", "patch", "delete"]]
    ] = field(default=None, metadata={"note": "Not working"})

    def to_camel_case_dict(self) -> Dict[str, object]:
        return {
            (
                k
                if "_" not in k
                else k.split("_")[0] + "".join(w.capitalize() for w in k.split("_")[1:])
            ): v
            for k, v in asdict(self).items()
            if v is not None
        }

    def to_json(self) -> str:
        return json.dumps(self.to_camel_case_dict())


@dataclass
class ScalarColorSchema:
    __slots__ = (
        "color_1",
        "color_2",
        "color_3",
        "color_accent",
        "background_1",
        "background_2",
        "background_3",
        "background_accent",
        "link_color",
        "code",
    )
    color_1: str
    color_2: str
    color_3: str
    color_accent: str
    background_1: str
    background_2: str
    background_3: str
    background_accent: str
    link_color: str
    code: str

    def to_css(self, mode: str) -> str:
        return f"""
        .{mode}-mode {{
            --scalar-color-1: {self.color_1};
            --scalar-color-2: {self.color_2};
            --scalar-color-3: {self.color_3};
            --scalar-background-1: {self.background_1};
            --scalar-background-2: {self.background_2};
            --scalar-background-3: {self.background_3};
            --scalar-color-accent: {self.color_accent};
            --scalar-background-accent: {self.background_accent};
            --scalar-link-color: {self.link_color};
            code {{ color: {self.code}; }}
        }}""".strip()


class ScalarTheme:
    def __init__(
        self,
        color_scheme_light: ScalarColorSchema = ScalarColorSchema(
            "#121212",
            "rgba(0, 0, 0, 0.6)",
            "rgba(0, 0, 0, 0.4)",
            "#0a85d1",
            "#fff",
            "#f6f5f4",
            "#f1ede9",
            "#5369d20f",
            "#0a85d1",
            "orange",
        ),
        color_scheme_dark: ScalarColorSchema = ScalarColorSchema(
            "rgba(255, 255, 255, 0.81)",
            "rgba(255, 255, 255, 0.443)",
            "rgba(255, 255, 255, 0.282)",
            "#8ab4f8",
            "#202020",
            "#272727",
            "#333333",
            "#8ab4f81f",
            "#0a85d1",
            "orange",
        ),
        favicon_url: Optional[str] = None,
        logo_url: Optional[str] = None,
        logo_url_dark: Optional[str] = None,
    ):
        self.color_scheme_light = color_scheme_light
        self.color_scheme_dark = color_scheme_dark
        self.logo_url = logo_url
        self.logo_url_dark = logo_url_dark
        self.favicon_url = favicon_url

    def to_css(self) -> str:
        return f"{self.color_scheme_light.to_css('light')}\n{self.color_scheme_dark.to_css('dark')}"


class ScalarHeader:
    def __init__(
        self,
        logo_url: str,
        logo_url_dark: Optional[str] = None,
        links: Dict[str, str] = {},
    ):
        self.__logo_url = logo_url
        self.__logo_url_dark = logo_url_dark or logo_url
        self.__links = links

    def to_html(self) -> Optional[str]:
        if not self.__logo_url:
            return None
        nav = "".join(
            f'<li><a target="_blank" href="{url}">{title}</a></li>'
            for title, url in self.__links.items()
        )
        return f"""
        <style>
            :root {{ --scalar-custom-header-height: 64px; }}
            .custom-header {{ height: var(--scalar-custom-header-height); backdrop-filter: blur(5px); display: flex; justify-content: space-between; align-items: center; padding: 0 18px; position: sticky; top: 0; z-index: 100; box-shadow: inset 0 -1px 0 var(--scalar-border-color); background: transparent; color: var(--scalar-color-1); font-size: var(--scalar-font-size-2); }}
            .custom-header nav {{ display: flex; gap: 18px; }}
            .custom-header a:hover {{ color: var(--scalar-color-2); }}
        </style>
        <header class="custom-header scalar-app">
            <div style="padding: 16px;">
                <img class="{'light-only' if self.__logo_url_dark else ''}" src="{self.__logo_url}" style="max-height:24px;">
                {'<img class="dark-only" src="' + self.__logo_url_dark + '" style="max-height:24px;">' if self.__logo_url_dark else ''}
            </div>
            <nav><ul>{nav}</ul></nav>
        </header>
        """.strip()


class ScalarDoc:
    __scalar_cdn_url = "https://cdn.jsdelivr.net/npm/@scalar/api-reference"

    def __init__(self):
        self.__openapi_mode = self.__openapi_url = self.__openapi_json = None
        self.__scalar_configuration = ScalarConfiguration()
        self.__title = "Scalar API Docs"
        self.__theme = ScalarTheme()
        self.__header = None

    @classmethod
    def from_spec(cls, spec: Any, mode: Literal["url", "json"] = "url") -> "ScalarDoc":
        obj = cls()
        obj.set_spec(spec=spec, mode=mode)
        return obj

    def set_spec(self, spec: Any, mode: Literal["url", "json"] = "url"):
        if mode == "url":
            self.__openapi_url = spec
        elif mode == "json":
            self.__openapi_json = spec
        else:
            raise ValueError("mode must be 'url' or 'json'")
        self.__openapi_mode = mode

    def set_title(self, title: str):
        self.__title = title

    def set_theme(self, theme: ScalarTheme):
        self.__theme = theme

    def set_header(self, header: ScalarHeader):
        self.__header = header

    def set_configuration(self, configuration: ScalarConfiguration):
        self.__scalar_configuration = configuration

    @property
    def __header_html(self):
        return self.__header.to_html() if self.__header else ""

    def to_html(self) -> str:
        conf = self.__scalar_configuration.to_json()
        if self.__openapi_url:
            spec_loader = f"""
            <script id="api-reference" data-url="{self.__openapi_url}"></script>
            <script>document.getElementById('api-reference').dataset.configuration = '{conf}';</script>"""
        elif self.__openapi_json:
            spec_loader = f"""
            <div id="api-reference"></div>
            <script>
                const openapiSpec = {self.__openapi_json};
                const loaded_configuration = {conf};
                ScalarAPI.render(document.getElementById("api-reference"), {{
                    spec: openapiSpec,
                    configuration: loaded_configuration
                }});
            </script>"""
        else:
            raise ValueError("Needs `openapi_url` or `openapi_dict`.")

        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>{self.__title}</title>
            <link rel="shortcut icon" href="{self.__theme.favicon_url}">
            <meta name="theme-color" content="{self.__theme.color_scheme_dark.color_accent}">
            <style>
                body {{ margin: 0; padding: 0; }}
                api-reference {{ height: 100vh; display: block; }}
                .introduction-description-heading {{ margin-top: 5em !important; }}
                .dark-mode .light-only {{ display: none; }}
                .light-mode .light-only {{ display: inherit; }}
                .light-mode .dark-only {{ display: none; }}
                .dark-mode .dark-only {{ display: inherit; }}
                {self.__theme.to_css()}
            </style>
        </head>
        <body>
            {self.__header_html}
            {spec_loader}
            <script src="{self.__scalar_cdn_url}"></script>
        </body>
        </html>
        """.strip()

    def to_file(self, path: str):
        (
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if os.path.dirname(path)
            else None
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_html())
