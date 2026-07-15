from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

from . import crypto, models, storage


@dataclass(slots=True)
class ServerPaths:
    root: Path

    @property
    def requests_dir(self) -> Path:
        return self.root / "requests"

    @property
    def licenses_dir(self) -> Path:
        return self.root / "licenses"

    @property
    def private_key(self) -> Path:
        return self.root / "keys" / "private.pem"

    def license_path(self, request_path: Path) -> Path:
        return self.licenses_dir / "license.dat"


def issue_license(
    paths: ServerPaths,
    request_path: Path,
    customer: str,
    expire: str,
    edition: str,
    features: list[str],
) -> models.SignedLicense:
    request = models.ActivationRequest.from_dict(storage.read_json(request_path))
    private_key = crypto.load_private_key(paths.private_key)

    payload = models.LicensePayload(
        customer=customer,
        product=request.product,
        version=request.version,
        expire=expire,
        edition=edition,
        hwid=request.hwid,
        feature=features,
    )
    signature = crypto.sign_payload(private_key, payload.to_dict())
    signed_license = models.SignedLicense(payload=payload, signature=signature)
    storage.write_json(paths.license_path(request_path), signed_license.to_dict())
    return signed_license


def parse_expire_or_default(expire: str | None) -> str:
    if expire:
        return expire
    return date(date.today().year + 2, 12, 31).isoformat()
