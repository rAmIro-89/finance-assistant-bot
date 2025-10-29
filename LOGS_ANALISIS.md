# 📊 CÓMO VER Y ANALIZAR LOGS DEL BOT

## 🔒 PRIVACIDAD
Los logs contienen datos de usuarios y **NO se suben a GitHub**.
Están protegidos en `.gitignore`:
- `chat_logs.csv`
- `chat_logs_backup*.csv`
- `logs_dashboard.html`

---

## 📥 SINCRONIZAR LOGS DESDE EL NAS

### Opción 1: Script automático (Recomendado)
```bash
sync_logs_from_nas.bat
```

Esto:
1. ✅ Descarga `chat_logs.csv` desde Y:\deploy-nas
2. ✅ Crea backup con fecha del log anterior
3. ✅ Muestra estadísticas rápidas
4. ✅ Opción de análisis inmediato

### Opción 2: Manual
```bash
copy Y:\deploy-nas\chat_logs.csv chat_logs.csv
```

---

## 📊 FORMAS DE ANALIZAR LOS LOGS

### 1️⃣ Dashboard Web Interactivo (NAS)
Desde el navegador mientras el bot está corriendo:
```
http://192.168.1.42:5000/logs          (desde tu red local)
http://TU_NGROK_URL/logs               (desde internet)
```

**Características:**
- ✅ Tiempo real
- ✅ Búsqueda y filtros
- ✅ Estadísticas visuales
- ✅ No requiere descargar nada

---

### 2️⃣ Dashboard HTML Local (Offline)
Genera un archivo HTML que puedes abrir sin servidor:

```bash
python generate_logs_dashboard.py
```

Esto genera `logs_dashboard.html` con:
- 📊 Gráficos interactivos (Plotly)
- 📈 Estadísticas por escenario
- 😊 Análisis de sentimientos
- ⚠️ Detección de pérdidas de contexto
- 💭 Mensajes no entendidos
- 🕐 Actividad por hora

Se abre automáticamente en tu navegador.

---

### 3️⃣ Análisis por Terminal
```bash
python analyze_logs.py
```

Genera reporte de texto con:
- Distribución por escenarios
- Detección de errores
- Mensajes no entendidos
- Recomendaciones de mejora

---

### 4️⃣ Excel/LibreOffice
Abre directamente `chat_logs.csv` para análisis manual:
```
chat_logs.csv
```

Columnas:
- `timestamp`: Fecha y hora
- `scenario`: presupuesto, ahorro, inversiones, deudas, educacion, calculadora, ayuda
- `sentiment`: positivo, negativo, neutral
- `emotion`: motivado, preocupado, estresado, confundido, frustrado, etc.
- `user`: Mensaje del usuario
- `bot`: Respuesta del bot

---

## 🔄 FLUJO DE TRABAJO RECOMENDADO

### Cada semana:
1. Ejecutar `sync_logs_from_nas.bat`
2. Generar dashboard: `python generate_logs_dashboard.py`
3. Revisar:
   - ¿Hay pérdida de contexto?
   - ¿Qué preguntas no se entienden?
   - ¿Qué escenarios son más usados?
4. Implementar mejoras en base al análisis
5. Deploy al NAS con `deploy_to_nas.bat`

### Diariamente:
- Ver logs en tiempo real: http://192.168.1.42:5000/logs
- Monitorear que no haya errores críticos

---

## 🎯 INDICADORES CLAVE

### ✅ Bot funcionando bien:
- `ayuda` < 20% del total
- Pérdida de contexto < 5%
- Sentimiento positivo > 40%

### ⚠️ Requiere atención:
- `ayuda` > 30% (muchos mensajes no entendidos)
- Pérdida de contexto > 10%
- Sentimiento negativo > 30%

### 🚨 Crítico:
- `ayuda` > 50%
- Sentimiento negativo > 50%
- Emociones: frustrado, desesperado, enojado > 20%

---

## 📁 UBICACIONES

### Local (desarrollo):
```
E:\Tecnica de Procesamiento del Habla\Trabajo TPH\
├── chat_logs.csv              (logs locales, NO en git)
├── logs_dashboard.html        (dashboard generado, NO en git)
├── sync_logs_from_nas.bat     (script sincronización)
└── generate_logs_dashboard.py (generador dashboard)
```

### NAS (producción):
```
Y:\deploy-nas\
├── chat_logs.csv              (logs de producción)
└── web_app.py                 (incluye endpoint /logs)
```

### GitHub:
```
❌ chat_logs.csv              → Bloqueado por .gitignore
❌ logs_dashboard.html        → Bloqueado por .gitignore
✅ web_app.py                 → SÍ (código del bot)
✅ chatbot_core.py            → SÍ (lógica del bot)
✅ analyze_logs.py            → SÍ (herramienta análisis)
```

---

## 🔐 SEGURIDAD Y PRIVACIDAD

### Datos que contienen los logs:
- ❌ NO contienen nombres reales (solo IDs)
- ❌ NO contienen números de teléfono completos
- ✅ SÍ contienen mensajes de texto
- ✅ SÍ contienen montos mencionados
- ✅ SÍ contienen metas personales (casa, auto, etc.)

### Mejores prácticas:
1. **Nunca subir logs a GitHub** ✅ Ya protegido en .gitignore
2. **No compartir logs_dashboard.html públicamente**
3. **Guardar backups locales** (se generan automáticamente)
4. **Limpiar logs antiguos** si hay problemas de espacio

---

## 💡 TIPS

### Backup automático:
Los backups se crean automáticamente con timestamp:
```
chat_logs_backup_20251029_1435.csv
```

### Buscar patrones específicos:
```bash
# Buscar todas las menciones de "oro"
findstr /i "oro" chat_logs.csv

# Ver solo errores de contexto
python analyze_logs.py | findstr "contexto"
```

### Resetear logs (si es necesario):
```bash
# En el NAS, conectado por SSH
rm /volume1/Docker/deploy-nas/chat_logs.csv
# Se creará automáticamente en la siguiente interacción
```

---

## 🆘 TROUBLESHOOTING

### "No se encuentra chat_logs.csv"
- Verifica que Y: esté mapeado: `dir Y:\deploy-nas`
- Verifica que el bot haya recibido al menos 1 mensaje

### "Error de encoding al abrir CSV"
- Abre con Excel/LibreOffice y selecciona UTF-8

### "Dashboard no se genera"
- Verifica que tengas plotly: `pip install plotly`
- Ejecuta: `python generate_logs_dashboard.py`

---

## ✨ MEJORAS FUTURAS

Ideas para implementar:
- [ ] Exportar reportes PDF
- [ ] Alertas automáticas si contexto < 90%
- [ ] Gráficos de tendencias temporales
- [ ] Comparación semana a semana
- [ ] Análisis de palabras clave más buscadas
- [ ] Heatmap de actividad por día/hora

---

**Última actualización:** 29 de octubre de 2025
