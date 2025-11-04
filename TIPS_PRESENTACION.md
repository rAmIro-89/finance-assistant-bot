# 🎤 Tips Rápidos para la Presentación

## ✅ Pre-vuelo (5 min antes)

1. **Verificar NAS**
   ```
   python test_nas_pre_demo.py
   ```
   → Debe mostrar: ✅ 4/4 casos funcionando

2. **Abrir pestañas en orden**
   - Pestaña 1: http://192.168.1.42:5000 (chat)
   - Pestaña 2: http://192.168.1.42:5000/dashboard
   - Pestaña 3: http://192.168.1.42:5000/debug (opcional)

3. **Tener GUIA_DEMO.md visible** (este archivo)

---

## 🎬 Durante la Demo

### Opener (30 seg)
> "Desarrollé un asistente financiero con IA que funciona 24/7 en mi NAS. Entiende lenguaje natural, slang argentino, y ayuda con decisiones de dinero."

### Demo Interactiva (3 min)

**Mientras escribes cada mensaje, narrar:**

1. **"200 lucas"** → "Detecta slang argentino"
2. **"Viajar a Europa"** → "Identifica viajes como meta de ahorro"  
3. **"Invertir 50000" + "1 año" + "dale"** → "Mantiene contexto en conversaciones multi-turno"
4. **"Qué es CER"** → "Modo educación para conceptos financieros"

### Dashboard (1 min)
> "Incluye visualizaciones interactivas: presupuesto 50/30/20, simuladores de ahorro e inversión."

### Tech Stack (30 seg)
> "Backend Flask, NLP custom, Docker, base de datos SQLite. Todo desplegado en producción con tests automatizados."

---

## 💡 Frases Clave

- **"Producción real, no demo"** → Mencionar que está corriendo 24/7
- **"Slang argentino"** → 'lucas', 'palo', 'verde'
- **"Análisis continuo"** → Logs → mejoras → deploy → validación
- **"88% → 100% éxito"** → Mostrar mejora medible

---

## 🚨 Plan B

### Si algo falla:
1. **NAS no responde** → Mostrar local: `python web_app.py`
2. **Chat lento** → Explicar: "Está en mi NAS, red local"
3. **Pregunta inesperada** → Improvisa con /dashboard o /debug

### Backup: localhost
Si el NAS falla completamente:
```powershell
python web_app.py
# Usar http://localhost:5000
```

---

## 🎯 Cierre Fuerte

> "Este bot no es solo código académico: está en producción, funciona por WhatsApp, analiza logs reales, y se mejora continuamente. Es un proyecto end-to-end completo."

**Mostrar GitHub:**
```
https://github.com/rAmIro-89/finance-assistant-bot
```

---

## ⏱️ Timing

- Intro: 30 seg
- Demo chat: 3 min
- Dashboard: 1 min
- Tech: 30 seg
- **Total: 5 min**

Si tenés más tiempo:
- Mostrar /debug (versión, SHA1)
- Explicar proceso de deploy
- Mostrar análisis de logs

---

## 🎉 Último Check

- [ ] NAS funcionando (4/4 tests)
- [ ] Pestañas abiertas
- [ ] Casos memorizados
- [ ] Laptop cargada
- [ ] Proyector probado

**¡MUCHA SUERTE! 🚀**
