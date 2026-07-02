"""Carga de configuración desde variables de entorno."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv() -> None:
    """Carga un archivo .env en el directorio de trabajo si existe."""
    env_path = Path(".env")
    if not env_path.is_file():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


@dataclass(frozen=True)
class Settings:
    """Parámetros de ejecución del monitor."""

    check_interval: int
    high_threshold: float
    low_threshold: float
    webhook_url: str | None
    chat_id: str | None
    sound_startup: Path | None
    sound_full: Path | None
    sound_low: Path | None
    enable_desktop_notifications: bool
    startup_notification: bool

    @classmethod
    def from_env(cls) -> Settings:
        _load_dotenv()

        def optional_path(name: str) -> Path | None:
            value = os.getenv(name, "").strip()
            return Path(value).expanduser() if value else None

        return cls(
            check_interval=int(os.getenv("NOTIPY_CHECK_INTERVAL", "30")),
            high_threshold=float(os.getenv("NOTIPY_HIGH_THRESHOLD", "90")),
            low_threshold=float(os.getenv("NOTIPY_LOW_THRESHOLD", "9")),
            webhook_url=os.getenv("NOTIPY_WEBHOOK_URL") or None,
            chat_id=os.getenv("NOTIPY_CHAT_ID") or None,
            sound_startup=optional_path("NOTIPY_SOUND_STARTUP"),
            sound_full=optional_path("NOTIPY_SOUND_FULL"),
            sound_low=optional_path("NOTIPY_SOUND_LOW"),
            enable_desktop_notifications=os.getenv(
                "NOTIPY_DESKTOP_NOTIFICATIONS", "true"
            ).lower()
            in ("1", "true", "yes", "on"),
            startup_notification=os.getenv(
                "NOTIPY_STARTUP_NOTIFICATION", "true"
            ).lower()
            in ("1", "true", "yes", "on"),
        )
