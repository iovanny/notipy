#!/usr/bin/env python3
"""
Script de diagnóstico para problemas de red en Cursor (Linux)
Diagnostica problemas comunes de conectividad que afectan a Cursor
"""

import subprocess
import socket
import requests
import os
import sys
import json
from urllib.parse import urlparse

# Colores para la salida
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")

def check_internet_connectivity():
    """Verifica conectividad básica a internet"""
    print_header("1. VERIFICANDO CONECTIVIDAD BÁSICA A INTERNET")
    
    # Verificar conectividad con ping a DNS públicos
    dns_servers = ['8.8.8.8', '1.1.1.1', '208.67.222.222']
    internet_ok = False
    
    for dns in dns_servers:
        try:
            result = subprocess.run(
                ['ping', '-c', '2', '-W', '2', dns],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                print_success(f"Conectividad a {dns} OK")
                internet_ok = True
                break
        except Exception as e:
            continue
    
    if not internet_ok:
        print_error("No hay conectividad básica a internet")
        return False
    
    # Verificar resolución DNS
    try:
        socket.gethostbyname('google.com')
        print_success("Resolución DNS funcionando")
    except socket.gaierror:
        print_error("Problema con resolución DNS")
        return False
    
    return True

def check_cursor_servers():
    """Verifica conectividad a servidores de Cursor"""
    print_header("2. VERIFICANDO CONECTIVIDAD A SERVIDORES DE CURSOR")
    
    # URLs comunes de servicios de Cursor
    cursor_urls = [
        'https://www.cursor.com',
        'https://api.cursor.com',
        'https://cursor.sh',
    ]
    
    results = {}
    
    for url in cursor_urls:
        try:
            response = requests.get(url, timeout=10, allow_redirects=True)
            if response.status_code in [200, 301, 302]:
                print_success(f"{url} - Accesible (Status: {response.status_code})")
                results[url] = True
            else:
                print_warning(f"{url} - Status: {response.status_code}")
                results[url] = False
        except requests.exceptions.Timeout:
            print_error(f"{url} - Timeout")
            results[url] = False
        except requests.exceptions.ConnectionError as e:
            print_error(f"{url} - Error de conexión: {str(e)}")
            results[url] = False
        except Exception as e:
            print_error(f"{url} - Error: {str(e)}")
            results[url] = False
    
    return any(results.values())

def check_proxy_settings():
    """Verifica configuración de proxy"""
    print_header("3. VERIFICANDO CONFIGURACIÓN DE PROXY")
    
    proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 
                  'NO_PROXY', 'no_proxy', 'ALL_PROXY', 'all_proxy']
    
    proxies_found = False
    
    for var in proxy_vars:
        value = os.environ.get(var)
        if value:
            print_info(f"{var} = {value}")
            proxies_found = True
    
    if not proxies_found:
        print_success("No hay variables de proxy configuradas")
    else:
        print_warning("Se encontraron variables de proxy. Esto puede causar problemas.")
        print_info("Solución: Desactiva temporalmente el proxy o configura Cursor para usarlo")
    
    return proxies_found

def check_firewall():
    """Verifica si hay firewall activo"""
    print_header("4. VERIFICANDO FIREWALL")
    
    firewall_commands = [
        ('ufw', ['ufw', 'status']),
        ('firewalld', ['firewall-cmd', '--state']),
        ('iptables', ['iptables', '-L', '-n']),
    ]
    
    firewall_active = False
    
    for name, cmd in firewall_commands:
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=3)
            if result.returncode == 0:
                output = result.stdout.decode().lower()
                if 'active' in output or 'running' in output or len(output) > 100:
                    print_warning(f"Firewall {name} parece estar activo")
                    firewall_active = True
        except FileNotFoundError:
            continue
        except Exception:
            continue
    
    if not firewall_active:
        print_success("No se detectó firewall activo (o no está bloqueando)")
    
    return firewall_active

def check_dns_resolution():
    """Verifica resolución DNS específica"""
    print_header("5. VERIFICANDO RESOLUCIÓN DNS")
    
    test_domains = [
        'cursor.com',
        'api.cursor.com',
        'cursor.sh',
        'google.com',  # Control
    ]
    
    dns_ok = True
    
    for domain in test_domains:
        try:
            ip = socket.gethostbyname(domain)
            print_success(f"{domain} -> {ip}")
        except socket.gaierror as e:
            print_error(f"{domain} - No se pudo resolver: {e}")
            dns_ok = False
    
    return dns_ok

def check_ssl_certificates():
    """Verifica certificados SSL"""
    print_header("6. VERIFICANDO CERTIFICADOS SSL")
    
    try:
        import ssl
        import urllib.request
        
        url = 'https://www.cursor.com'
        context = ssl.create_default_context()
        
        with urllib.request.urlopen(url, timeout=10, context=context) as response:
            print_success("Certificados SSL válidos")
            return True
    except ssl.SSLError as e:
        print_error(f"Error de certificado SSL: {e}")
        return False
    except Exception as e:
        print_warning(f"No se pudo verificar SSL: {e}")
        return True  # No es crítico

def check_system_resources():
    """Verifica recursos del sistema"""
    print_header("7. VERIFICANDO RECURSOS DEL SISTEMA")
    
    try:
        import psutil
        
        # Memoria
        memory = psutil.virtual_memory()
        if memory.percent > 90:
            print_warning(f"Memoria alta: {memory.percent}%")
        else:
            print_success(f"Memoria: {memory.percent}%")
        
        # Conexiones de red
        connections = psutil.net_connections()
        print_info(f"Conexiones de red activas: {len(connections)}")
        
    except ImportError:
        print_warning("psutil no está instalado, omitiendo verificación de recursos")
    except Exception as e:
        print_warning(f"Error al verificar recursos: {e}")

def check_cursor_process():
    """Verifica si Cursor está corriendo"""
    print_header("8. VERIFICANDO PROCESOS DE CURSOR")
    
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'cursor'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            print_info(f"Procesos de Cursor encontrados: {len(pids)}")
            for pid in pids:
                if pid:
                    print_info(f"  PID: {pid}")
        else:
            print_warning("No se encontraron procesos de Cursor corriendo")
    except Exception as e:
        print_warning(f"No se pudo verificar procesos: {e}")

def provide_solutions():
    """Proporciona soluciones comunes"""
    print_header("SOLUCIONES RECOMENDADAS")
    
    solutions = [
        {
            'title': '1. Reiniciar Cursor',
            'description': 'Cierra completamente Cursor y vuelve a abrirlo',
            'command': 'pkill -f cursor && cursor'
        },
        {
            'title': '2. Verificar conexión a internet',
            'description': 'Asegúrate de que tu conexión a internet funciona correctamente',
            'command': 'ping -c 3 8.8.8.8'
        },
        {
            'title': '3. Limpiar caché de Cursor',
            'description': 'Elimina el caché de Cursor (puede contener datos corruptos)',
            'command': 'rm -rf ~/.config/Cursor/Cache/*'
        },
        {
            'title': '4. Desactivar proxy temporalmente',
            'description': 'Si usas proxy, desactívalo temporalmente para probar',
            'command': 'unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy'
        },
        {
            'title': '5. Verificar firewall',
            'description': 'Asegúrate de que el firewall no está bloqueando Cursor',
            'command': 'sudo ufw status  # o firewall-cmd --list-all'
        },
        {
            'title': '6. Actualizar Cursor',
            'description': 'Asegúrate de tener la última versión de Cursor',
            'command': 'cursor --version'
        },
        {
            'title': '7. Verificar DNS',
            'description': 'Prueba cambiar a DNS públicos (Google: 8.8.8.8, Cloudflare: 1.1.1.1)',
            'command': 'echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf'
        },
        {
            'title': '8. Reinstalar Cursor',
            'description': 'Como último recurso, reinstala Cursor completamente',
            'command': 'sudo apt remove cursor && sudo apt install cursor'
        }
    ]
    
    for sol in solutions:
        print(f"\n{Colors.BOLD}{sol['title']}{Colors.RESET}")
        print(f"  {sol['description']}")
        print(f"  {Colors.YELLOW}Comando: {sol['command']}{Colors.RESET}")

def main():
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   DIAGNÓSTICO DE RED PARA CURSOR (LINUX)                ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")
    
    results = {}
    
    # Ejecutar todas las verificaciones
    results['internet'] = check_internet_connectivity()
    results['cursor_servers'] = check_cursor_servers()
    results['proxy'] = check_proxy_settings()
    results['firewall'] = check_firewall()
    results['dns'] = check_dns_resolution()
    results['ssl'] = check_ssl_certificates()
    check_system_resources()
    check_cursor_process()
    
    # Resumen
    print_header("RESUMEN DEL DIAGNÓSTICO")
    
    critical_issues = []
    
    if not results.get('internet', False):
        critical_issues.append("No hay conectividad básica a internet")
    
    if not results.get('cursor_servers', False):
        critical_issues.append("No se puede acceder a los servidores de Cursor")
    
    if not results.get('dns', True):
        critical_issues.append("Problemas con resolución DNS")
    
    if results.get('proxy', False):
        print_warning("Proxy configurado - puede causar problemas")
    
    if results.get('firewall', False):
        print_warning("Firewall activo - puede estar bloqueando conexiones")
    
    if critical_issues:
        print_error("\nPROBLEMAS CRÍTICOS ENCONTRADOS:")
        for issue in critical_issues:
            print_error(f"  • {issue}")
    else:
        print_success("\nNo se encontraron problemas críticos de conectividad")
        print_info("El problema puede ser específico de la aplicación Cursor")
    
    # Mostrar soluciones
    provide_solutions()
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}Diagnóstico completado{Colors.RESET}\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDiagnóstico interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        sys.exit(1)
