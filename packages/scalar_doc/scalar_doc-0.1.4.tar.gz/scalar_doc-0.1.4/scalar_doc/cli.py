import argparse

from .core import ScalarDoc


def main():
    parser = argparse.ArgumentParser(
        description="Generate static HTML documentation using Scalar Docs."
    )
    parser.add_argument("spec", help="OpenAPI spec (URL or path to JSON file)")
    parser.add_argument(
        "--mode",
        choices=["url", "json"],
        default="url",
        help="Mode to interpret the spec (default: url)",
    )
    parser.add_argument(
        "--output", "-o", default="scalar-docs.html", help="Output HTML file path"
    )

    args = parser.parse_args()

    if args.mode == "url":
        doc = ScalarDoc.from_spec(spec=args.spec, mode="url")
    else:
        with open(args.spec, "r", encoding="utf-8") as f:
            spec_json = f.read()
        doc = ScalarDoc.from_spec(spec=spec_json, mode="json")

    doc.to_file(args.output)
    print(f"✅ Documentation generated: {args.output}")


if __name__ == "__main__":
    main()
