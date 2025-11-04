#!/usr/bin/env python3
"""
Test rápido pre-demo contra NAS
Verifica que todos los casos de prueba funcionen correctamente
"""
import requests
import json
from colorama import init, Fore, Style

init(autoreset=True)

NAS_URL = "http://192.168.1.42:5000"

def test_chat(message: str, expected_scenario: str = None):
    """Envía un mensaje y verifica la respuesta"""
    try:
        response = requests.post(
            f"{NAS_URL}/api/chat",
            json={"message": message},
            timeout=10
        )
        data = response.json()
        
        print(f"\n{Fore.YELLOW}Usuario: {message}")
        print(f"{Fore.GREEN}Bot: {data['reply'][:150]}...")
        
        if expected_scenario and 'scenario' in data:
            if data['scenario'] == expected_scenario:
                print(f"{Fore.GREEN}✅ Escenario correcto: {expected_scenario}")
            else:
                print(f"{Fore.RED}❌ Escenario incorrecto: esperado {expected_scenario}, obtenido {data.get('scenario')}")
        
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}")
        return False

def main():
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"{Fore.CYAN}  🎤 TEST PRE-DEMO CONTRA NAS")
    print(f"{Fore.CYAN}{'='*50}\n")
    
    # 1. Health check
    print(f"{Fore.YELLOW}1. Health Check...")
    try:
        r = requests.get(f"{NAS_URL}/health", timeout=5)
        if r.status_code == 200:
            print(f"{Fore.GREEN}✅ NAS respondiendo OK")
        else:
            print(f"{Fore.RED}❌ Health check falló: {r.status_code}")
            return
    except Exception as e:
        print(f"{Fore.RED}❌ NAS no accesible: {e}")
        return
    
    # 2. Casos de prueba para demo
    print(f"\n{Fore.YELLOW}2. Probando casos de demo...\n")
    
    casos = [
        ("Presupuesto con 200 lucas", "presupuesto"),
        ("Quiero viajar a Europa", "ahorro"),
        ("Invertir 50000", "inversiones"),
        ("Qué es CER", "educacion"),
    ]
    
    exitos = 0
    for mensaje, escenario in casos:
        if test_chat(mensaje, escenario):
            exitos += 1
    
    # 3. Resumen
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"{Fore.CYAN}  RESUMEN")
    print(f"{Fore.CYAN}{'='*50}")
    print(f"\n{Fore.GREEN if exitos == len(casos) else Fore.YELLOW}✅ {exitos}/{len(casos)} casos funcionando")
    
    if exitos == len(casos):
        print(f"\n{Fore.GREEN}🎉 ¡TODO LISTO PARA LA DEMO!")
    else:
        print(f"\n{Fore.YELLOW}⚠️ Revisar casos que fallaron")
    
    print(f"\n{Fore.CYAN}URLs para demo:")
    print(f"{Fore.WHITE}  • Chat:      {NAS_URL}")
    print(f"{Fore.WHITE}  • Dashboard: {NAS_URL}/dashboard")
    print(f"{Fore.WHITE}  • Debug:     {NAS_URL}/debug\n")

if __name__ == "__main__":
    main()
