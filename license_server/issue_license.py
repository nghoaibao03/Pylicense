from __future__ import annotations

import argparse
from pathlib import Path
from pprint import pprint

from pylicense.server import ServerPaths, issue_license, parse_expire_or_default


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Issue a signed license from a request")
    parser.add_argument("request_path")
    parser.add_argument("--customer", default="Bao Nguyen")
    parser.add_argument("--expire", default=None)
    parser.add_argument("--edition", default="Enterprise")
    parser.add_argument("--feature", action="append", default=["Export", "ETL", "AI"])
    return parser


def main() -> None:
    args = build_parser().parse_args()
    root = Path.cwd()
    paths = ServerPaths(root=root)
    signed_license = issue_license(
        paths=paths,
        request_path=Path(args.request_path),
        customer=args.customer,
        expire=parse_expire_or_default(args.expire),
        edition=args.edition,
        features=args.feature,
    )
    output_path = paths.license_path(Path(args.request_path))
    print(f"License saved to {output_path}")
    pprint(signed_license.to_dict())


if __name__ == "__main__":
    main()
