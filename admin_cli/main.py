from __future__ import annotations

import argparse
from pathlib import Path

from client_sdk import LicenseClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Admin CLI for PyLicense")
    parser.add_argument("--license", default="licenses/license.dat")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    client = LicenseClient(root=Path.cwd())
    ok, message = client.verify(Path(args.license))
    print(message)
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
