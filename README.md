# 💰 Financial Assistant Chatbot | Chatbot Financiero# Chatbot Financiero 24/7 (Web + WhatsApp)



[English](#english) | [Español](#español)> Asistente educativo financiero con simuladores, dashboard y memoria por usuario. Desplegable en NAS con Docker.



---## Resumen (Abstract)



<a name="english"></a>Este proyecto implementa un chatbot financiero en Flask que funciona por web y WhatsApp. Incluye:

## 🇬🇧 English- Procesamiento de intenciones (presupuesto, ahorro, inversiones, deudas, calculadoras, educación)

- Dashboard interactivo con Plotly (presupuesto 50/30/20, interés compuesto, comparación de inversiones)

> AI-powered financial education assistant with budget simulators, interactive dashboard, and user memory. Deployable on NAS with Docker. Available via web and WhatsApp.- Persistencia por usuario (SQLite): ingresos, deudas, perfil de riesgo, etc.

- Identidad y sesión:

### 📋 Overview	- Web: cookie `uid` vía login con DNI o nickname

	- WhatsApp: id por número `From`

This project implements an intelligent financial chatbot built with Flask that works through web interface and WhatsApp. Key features include:	- Vinculación mínima WhatsApp→Web por enlace seguro de un solo uso

- Despliegue simple con Docker/Docker Compose, pensado para NAS

**🤖 Conversational AI:**

- Intent detection (budget, savings, investments, debt, calculators, education)## Arquitectura

- Context-aware responses with memory across conversations

- Natural language processing for financial queries- Backend: Flask (Python)

- UI: HTML/JS + Plotly

**📊 Interactive Dashboard:**- Persistencia: SQLite (SQLAlchemy)

- Budget visualization (50/30/20 rule)- Mensajería: Twilio WhatsApp Webhook (inbound) y TwiML de respuesta

- Compound interest simulator- Contenedores: Docker + docker-compose (con opción de ngrok)

- Investment comparison charts

- Real-time data with PlotlyEndpoints principales:

- Web chat: `GET /`

**💾 User Persistence:**- API chat: `POST /api/chat`

- SQLite database with SQLAlchemy- Dashboard: `GET /dashboard`

- Stores: income, debts, risk profile, savings goals- Salud: `GET /health`

- Cross-channel identity management- Perfil actual: `GET /api/user`

- Login web: `POST /api/login` (dni o nickname)

**🔐 Identity & Sessions:**- Logout web: `POST /api/logout`

- **Web**: Cookie-based `uid` via login (DNI or nickname)- WhatsApp webhook: `POST /whatsapp-webhook`

- **WhatsApp**: User ID from phone number- Vincular WA→web: `GET /claim/<token>` (redirige al dashboard y fija cookie)

- **Linking**: Secure one-time token to connect WhatsApp → Web

## Características destacadas

**🐳 Easy Deployment:**

- Docker & Docker Compose ready- Memoria conversacional ampliada y persistencia por usuario

- Optimized for NAS deployment- Flujo mejorado en inversiones (reconoce “dale” y simula con contexto guardado)

- Optional ngrok tunnel for public access- Dashboard que usa tu perfil (ingreso mensual por defecto desde DB)

- Vinculación mínima y rápida desde WhatsApp (enlace 1 uso, expira a los 15 minutos)

### 🏗️ Architecture

## Ejecutar localmente (Docker)

**Backend:**

- Flask (Python 3.12)```bash

- SQLite + SQLAlchemy# Construir e iniciar

- Twilio WhatsApp APIdocker-compose up -d



**Frontend:**# Verificar

- Responsive HTML/CSS/JScurl http://localhost:5000/health

- Plotly.js for charts```

- Mobile-optimized UI

Accede luego a:

**Infrastructure:**- Chat: http://localhost:5000/

- Docker containers- Dashboard: http://localhost:5000/dashboard

- Health checks

- Volume persistence## Despliegue en NAS



### 🚀 Quick StartConsulta la guía única y concisa: `docs/DEPLOY_NAS.md`.



**Local deployment with Docker:**Incluye opciones de acceso externo (port forwarding, reverse proxy + HTTPS o ngrok) y configuración del webhook de WhatsApp.



```bash## Uso de WhatsApp

# Clone repository

git clone https://github.com/rAmIro-89/finance-assistant-bot.git- Configura en Twilio tu webhook: `http(s)://TU_DOMINIO/whatsapp-webhook`

cd finance-assistant-bot- En el chat de WhatsApp, envía “vincular” para recibir un enlace único y asociar tu número al dashboard web.



# Start services## Datos y privacidad

docker-compose up -d

- Base: SQLite en `data/`

# Check health- Logs de chat: `chat_logs.csv`

curl http://localhost:5000/health- No incluyas secretos en el repo. Usa variables de entorno (ej.: `NGROK_AUTHTOKEN` si utilizas ngrok).

```

## Créditos y licencia

**Access:**

- Chat: http://localhost:5000/Código con fines académicos y de portafolio.

- Dashboard: http://localhost:5000/dashboard

- Licencia: MIT — ver el archivo `LICENSE` en la raíz del repositorio.

### 📡 API Endpoints

Autor: Ramiro Ottone Villar

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web chat interface |
| `/api/chat` | POST | Process chat messages |
| `/dashboard` | GET | Interactive dashboard |
| `/health` | GET | Health check |
| `/api/user` | GET | Current user profile |
| `/api/login` | POST | Web login (DNI/nickname) |
| `/api/logout` | POST | Web logout |
| `/whatsapp-webhook` | POST | WhatsApp inbound messages |
| `/claim/<token>` | GET | Link WhatsApp to web session |

### 💬 WhatsApp Integration

1. Configure Twilio webhook: `https://YOUR_DOMAIN/whatsapp-webhook`
2. Send "vincular" via WhatsApp to receive a one-time link
3. Click the link to access your dashboard with WhatsApp data

### 📦 NAS Deployment

See comprehensive guide: `docs/DEPLOY_NAS.md`

Includes:
- Docker setup on ASUSTOR/Synology/QNAP
- External access options (port forwarding, reverse proxy, ngrok)
- WhatsApp webhook configuration
- Troubleshooting tips

### 🧪 Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

### 📄 License

MIT License - See `LICENSE` file for details.

**Author:** Ramiro Ottone Villar

---

<a name="español"></a>
## 🇦🇷 Español

> Asistente educativo financiero con simuladores, dashboard interactivo y memoria por usuario. Desplegable en NAS con Docker. Disponible vía web y WhatsApp.

### 📋 Resumen

Este proyecto implementa un chatbot financiero inteligente construido con Flask que funciona a través de interfaz web y WhatsApp. Características principales:

**🤖 IA Conversacional:**
- Detección de intenciones (presupuesto, ahorro, inversiones, deudas, calculadoras, educación)
- Respuestas contextuales con memoria entre conversaciones
- Procesamiento de lenguaje natural para consultas financieras

**📊 Dashboard Interactivo:**
- Visualización de presupuesto (regla 50/30/20)
- Simulador de interés compuesto
- Gráficos de comparación de inversiones
- Datos en tiempo real con Plotly

**💾 Persistencia de Usuario:**
- Base de datos SQLite con SQLAlchemy
- Almacena: ingresos, deudas, perfil de riesgo, metas de ahorro
- Gestión de identidad multi-canal

**🔐 Identidad y Sesiones:**
- **Web**: Cookie `uid` vía login (DNI o nickname)
- **WhatsApp**: ID de usuario desde número telefónico
- **Vinculación**: Token seguro de un solo uso para conectar WhatsApp → Web

**🐳 Despliegue Fácil:**
- Docker & Docker Compose listo
- Optimizado para despliegue en NAS
- Túnel ngrok opcional para acceso público

### 🏗️ Arquitectura

**Backend:**
- Flask (Python 3.12)
- SQLite + SQLAlchemy
- API de WhatsApp de Twilio

**Frontend:**
- HTML/CSS/JS responsivo
- Plotly.js para gráficos
- UI optimizada para móviles

**Infraestructura:**
- Contenedores Docker
- Health checks
- Persistencia con volúmenes

### 🚀 Inicio Rápido

**Despliegue local con Docker:**

```bash
# Clonar repositorio
git clone https://github.com/rAmIro-89/finance-assistant-bot.git
cd finance-assistant-bot

# Iniciar servicios
docker-compose up -d

# Verificar salud
curl http://localhost:5000/health
```

**Acceder a:**
- Chat: http://localhost:5000/
- Dashboard: http://localhost:5000/dashboard

### 📡 Endpoints de API

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Interfaz de chat web |
| `/api/chat` | POST | Procesar mensajes del chat |
| `/dashboard` | GET | Dashboard interactivo |
| `/health` | GET | Verificación de salud |
| `/api/user` | GET | Perfil del usuario actual |
| `/api/login` | POST | Login web (DNI/nickname) |
| `/api/logout` | POST | Logout web |
| `/whatsapp-webhook` | POST | Mensajes entrantes de WhatsApp |
| `/claim/<token>` | GET | Vincular WhatsApp a sesión web |

### 💬 Integración con WhatsApp

1. Configurar webhook de Twilio: `https://TU_DOMINIO/whatsapp-webhook`
2. Enviar "vincular" por WhatsApp para recibir enlace de un solo uso
3. Hacer clic en el enlace para acceder al dashboard con datos de WhatsApp

### 📦 Despliegue en NAS

Ver guía completa: `docs/DEPLOY_NAS.md`

Incluye:
- Configuración de Docker en ASUSTOR/Synology/QNAP
- Opciones de acceso externo (port forwarding, reverse proxy, ngrok)
- Configuración de webhook de WhatsApp
- Consejos de troubleshooting

### 🧪 Testing

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
pytest tests/
```

### 📄 Licencia

Licencia MIT - Ver archivo `LICENSE` para detalles.

**Autor:** Ramiro Ottone Villar
