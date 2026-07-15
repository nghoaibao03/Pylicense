from __future__ import annotations

from pathlib import Path

from client_sdk import LicenseClient


def main() -> None:
    client = LicenseClient(root=Path.cwd())
    ok, message = client.verify()
    print(message)
    if ok:
        print("Sample app is running.")
        return

    response = input("Generate activation request? [Y/N] ").strip().lower()
    if response.startswith("y"):
        request = client.create_request("DemoApp", "1.0")
        print("Activation request saved to:", client.paths.request_file)
        print(request.to_dict())


if __name__ == "__main__":
    main()
