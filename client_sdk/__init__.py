from __future__ import annotations

from pathlib import Path

_PACKAGE_ROOT = Path(__file__).resolve().parent
_SOURCE_PACKAGE = _PACKAGE_ROOT.parent / "src" / "client_sdk"

__path__ = [str(_PACKAGE_ROOT), str(_SOURCE_PACKAGE)]

from .sdk import LicenseClient

__all__ = ["LicenseClient"]
