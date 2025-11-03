#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar normalización de texto y detección de intención
"""

from chatbot_core import ChatBot, normalize_text
from datetime import datetime

def test_normalizacion():
    """Prueba la función normalize_text"""
    print("=" * 60)
    print("🧪 TEST DE NORMALIZACIÓN")
    print("=" * 60)
    
    casos = [
        "Inversión",
        "quiero_ahorrar",
        "plazo-fijo",
        "DÓLAR",
        "Año",
        "casa   auto",
        "Ñoño",
        "café",
        "CRÉDITO",
        "Educación_Financiera"
    ]
    
    for texto in casos:
        normalizado = normalize_text(texto)
        print(f"{texto:25s} → {normalizado}")
    print()

def test_deteccion_contexto():
    """Prueba detección de intención con contexto"""
    print("=" * 60)
    print("🧪 TEST DE DETECCIÓN CON CONTEXTO")
    print("=" * 60)
    
    bot = ChatBot()
    dt = datetime.now()
    
    # CASO 1: Ahorro → casa → 500000
    print("\n📝 CASO 1: Ahorro con meta de una palabra")
    print("-" * 60)
    
    msg1 = "quiero ahorrar"
    scenario1 = bot.detect(msg1)
    print(f"User: {msg1}")
    print(f"Escenario detectado: {scenario1}")
    bot.reply(msg1, dt)
    
    msg2 = "casa"
    scenario2 = bot.detect(msg2)
    print(f"\nUser: {msg2}")
    print(f"Escenario detectado: {scenario2}")
    print(f"Estado: waiting_for={bot.conversation_state.get('waiting_for')}")
    bot.reply(msg2, dt)
    
    msg3 = "500000"
    scenario3 = bot.detect(msg3)
    print(f"\nUser: {msg3}")
    print(f"Escenario detectado: {scenario3}")
    print(f"Estado: waiting_for={bot.conversation_state.get('waiting_for')}")
    bot.reply(msg3, dt)
    
    # CASO 2: Presupuesto → 80000
    print("\n\n📝 CASO 2: Presupuesto con ingreso")
    print("-" * 60)
    
    bot2 = ChatBot()
    
    msg1 = "quiero hacer un presupuesto"
    scenario1 = bot2.detect(msg1)
    print(f"User: {msg1}")
    print(f"Escenario detectado: {scenario1}")
    bot2.reply(msg1, dt)
    
    msg2 = "80000"
    scenario2 = bot2.detect(msg2)
    print(f"\nUser: {msg2}")
    print(f"Escenario detectado: {scenario2}")
    
    # CASO 3: Inversiones con activos específicos
    print("\n\n📝 CASO 3: Inversiones - Activos específicos")
    print("-" * 60)
    
    bot3 = ChatBot()
    
    activos = [
        "quiero invertir en oro",
        "Oro cómo inversión",
        "plazo_fijo conviene?",
        "invertir en DÓLAR",
        "Bitcoin es seguro?"
    ]
    
    for msg in activos:
        scenario = bot3.detect(msg)
        print(f"User: {msg:30s} → Escenario: {scenario}")

def test_keywords_directos():
    """Prueba mapeo directo de keywords"""
    print("\n\n" + "=" * 60)
    print("🧪 TEST DE KEYWORDS DIRECTOS (direct_map)")
    print("=" * 60)
    
    bot = ChatBot()
    
    casos = [
        ("oro", "inversiones"),
        ("plata", "inversiones"),
        ("dolar", "inversiones"),
        ("bitcoin", "inversiones"),
        ("aguinaldo", "inversiones"),
        ("plazo fijo", "inversiones"),
        ("presupuesto", "presupuesto"),
        ("ahorrar", "ahorro"),
        ("deuda", "deudas"),
        ("que es inflacion", "educacion"),
    ]
    
    for texto, esperado in casos:
        detectado = bot.detect(texto)
        status = "✅" if detectado == esperado else "❌"
        print(f"{status} '{texto:20s}' → Esperado: {esperado:12s} | Detectado: {detectado}")

if __name__ == "__main__":
    test_normalizacion()
    test_deteccion_contexto()
    test_keywords_directos()
    
    print("\n" + "=" * 60)
    print("✅ TESTS COMPLETADOS")
    print("=" * 60)
