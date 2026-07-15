from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pylicense.client import ClientPaths, create_activation_request, verify_license


@dataclass(slots=True)
class LicenseClient:
    root: Path

    @property
    def paths(self) -> ClientPaths:
        return ClientPaths(root=self.root)

    def create_request(self, product: str, version: str):
        return create_activation_request(self.paths, product, version)

    def verify(self, license_path: Path | None = None) -> tuple[bool, str]:
        return verify_license(self.paths, license_path)
