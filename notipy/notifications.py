"""Alertas locales (sonido y escritorio) y remotas (webhook)."""

from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path

import requests

from notipy.config import Settings

logger = logging.getLogger(__name__)


def play_sound(path: Path | None, duration: int = 5) -> None:
    """Reproduce un archivo de audio con ffplay si está disponible."""
    if path is None:
        return
    if not path.is_file():
        logger.warning("Archivo de sonido no encontrado: %s", path)
        return
    if shutil.which("ffplay") is None:
        logger.warning("ffplay no está instalado; no se reproducirá %s", path)
        return

    subprocess.run(
        [
            "ffplay",
            "-nodisp",
            "-t",
            str(duration),
            "-autoexit",
            str(path),
        ],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def send_desktop_notification(title: str, icon: str = "battery-caution") -> None:
    """Muestra una notificación de escritorio en entornos compatibles con notify-send."""
    if shutil.which("notify-send") is None:
        logger.debug("notify-send no disponible; se omite la notificación de escritorio")
        return

    subprocess.run(
        ["notify-send", title, f"--icon={icon}"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def send_remote_message(settings: Settings, message: str) -> None:
    """Envía un mensaje al webhook configurado."""
    if not settings.webhook_url or not settings.chat_id:
        logger.debug("Webhook o chat_id no configurados; se omite el envío remoto")
        return

    try:
        response = requests.post(
            settings.webhook_url,
            json={"chat_id": settings.chat_id, "mensaje": message},
            timeout=10,
        )
        response.raise_for_status()
        logger.info("Mensaje remoto enviado correctamente")
    except requests.RequestException as exc:
        logger.error("No se pudo enviar el mensaje remoto: %s", exc)
