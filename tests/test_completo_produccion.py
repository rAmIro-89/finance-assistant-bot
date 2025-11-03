#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Completo de Producción - Todas las conversaciones
Valida que el bot entienda correctamente cada escenario
"""

import requests
import os
import time
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

BASE_URL = os.getenv("BASE_URL", "http://192.168.1.42:5000").rstrip("/")

class BotTester:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.session_id = f"test_{datetime.now().strftime('%H%M%S')}"
        # Mantener cookies (uid) entre requests para preservar contexto conversacional
        self.session = requests.Session()
    
    def send_message(self, text, expected_scenario=None):
        """Envía mensaje al bot y verifica respuesta"""
        print(f"\n{Fore.CYAN}📤 Usuario: {text}")
        
        try:
            response = self.session.post(
                f"{BASE_URL}/api/chat",
                json={"message": text, "user_id": self.session_id},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                scenario = data.get('scenario', 'unknown')
                reply = data.get('reply', '')
                
                print(f"{Fore.YELLOW}🤖 Escenario detectado: {scenario}")
                print(f"{Fore.GREEN}💬 Bot: {reply[:150]}..." if len(reply) > 150 else f"{Fore.GREEN}💬 Bot: {reply}")
                
                # Verificar si el escenario es el esperado
                if expected_scenario:
                    if scenario == expected_scenario:
                        print(f"{Fore.GREEN}✅ CORRECTO: Detectó {expected_scenario}")
                        self.tests_passed += 1
                        return True
                    else:
                        print(f"{Fore.RED}❌ ERROR: Esperaba {expected_scenario}, obtuvo {scenario}")
                        self.tests_failed += 1
                        return False
                
                return True
            else:
                print(f"{Fore.RED}❌ Error HTTP: {response.status_code}")
                self.tests_failed += 1
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {e}")
            self.tests_failed += 1
            return False
    
    def test_presupuesto(self):
        """Test del flujo de presupuesto"""
        print(f"\n{'='*70}")
        print(f"{Fore.MAGENTA}🧪 TEST 1: PRESUPUESTO")
        print(f"{'='*70}")
        
        # Variaciones de mensajes
        tests = [
            ("necesito organizar mis gastos", "presupuesto"),
            ("cuanto puedo gastar con mi sueldo", "presupuesto"),
            ("mi ingreso mensual es 150000", "presupuesto"),
            ("gano 80000 por mes", "presupuesto"),
            ("como distribuir mi plata", "presupuesto"),
        ]
        
        for msg, expected in tests:
            self.send_message(msg, expected)
            time.sleep(1)
    
    def test_ahorro(self):
        """Test del flujo de ahorro con contexto"""
        print(f"\n{'='*70}")
        print(f"{Fore.MAGENTA}🧪 TEST 2: AHORRO (con contexto)")
        print(f"{'='*70}")
        
        # Flujo completo
        print(f"\n{Fore.BLUE}--- Flujo 1: Casa ---")
        self.send_message("quiero ahorrar", "ahorro")
        time.sleep(1)
        self.send_message("casa", "ahorro")  # Meta de una palabra
        time.sleep(1)
        self.send_message("800000", "ahorro")  # Monto
        time.sleep(1)
        self.send_message("24 meses", "ahorro")  # Plazo
        time.sleep(2)
        
        # Flujo 2: Auto
        print(f"\n{Fore.BLUE}--- Flujo 2: Auto ---")
        self.send_message("necesito juntar plata", "ahorro")
        time.sleep(1)
        self.send_message("auto", "ahorro")
        time.sleep(1)
        self.send_message("300000", "ahorro")
        time.sleep(2)
        
        # Flujo 3: Viaje
        print(f"\n{Fore.BLUE}--- Flujo 3: Viaje ---")
        self.send_message("quiero viajar a europa", "ahorro")
        time.sleep(1)
        self.send_message("500000", "ahorro")
        time.sleep(2)
        
        # Frases alternativas
        print(f"\n{Fore.BLUE}--- Variaciones ---")
        tests = [
            ("como puedo ahorrar mejor", "ahorro"),
            ("guardar dinero para emergencia", "ahorro"),
            ("planear compra de moto", "ahorro"),
        ]
        for msg, expected in tests:
            self.send_message(msg, expected)
            time.sleep(1)
    
    def test_inversiones_activos(self):
        """Test de inversiones con activos específicos"""
        print(f"\n{'='*70}")
        print(f"{Fore.MAGENTA}🧪 TEST 3: INVERSIONES - Activos Específicos")
        print(f"{'='*70}")
        
        tests = [
            ("quiero invertir en oro", "inversiones"),
            ("conviene comprar plata", "inversiones"),
            ("dolar como inversion", "inversiones"),
            ("bitcoin es seguro", "inversiones"),
            ("comprar acciones de apple", "inversiones"),
            ("plazo fijo o algo mejor", "inversiones"),
            ("cripto para principiantes", "inversiones"),
            ("cedear de tesla", "inversiones"),
            ("aguinaldo donde invertir", "inversiones"),
        ]
        
        for msg, expected in tests:
            self.send_message(msg, expected)
            time.sleep(1.5)
    
    def test_inversiones_generales(self):
        """Test de inversiones generales"""
        print(f"\n{'='*70}")
        print(f"{Fore.MAGENTA}🧪 TEST 4: INVERSIONES - Consultas Generales")
        print(f"{'='*70}")
        
        tests = [
            ("donde puedo invertir 100000", "inversiones"),
            ("soy principiante en inversiones", "inversiones"),
            ("quiero algo seguro para invertir", "inversiones"),
            ("tengo 50000 que hago", "inversiones"),
            ("invertir a largo plazo", "inversiones"),
        ]
        
        for msg, expected in tests:
            self.send_message(msg, expected)
            time.sleep(1)
    
    def test_deudas(self):
        """Test del flujo de deudas"""
        print(f"\n{'='*70}")
        print(f"{Fore.MAGENTA}🧪 TEST 5: DEUDAS")
        print(f"{'='*70}")
        
        tests = [
            ("tengo una deuda de 200000", "deudas"),
            ("debo plata en la tarjeta", "deudas"),
            ("no puedo pagar el prestamo", "deudas"),
            ("me atrase con las cuotas", "deudas"),
            ("como salir de deudas", "deudas"),
            ("refinanciar credito", "deudas"),
        ]
        
        for msg, expected in tests:
            self.send_message(msg, expected)
            time.sleep(1)
    
    def test_educacion(self):
        """Test de educación financiera"""
        print(f"\n{'='*70}")
        print(f"{Fore.MAGENTA}🧪 TEST 6: EDUCACIÓN")
        print(f"{'='*70}")
        
        tests = [
            ("que es inflacion", "educacion"),
            ("explicame que son los bonos", "educacion"),
            ("como funciona el plazo fijo", "educacion"),
            ("que significa TNA", "educacion"),
            ("aprender sobre inversiones", "educacion"),
            ("no entiendo que es un CEDEAR", "educacion"),
        ]
        
        for msg, expected in tests:
            self.send_message(msg, expected)
            time.sleep(1)
    
    def test_calculadora(self):
        """Test de calculadora financiera"""
        print(f"\n{'='*70}")
        print(f"{Fore.MAGENTA}🧪 TEST 7: CALCULADORA")
        print(f"{'='*70}")
        
        tests = [
            ("calcular interes compuesto", "calculadora"),
            ("cuanto ganaria invirtiendo 100000", "calculadora"),
            ("simular prestamo de 50000", "calculadora"),
            ("comparar opciones de inversion", "calculadora"),
        ]
        
        for msg, expected in tests:
            self.send_message(msg, expected)
            time.sleep(1)
    
    def test_casos_complejos(self):
        """Test de casos complejos y edge cases"""
        print(f"\n{'='*70}")
        print(f"{Fore.MAGENTA}🧪 TEST 8: CASOS COMPLEJOS")
        print(f"{'='*70}")
        
        # Mensajes ambiguos o con múltiples intenciones
        tests = [
            ("tengo deuda pero quiero invertir", None),  # Sin expectativa específica
            ("oro vs plata cual conviene", "inversiones"),
            ("puedo ahorrar y pagar deuda al mismo tiempo", None),
            ("presupuesto para ahorrar 50000", None),
        ]
        
        for msg, expected in tests:
            self.send_message(msg, expected)
            time.sleep(1)
    
    def test_contexto_numeros(self):
        """Test específico de contexto con números sueltos"""
        print(f"\n{'='*70}")
        print(f"{Fore.MAGENTA}🧪 TEST 9: CONTEXTO - Números Sueltos")
        print(f"{'='*70}")
        
        print(f"\n{Fore.BLUE}--- Contexto Presupuesto ---")
        self.send_message("hacer presupuesto", "presupuesto")
        time.sleep(1)
        self.send_message("120000", "presupuesto")
        time.sleep(2)
        
        print(f"\n{Fore.BLUE}--- Contexto Deudas ---")
        self.send_message("pagar deuda", "deudas")
        time.sleep(1)
        self.send_message("85000", "deudas")
        time.sleep(2)
    
    def test_respuestas_cortas(self):
        """Test de respuestas cortas de continuación"""
        print(f"\n{'='*70}")
        print(f"{Fore.MAGENTA}🧪 TEST 10: RESPUESTAS CORTAS")
        print(f"{'='*70}")
        
        print(f"\n{Fore.BLUE}--- Confirmaciones ---")
        self.send_message("quiero invertir 50000", "inversiones")
        time.sleep(1)
        self.send_message("si", "inversiones")  # Debe mantener contexto
        time.sleep(1)
        self.send_message("dale", "inversiones")
        time.sleep(2)
    
    def print_summary(self):
        """Muestra resumen de resultados"""
        print(f"\n{'='*70}")
        print(f"{Fore.CYAN}📊 RESUMEN DE PRUEBAS")
        print(f"{'='*70}")
        
        total = self.tests_passed + self.tests_failed
        percentage = (self.tests_passed / total * 100) if total > 0 else 0
        
        print(f"{Fore.GREEN}✅ Pruebas exitosas: {self.tests_passed}")
        print(f"{Fore.RED}❌ Pruebas fallidas: {self.tests_failed}")
        print(f"{Fore.YELLOW}📈 Total: {total}")
        print(f"{Fore.CYAN}🎯 Tasa de éxito: {percentage:.1f}%")
        
        if percentage >= 90:
            print(f"\n{Fore.GREEN}🎉 EXCELENTE! El bot está funcionando muy bien")
        elif percentage >= 75:
            print(f"\n{Fore.YELLOW}✅ BIEN! Hay algunos casos a revisar")
        else:
            print(f"\n{Fore.RED}⚠️  REQUIERE ATENCIÓN! Varios casos fallando")
        
        print(f"\n{Fore.CYAN}Ver logs detallados en: http://192.168.1.42:5000/logs")
        print(f"{'='*70}\n")

def main():
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}🤖 TEST COMPLETO DE PRODUCCIÓN - CHATBOT FINANCIERO")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    tester = BotTester()
    
    try:
        # Verificar conexión
        print(f"{Fore.YELLOW}🔍 Verificando conexión con el servidor...")
        response = requests.get(f"{BASE_URL}/debug", timeout=5)
        if response.status_code == 200:
            print(f"{Fore.GREEN}✅ Servidor en línea: {BASE_URL}\n")
        else:
            print(f"{Fore.RED}❌ Servidor no responde correctamente")
            return
    except Exception as e:
        print(f"{Fore.RED}❌ No se puede conectar al servidor: {e}")
        return
    
    # Ejecutar todos los tests
    tester.test_presupuesto()
    tester.test_ahorro()
    tester.test_inversiones_activos()
    tester.test_inversiones_generales()
    tester.test_deudas()
    tester.test_educacion()
    tester.test_calculadora()
    tester.test_contexto_numeros()
    tester.test_respuestas_cortas()
    tester.test_casos_complejos()
    
    # Resumen final
    tester.print_summary()
    
    print(f"{Fore.CYAN}💡 TIP: Revisa el endpoint /logs para ver el análisis completo")
    print(f"{Fore.CYAN}   URL: http://192.168.1.42:5000/logs\n")

if __name__ == "__main__":
    main()
