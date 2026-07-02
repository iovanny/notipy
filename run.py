#!/usr/bin/env python3
"""Punto de entrada para el monitor de batería Notipy."""

from __future__ import annotations

import logging
import sys

from notipy.config import Settings
from notipy.monitor import run_monitor


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    settings = Settings.from_env()

    try:
        run_monitor(settings)
    except KeyboardInterrupt:
        logging.info("Monitor detenido por el usuario")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
