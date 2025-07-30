# cli.py (parte relevante adaptada)
import argparse
import json
import sys
import tomllib  # Python 3.11+
from pathlib import Path

from scalar_doc import ScalarConfiguration, ScalarDoc, ScalarTheme


def load_config_from_files(path: Path) -> dict:
    pyproject_path = path / "pyproject.toml"
    scalar_doc_path = path / "scalar_doc.toml"

    if pyproject_path.exists():
        with pyproject_path.open("rb") as f:
            data = tomllib.load(f)
        scalar_doc = data.get("tool", {}).get("scalar_doc", {})
        if scalar_doc:
            print(f"⚙️\t{pyproject_path} loaded")
            return scalar_doc

    if scalar_doc_path.exists():
        print(f"⚙️\t{scalar_doc_path} loaded")
        with scalar_doc_path.open("rb") as f:
            data = tomllib.load(f)
        return data

    print(f"⚙️\tNo config loaded")
    return {}


def parse_theme(toml_config: dict) -> ScalarTheme:
    base_theme = ScalarTheme()

    config_theme = toml_config.get("theme", {})
    base_theme.favicon_url = config_theme.get("favicon_url", None)

    for key, value in config_theme.get("light", {}).items():
        setattr(base_theme.color_scheme_light, key, value)

    for key, value in config_theme.get("dark", {}).items():
        setattr(base_theme.color_scheme_dark, key, value)

    return base_theme


def parse_scalar_configuration(toml_config: dict) -> ScalarConfiguration:
    base_config = ScalarConfiguration(**toml_config.get("config", {}))
    return base_config


def main():
    parser = argparse.ArgumentParser(
        description="Generate HTML documentation from OpenAPI specs using Scalar"
    )
    parser.add_argument("spec", help="Path or URL to OpenAPI spec (JSON or YAML)")
    parser.add_argument("--output", default="docs.html", help="Output HTML file")
    parser.add_argument(
        "--mode", choices=["url", "json"], default="json", help="Mode of input spec"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print resolved configuration and exit"
    )

    args = parser.parse_args()

    # Load config
    project_root = Path.cwd()
    config_data = load_config_from_files(project_root)

    configuration = parse_scalar_configuration(config_data)
    theme = parse_theme(config_data)

    if args.dry_run:
        print("Resolved ScalarDoc configuration:\n")
        print(json.dumps(config_data, indent=2))
        sys.exit(0)

    # Generate docs
    docs = ScalarDoc.from_spec(args.spec, mode=args.mode)
    docs.set_configuration(configuration)
    docs.set_theme(theme)
    docs.to_file(args.output)
    print(f"✅\tDocumentation generated at {args.output}")


if __name__ == "__main__":
    main()
