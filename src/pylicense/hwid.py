from __future__ import annotations

import hashlib
import platform
import subprocess
from functools import lru_cache


def _run_command(command: str) -> str:
    try:
        result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.DEVNULL)
    except Exception:
        return ""
    return result.strip()


def _wmic_value(command: str) -> str:
    output = _run_command(command)
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if len(lines) <= 1:
        return ""
    return lines[-1]


def _fallback_parts() -> list[str]:
    return [
        platform.node(),
        platform.platform(),
        platform.machine(),
        platform.processor(),
    ]


@lru_cache(maxsize=1)
def get_hwid() -> str:
    if platform.system().lower() == "windows":
        parts = [
            _wmic_value("wmic cpu get ProcessorId"),
            _wmic_value("wmic csproduct get UUID"),
            _wmic_value("wmic bios get serialnumber"),
            _wmic_value("wmic diskdrive get serialnumber"),
        ]
    else:
        parts = []

    parts.extend(_fallback_parts())
    fingerprint = "|".join(part for part in parts if part)
    return hashlib.sha256(fingerprint.encode("utf-8")).hexdigest().upper()
