# 🎤 Guía de Demostración del Bot Financiero

## ⏱️ Demo de 5 minutos

### 1️⃣ Abrir Chat Web en NAS - PRODUCCIÓN (30 seg)
```
http://192.168.1.42:5000
```
**💡 Ventaja:** Demostrar que está corriendo 24/7 en producción real, no solo local

### 2️⃣ Casos de Prueba para Mostrar (3 min)

#### a) Slang Argentino ✨ NUEVO
```
Usuario: "Presupuesto con 200 lucas"
Bot: → Interpreta $200,000 correctamente
     → Muestra regla 50/30/20
```

#### b) Viajes → Ahorro ✨ NUEVO
```
Usuario: "Quiero viajar a Europa"
Bot: → Detecta intención de viaje
     → Redirige a escenario ahorro
     → Pregunta monto y plazo
```

#### c) Inversiones (mejorado)
```
Usuario: "Invertir 50000"
Bot: → Detecta correctamente inversiones
     → Pregunta plazo
Usuario: "1 año"
Bot: → Ofrece simulación
Usuario: "dale"
Bot: → Calcula interés compuesto
```

#### d) Acrónimos Financieros ✨ NUEVO
```
Usuario: "Qué es CER"
Bot: → Explica Coeficiente de Estabilización de Referencia
     → Escenario educación
```

#### e) Contexto Mejorado ✨ NUEVO
```
Usuario: "Quiero ahorrar para un auto"
Bot: → Pregunta monto
Usuario: "3000000"
Bot: → Pregunta plazo
Usuario: "24 meses"
Bot: → MANTIENE contexto de ahorro
     → Calcula cuota mensual
```

### 3️⃣ Mostrar Dashboard (1 min)
```
http://192.168.1.42:5000/dashboard
```
- Gráfico presupuesto 50/30/20
- Simulador interés compuesto
- Comparación inversiones

### 4️⃣ Mostrar Endpoint /debug (30 seg) - OPCIONAL
```
http://192.168.1.42:5000/debug
```
- Ver versión del código desplegado (SHA1)
- Verificar archivos y timestamps
- Demostrar proceso de validación post-deploy

---

## 🎯 Puntos Clave a Mencionar

### Innovación
- NLP aplicado a educación financiera argentina
- Detección de slang local ("lucas", "palo")
- Análisis de sentimientos en tiempo real

### Completitud
- ✅ Web + WhatsApp + Dashboard
- ✅ Persistencia de usuario
- ✅ 7 calculadoras financieras
- ✅ 6 escenarios conversacionales

### Producción Real
- ✅ Desplegado 24/7 en NAS
- ✅ Docker + docker-compose
- ✅ Logs protegidos
- ✅ Tests automatizados (100% passing)

### Mejora Continua
- ✅ Análisis de logs → identificación de errores
- ✅ Correcciones implementadas
- ✅ Validación en producción

---

## 📊 Métricas para Mostrar

- **1,500+ líneas de código Python**
- **6 escenarios conversacionales**
- **7 calculadoras financieras**
- **Tests: 44/44 passing** (local + NAS)
- **Logs analizados: 1,244 interacciones**
- **Tasa de éxito: 88.2% → 100%** (después de mejoras)

---

## 🚨 Troubleshooting Rápido

### Si el NAS no responde:
```powershell
# Verificar conectividad
Test-NetConnection -ComputerName 192.168.1.42 -Port 5000

# Verificar health check
Invoke-WebRequest -Uri "http://192.168.1.42:5000/health"
```

### Si necesitas reiniciar el contenedor:
1. Abrir Portainer: http://192.168.1.42:19900
2. Containers → chatbot-financiero → Restart
3. Esperar 30-40 segundos
4. Verificar: http://192.168.1.42:5000/health

---

## 🎬 Script de Presentación

1. **Intro (30 seg)**
   > "Desarrollé un asistente financiero con IA que ayuda a argentinos con decisiones de dinero. Usa NLP para entender lenguaje natural y slang local."

2. **Demo Web (2 min)**
   > [Mostrar los 5 casos de prueba arriba]
   > "Como ven, entiende 'lucas', detecta viajes, mantiene contexto..."

3. **Dashboard (1 min)**
   > [Abrir dashboard]
   > "Incluye visualizaciones interactivas y calculadoras financieras."

4. **Producción (30 seg)**
   > [Mostrar NAS]
   > "Está desplegado 24/7 en mi NAS, funciona por web y WhatsApp."

5. **Tech Stack (1 min)**
   > "Backend: Flask + SQLite + SQLAlchemy"
   > "Frontend: HTML/JS + Plotly"
   > "Deploy: Docker + docker-compose"
   > "Tests automatizados y análisis continuo de logs"

6. **Q&A**

---

## ✅ Checklist Pre-Presentación

- [ ] NAS accesible: http://192.168.1.42:5000 ✅
- [ ] Health check OK: http://192.168.1.42:5000/health ✅
- [ ] Chat abierto en pestaña del navegador
- [ ] Dashboard abierto en otra pestaña
- [ ] Casos de prueba memorizados
- [ ] /debug listo para mostrar (opcional)
- [ ] Diapositivas listas (si las usás)

---

**¡Éxitos! 🚀**
