# Notipy

Monitor de batería para Linux que vigila el nivel de carga y avisa cuando conviene desconectar o conectar el cargador. Soporta alertas locales (sonido y escritorio) y remotas mediante webhook.

## Características

- Comprueba el estado de la batería a intervalos configurables
- Avisa cuando la batería supera un umbral alto estando enchufada
- Avisa cuando la batería cae por debajo de un umbral bajo sin cargador
- Reproduce sonidos opcionales con `ffplay`
- Muestra notificaciones de escritorio con `notify-send`
- Envía mensajes remotos a un webhook personalizado

## Requisitos

- Python 3.10 o superior
- Linux (para notificaciones de escritorio)
- `ffplay` (opcional, para alertas sonoras)

## Instalación

```bash
git clone https://github.com/iovanny/notipy.git
cd notipy
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuración

Copia el archivo de ejemplo y edítalo con tus valores:

```bash
cp .env.example .env
```

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `NOTIPY_CHECK_INTERVAL` | Segundos entre comprobaciones | `30` |
| `NOTIPY_HIGH_THRESHOLD` | Porcentaje para avisar de carga completa | `90` |
| `NOTIPY_LOW_THRESHOLD` | Porcentaje para avisar de batería baja | `9` |
| `NOTIPY_WEBHOOK_URL` | URL del webhook remoto | — |
| `NOTIPY_CHAT_ID` | ID del chat destino | — |
| `NOTIPY_SOUND_STARTUP` | Sonido al iniciar | — |
| `NOTIPY_SOUND_FULL` | Sonido al alcanzar carga alta | — |
| `NOTIPY_SOUND_LOW` | Sonido al detectar batería baja | — |
| `NOTIPY_DESKTOP_NOTIFICATIONS` | Activar `notify-send` | `true` |
| `NOTIPY_STARTUP_NOTIFICATION` | Notificar al arrancar | `true` |

Las variables de entorno también pueden exportarse directamente en la shell sin usar `.env`.

## Uso

```bash
python run.py
```

El monitor se ejecuta en bucle hasta que lo detengas con `Ctrl+C`.

### Ejemplo de salida

```
14:32:10 | INFO | Hora actual: 14:32:10
14:32:10 | INFO | Son más de las 14:00
14:32:40 | INFO | Batería: 87% | Cargador: conectado
14:33:10 | INFO | Batería: 91% | Cargador: conectado
14:33:10 | WARNING | Batería cargada (91%). Desconecta el cargador.
```

## Estructura del proyecto

```
notipy/
├── __init__.py
├── config.py          # Carga de configuración
├── monitor.py         # Bucle de monitoreo
└── notifications.py   # Sonido, escritorio y webhook
run.py                 # Punto de entrada
requirements.txt
.env.example
```

## Webhook remoto

Si configuras `NOTIPY_WEBHOOK_URL` y `NOTIPY_CHAT_ID`, Notipy enviará peticiones POST con este formato:

```json
{
  "chat_id": "-123456789",
  "mensaje": "La batería está cargada"
}
```

Adapta el endpoint a tu servicio de mensajería.

## Licencia

MIT
