from __future__ import annotations

import argparse
from pathlib import Path
from pprint import pprint

from client_sdk import LicenseClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PyLicense activation tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    request_parser = subparsers.add_parser("request", help="Generate activation request")
    request_parser.add_argument("--product", default="DemoApp")
    request_parser.add_argument("--version", default="1.0")

    activate_parser = subparsers.add_parser("activate", help="Verify a license file")
    activate_parser.add_argument("license_path", nargs="?", default="licenses/license.dat")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    root = Path.cwd()
    client = LicenseClient(root=root)

    if args.command == "request":
        request = client.create_request(args.product, args.version)
        print(f"Activation request saved to {client.paths.request_file}")
        pprint(request.to_dict())
        return

    if args.command == "activate":
        ok, message = client.verify(Path(args.license_path))
        print(message)
        raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
