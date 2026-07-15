from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

from . import crypto, hwid, models, state_db, storage


DEFAULT_APP_NAME = "DemoApp"
DEFAULT_APP_VERSION = "1.0"


@dataclass(slots=True)
class ClientPaths:
    root: Path

    @property
    def requests_dir(self) -> Path:
        return self.root / "requests"

    @property
    def licenses_dir(self) -> Path:
        return self.root / "licenses"

    @property
    def state_dir(self) -> Path:
        return self.root / ".pylicense"

    @property
    def public_key(self) -> Path:
        return self.root / "keys" / "public.pem"

    @property
    def request_file(self) -> Path:
        return self.requests_dir / "request.json"

    @property
    def license_file(self) -> Path:
        return self.licenses_dir / "license.dat"

    @property
    def trial_file(self) -> Path:
        return self.state_dir / "trial.json"

    @property
    def trial_db(self) -> Path:
        return self.state_dir / "state.db"


def create_activation_request(paths: ClientPaths, product: str, version: str) -> models.ActivationRequest:
    request = models.ActivationRequest(product=product, version=version, hwid=hwid.get_hwid())
    storage.write_json(paths.request_file, request.to_dict())
    return request


def load_activation_request(path: Path) -> models.ActivationRequest:
    return models.ActivationRequest.from_dict(storage.read_json(path))


def load_signed_license(path: Path) -> models.SignedLicense:
    return models.SignedLicense.from_dict(storage.read_json(path))


def load_legacy_trial_state(path: Path) -> models.TrialState:
    return models.TrialState.from_dict(storage.read_json(path))


def create_trial_state(paths: ClientPaths, duration_days: int = 30) -> models.TrialState:
    state = models.TrialState(started_on=date.today().isoformat(), hwid=hwid.get_hwid(), duration_days=duration_days)
    state_db.save_trial_state(paths.trial_db, state)
    return state


def verify_trial(paths: ClientPaths) -> tuple[bool, str]:
    trial = state_db.load_trial_state(paths.trial_db)
    if trial is None and paths.trial_file.exists():
        trial = load_legacy_trial_state(paths.trial_file)
        state_db.save_trial_state(paths.trial_db, trial)

    if trial is None:
        state = create_trial_state(paths)
        remaining_days = max(0, (state.expires_on() - date.today()).days)
        return True, f"Trial started. {remaining_days} days remaining."

    if trial.hwid != hwid.get_hwid():
        return False, "Trial HWID mismatch."

    remaining_days = (trial.expires_on() - date.today()).days
    if remaining_days < 0:
        return False, "Trial expired."

    return True, f"Trial active. {remaining_days} days remaining."


def verify_license(paths: ClientPaths, license_path: Path | None = None) -> tuple[bool, str]:
    target = license_path or paths.license_file
    if not target.exists():
        return verify_trial(paths)

    signed_license = load_signed_license(target)
    payload = signed_license.payload

    if not paths.public_key.exists():
        return False, "Public key not found."

    public_key = crypto.load_public_key(paths.public_key)
    if not crypto.verify_payload_signature(public_key, payload.to_dict(), signed_license.signature):
        return False, "Verify Signature failed."

    current_hwid = hwid.get_hwid()
    if payload.hwid != current_hwid:
        return False, "Verify HWID failed."

    if payload.expires_on() < date.today():
        return False, "Verify Expire failed."

    return True, "License OK"
