# 💰 Financial Assistant Chatbot | Chatbot Financiero

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.1-green.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-Integration-25D366.svg)](https://www.twilio.com/whatsapp)

[English](#english) | [Español](#español)

---

<a name="english"></a>
## 🇬🇧 English

AI-powered financial education assistant with budget simulators, interactive dashboard, and per-user memory. Deployable on NAS with Docker. Available via web and WhatsApp.

### Highlights
- Conversational AI: intents (budget, savings, investments, debts, calculators, education), NLP, and context memory
- Dashboard: 50/30/20 budget, compound interest, investment comparisons (Plotly)
- Persistence: SQLite + SQLAlchemy (income, debts, risk, savings goals)
- Identity: web cookie `uid`, WhatsApp phone-based ID, secure one-time link to connect WhatsApp → Web
- Deployment: Docker + Compose, optimized for NAS, optional ngrok

### Quick Start
```bash
docker-compose up -d
curl http://localhost:5000/health
```
Access: Chat http://localhost:5000/ · Dashboard http://localhost:5000/dashboard

### Endpoints
- GET `/` chat UI
- POST `/api/chat` process chat messages
- GET `/dashboard` interactive charts
- GET `/health` health check
- GET `/api/user` current profile
- POST `/api/login` (dni or nickname)
- POST `/api/logout`
- POST `/whatsapp-webhook` Twilio inbound
- GET `/claim/<token>` link WhatsApp → web session

### WhatsApp
1) Set Twilio webhook to `https://YOUR_DOMAIN/whatsapp-webhook`
2) Send "vincular" on WhatsApp to receive a one-time link
3) Open the link to auto-login on the web dashboard

### NAS Deployment
See: docs/DEPLOY_NAS.md

### Testing
```bash
pip install -r requirements.txt
pytest -q
```

---

<a name="español"></a>
## 🇦🇷 Español

Asistente educativo financiero con simuladores, dashboard y memoria por usuario. Desplegable en NAS con Docker. Disponible por web y WhatsApp.

### Destacados
- IA Conversacional: intenciones (presupuesto, ahorro, inversiones, deudas, calculadoras, educación), PLN y memoria de contexto
- Dashboard: regla 50/30/20, interés compuesto, comparación de inversiones (Plotly)
- Persistencia: SQLite + SQLAlchemy (ingresos, deudas, perfil de riesgo, metas de ahorro)
- Identidad: cookie `uid` en web, ID por número en WhatsApp, enlace único para vincular WA→Web
- Despliegue: Docker + Compose, optimizado para NAS, ngrok opcional

### Inicio Rápido
```bash
docker-compose up -d
curl http://localhost:5000/health
```
Acceso: Chat http://localhost:5000/ · Dashboard http://localhost:5000/dashboard

### Endpoints
- GET `/` interfaz de chat
- POST `/api/chat` procesamiento de mensajes
- GET `/dashboard` gráficos interactivos
- GET `/health` estado
- GET `/api/user` perfil actual
- POST `/api/login` (dni o nickname)
- POST `/api/logout`
- POST `/whatsapp-webhook` webhook de Twilio
- GET `/claim/<token>` vincula WhatsApp → web

### WhatsApp
1) Configurá en Twilio el webhook: `https://TU_DOMINIO/whatsapp-webhook`
2) Enviá "vincular" por WhatsApp para recibir un enlace único
3) Abrí el enlace para ingresar directo al dashboard

### Despliegue en NAS
Guía: docs/DEPLOY_NAS.md

### Testing
```bash
pip install -r requirements.txt
pytest -q
```

---

## Operations & Validation

- Logs: how to analyze and keep them out of Git — see LOGS_ANALISIS.md
- Production validation checklist:
	1) Deploy changes and restart container
	2) Open `/debug` to confirm SHA1 and timestamps
	3) Run targeted tests (travel→ahorro, acronyms→educación, short replies keep context)

## Recent Improvements
- Travel intent routed to savings: "quiero viajar a…", "conocer/ir/visitar …" → ahorro
- Acronyms → education: CER/UVA/TNA/TEA/CFT directly; FCI/CEDEAR/ETF if "?" or "qué es"
- Short replies and numbers respect conversation context (e.g., "24 meses", "si", amounts)
- Slang parsing: "lucas" recognized as thousands (e.g., "200 lucas" → 200,000)

## License
MIT — see LICENSE. Author: Ramiro Ottone Villar
