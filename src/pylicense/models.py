from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any


@dataclass(slots=True)
class ActivationRequest:
    product: str
    version: str
    hwid: str

    def to_dict(self) -> dict[str, str]:
        return {
            "product": self.product,
            "version": self.version,
            "hwid": self.hwid,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ActivationRequest":
        return cls(
            product=str(data["product"]),
            version=str(data["version"]),
            hwid=str(data["hwid"]),
        )


@dataclass(slots=True)
class LicensePayload:
    customer: str
    product: str
    version: str
    expire: str
    edition: str
    hwid: str
    feature: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer": self.customer,
            "product": self.product,
            "version": self.version,
            "expire": self.expire,
            "edition": self.edition,
            "hwid": self.hwid,
            "feature": list(self.feature),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LicensePayload":
        features = data.get("feature", [])
        return cls(
            customer=str(data["customer"]),
            product=str(data["product"]),
            version=str(data["version"]),
            expire=str(data["expire"]),
            edition=str(data["edition"]),
            hwid=str(data["hwid"]),
            feature=[str(item) for item in features],
        )

    def expires_on(self) -> date:
        return date.fromisoformat(self.expire)


@dataclass(slots=True)
class SignedLicense:
    payload: LicensePayload
    signature: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "payload": self.payload.to_dict(),
            "signature": self.signature,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SignedLicense":
        return cls(
            payload=LicensePayload.from_dict(data["payload"]),
            signature=str(data["signature"]),
        )


@dataclass(slots=True)
class TrialState:
    started_on: str
    hwid: str
    duration_days: int = 30

    def to_dict(self) -> dict[str, Any]:
        return {
            "started_on": self.started_on,
            "hwid": self.hwid,
            "duration_days": self.duration_days,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TrialState":
        return cls(
            started_on=str(data["started_on"]),
            hwid=str(data["hwid"]),
            duration_days=int(data.get("duration_days", 30)),
        )

    def expires_on(self) -> date:
        return date.fromisoformat(self.started_on) + timedelta(days=self.duration_days)
