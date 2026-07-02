"""Bucle principal de monitoreo de batería."""

from __future__ import annotations

import datetime
import logging
import time

import psutil

from notipy.config import Settings
from notipy.notifications import (
    play_sound,
    send_desktop_notification,
    send_remote_message,
)

logger = logging.getLogger(__name__)


def _battery_state() -> tuple[float, bool] | None:
    battery = psutil.sensors_battery()
    if battery is None:
        return None
    return float(battery.percent), bool(battery.power_plugged)


def _log_status(percent: float, plugged: bool) -> None:
    status = "conectado" if plugged else "desconectado"
    logger.info("Batería: %.0f%% | Cargador: %s", percent, status)


def _handle_high_battery(settings: Settings, percent: float) -> None:
    logger.warning("Batería cargada (%.0f%%). Desconecta el cargador.", percent)
    play_sound(settings.sound_full, duration=5)
    send_remote_message(settings, "La batería está cargada")


def _handle_low_battery(settings: Settings, percent: float) -> None:
    logger.warning("Batería baja (%.0f%%). Conecta el cargador.", percent)
    play_sound(settings.sound_low, duration=25)
    if settings.enable_desktop_notifications:
        send_desktop_notification("Batería baja: conecta el cargador")
    send_remote_message(settings, "La batería se está agotando")


def run_monitor(settings: Settings) -> None:
    """Ejecuta el monitor de batería hasta que se interrumpa manualmente."""
    now = datetime.datetime.now()
    logger.info("Hora actual: %s", now.strftime("%H:%M:%S"))

    if now.hour >= 14:
        logger.info("Son más de las 14:00")
    else:
        logger.info("Antes de las 14:00")

    if settings.startup_notification and settings.enable_desktop_notifications:
        send_desktop_notification("Iniciando Notipy")

    play_sound(settings.sound_startup, duration=1)

    while True:
        time.sleep(settings.check_interval)

        state = _battery_state()
        if state is None:
            logger.error(
                "No se detectó batería en este equipo. "
                "Notipy está pensado para portátiles."
            )
            continue

        percent, plugged = state
        _log_status(percent, plugged)

        if percent > settings.high_threshold and plugged:
            _handle_high_battery(settings, percent)

        if percent < settings.low_threshold and not plugged:
            _handle_low_battery(settings, percent)
