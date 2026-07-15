from __future__ import annotations

from pathlib import Path

from pylicense.crypto import generate_key_pair


def main() -> None:
    root = Path.cwd()
    private_path = root / "keys" / "private.pem"
    public_path = root / "keys" / "public.pem"
    generate_key_pair(private_path, public_path)
    print(f"Private key written to {private_path}")
    print(f"Public key written to {public_path}")


if __name__ == "__main__":
    main()
