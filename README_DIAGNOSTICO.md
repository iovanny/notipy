# Diagnóstico de Problemas de Red en Cursor (Linux)

Este script ayuda a diagnosticar problemas de conectividad de red que afectan a Cursor en Linux.

## Uso

```bash
python3 diagnostico_cursor_red.py
```

O si es ejecutable:

```bash
./diagnostico_cursor_red.py
```

## Qué verifica el script

1. **Conectividad básica a internet** - Verifica si hay conexión a internet
2. **Servidores de Cursor** - Comprueba si se puede acceder a los servidores de Cursor
3. **Configuración de proxy** - Detecta variables de proxy que pueden causar problemas
4. **Firewall** - Verifica si hay firewall activo que pueda estar bloqueando
5. **Resolución DNS** - Comprueba que los dominios se resuelvan correctamente
6. **Certificados SSL** - Verifica la validez de certificados SSL
7. **Recursos del sistema** - Revisa memoria y conexiones de red
8. **Procesos de Cursor** - Verifica si Cursor está corriendo

## Soluciones comunes

### 1. Reiniciar Cursor
```bash
pkill -f cursor && cursor
```

### 2. Limpiar caché de Cursor
```bash
rm -rf ~/.config/Cursor/Cache/*
```

### 3. Desactivar proxy temporalmente
```bash
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy
```

### 4. Verificar firewall
```bash
# Para UFW
sudo ufw status

# Para firewalld
sudo firewall-cmd --list-all
```

### 5. Cambiar DNS
```bash
# Temporalmente
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
echo "nameserver 1.1.1.1" | sudo tee -a /etc/resolv.conf
```

### 6. Reinstalar Cursor
```bash
# Dependiendo de cómo lo instalaste
sudo apt remove cursor
# Luego reinstala desde el sitio oficial
```

## Requisitos

- Python 3.6+
- Paquetes: `requests` (opcional: `psutil` para verificación de recursos)

Instalar dependencias:
```bash
pip3 install requests psutil
```

## Error específico

Si ves este error:
```
ConnectError: [unknown] Network disconnected
```

Esto generalmente indica:
- Problema de conectividad de red
- Firewall bloqueando conexiones
- Proxy mal configurado
- Problema con DNS
- Servidores de Cursor temporalmente inaccesibles

El script de diagnóstico te ayudará a identificar cuál es el problema específico.
