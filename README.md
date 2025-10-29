# 💰 Financial Assistant Chatbot | Chatbot Financiero

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.1-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-Integration-25D366.svg)](https://www.twilio.com/whatsapp)

[English](#english) | [Español](#español)

---

<a name="english"></a>
## 🇬🇧 English

> AI-powered financial education assistant with budget simulators, interactive dashboard, and user memory. Deployable on NAS with Docker. Available via web and WhatsApp.

### 📸 Screenshots

<div align="center">

![Web Chat](images/web-chat.png)

![Dashboard](images/dashboard.png)

![WhatsApp](images/whatsapp.png)

</div>

### 📋 Overview

This project implements an intelligent financial chatbot built with Flask that works through web interface and WhatsApp. Key features include:

**🤖 Conversational AI:**
- Intent detection (budget, savings, investments, debt, calculators, education)
- Context-aware responses with memory across conversations
- Natural language processing for financial queries

**📊 Interactive Dashboard:**
- Budget visualization (50/30/20 rule)
- Compound interest simulator
- Investment comparison charts
- Real-time data with Plotly

**💾 User Persistence:**
- SQLite database with SQLAlchemy
- Stores: income, debts, risk profile, savings goals
- Cross-channel identity management

**🔐 Identity & Sessions:**
- Web: Cookie-based `uid` via login (DNI or nickname)
- WhatsApp: User ID from phone number
- Linking: Secure one-time token to connect WhatsApp → Web

**🐳 Easy Deployment:**
- Docker & Docker Compose ready
- Optimized for NAS deployment
- Optional ngrok tunnel for public access

### 🏗️ Architecture

Backend: Flask (Python 3.12) · SQLite + SQLAlchemy · Twilio WhatsApp API  
Frontend: Responsive HTML/CSS/JS · Plotly.js  
Infra: Docker containers · Health checks · Volume persistence

### 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/rAmIro-89/finance-assistant-bot.git
cd finance-assistant-bot

# Start services
docker-compose up -d

# Check health
curl http://localhost:5000/health
```

Access:
- Chat: http://localhost:5000/
- Dashboard: http://localhost:5000/dashboard

### 📡 API Endpoints

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
See comprehensive guide: [`docs/DEPLOY_NAS.md`](docs/DEPLOY_NAS.md)

### 🧪 Testing

```bash
pip install -r requirements.txt
pytest tests/
```

### 📄 License
MIT License — see [`LICENSE`](LICENSE).  
Author: Ramiro Ottone Villar

---

<a name="español"></a>
## 🇦🇷 Español

> Asistente educativo financiero con simuladores, dashboard interactivo y memoria por usuario. Desplegable en NAS con Docker. Disponible vía web y WhatsApp.

### 📸 Capturas de Pantalla

<div align="center">

![Interfaz de Chat Web](images/web-chat.png)

![Dashboard Interactivo](images/dashboard.png)

![Integración con WhatsApp](images/whatsapp.png)

</div>

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
- Web: Cookie `uid` vía login (DNI o nickname)
- WhatsApp: ID de usuario desde número telefónico
- Vinculación: Token seguro de un solo uso para conectar WhatsApp → Web

**🐳 Despliegue Fácil:**
- Docker & Docker Compose listo
- Optimizado para despliegue en NAS
- Túnel ngrok opcional para acceso público

### 🏗️ Arquitectura

Backend: Flask (Python 3.12) · SQLite + SQLAlchemy · API de WhatsApp Twilio  
Frontend: HTML/CSS/JS responsivo · Plotly.js  
Infra: Contenedores Docker · Health checks · Persistencia con volúmenes

### 🚀 Inicio Rápido

```bash
git clone https://github.com/rAmIro-89/finance-assistant-bot.git
cd finance-assistant-bot
docker-compose up -d
curl http://localhost:5000/health
```

Acceso:
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
Ver guía completa: [`docs/DEPLOY_NAS.md`](docs/DEPLOY_NAS.md)

### 🧪 Testing

```bash
pip install -r requirements.txt
pytest tests/
```

### 📄 Licencia
Licencia MIT — ver [`LICENSE`](LICENSE).  
Autor: Ramiro Ottone Villar
# 💰 Financial Assistant Chatbot | Chatbot Financiero# 💰 Financial Assistant Chatbot | Chatbot Financiero# Chatbot Financiero 24/7 (Web + WhatsApp)



[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)

[![Flask](https://img.shields.io/badge/flask-3.1-green.svg)](https://flask.palletsprojects.com/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[English](#english) | [Español](#español)> Asistente educativo financiero con simuladores, dashboard y memoria por usuario. Desplegable en NAS con Docker.

[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

[![WhatsApp](https://img.shields.io/badge/WhatsApp-Integration-25D366.svg)](https://www.twilio.com/whatsapp)



[English](#english) | [Español](#español)---## Resumen (Abstract)



---



<a name="english"></a><a name="english"></a>Este proyecto implementa un chatbot financiero en Flask que funciona por web y WhatsApp. Incluye:

## 🇬🇧 English

## 🇬🇧 English- Procesamiento de intenciones (presupuesto, ahorro, inversiones, deudas, calculadoras, educación)

> AI-powered financial education assistant with budget simulators, interactive dashboard, and user memory. Deployable on NAS with Docker. Available via web and WhatsApp.

- Dashboard interactivo con Plotly (presupuesto 50/30/20, interés compuesto, comparación de inversiones)

### 📸 Screenshots

> AI-powered financial education assistant with budget simulators, interactive dashboard, and user memory. Deployable on NAS with Docker. Available via web and WhatsApp.- Persistencia por usuario (SQLite): ingresos, deudas, perfil de riesgo, etc.

<div align="center">

- Identidad y sesión:

**Web Chat Interface**  

*Coming soon*### 📋 Overview	- Web: cookie `uid` vía login con DNI o nickname



**Interactive Dashboard**  	- WhatsApp: id por número `From`

*Coming soon*

This project implements an intelligent financial chatbot built with Flask that works through web interface and WhatsApp. Key features include:	- Vinculación mínima WhatsApp→Web por enlace seguro de un solo uso

**WhatsApp Integration**  

*Coming soon*- Despliegue simple con Docker/Docker Compose, pensado para NAS



</div>**🤖 Conversational AI:**



### 📋 Overview- Intent detection (budget, savings, investments, debt, calculators, education)## Arquitectura



This project implements an intelligent financial chatbot built with Flask that works through web interface and WhatsApp. Key features include:- Context-aware responses with memory across conversations



**🤖 Conversational AI:**- Natural language processing for financial queries- Backend: Flask (Python)

- Intent detection (budget, savings, investments, debt, calculators, education)

- Context-aware responses with memory across conversations- UI: HTML/JS + Plotly

- Natural language processing for financial queries

**📊 Interactive Dashboard:**- Persistencia: SQLite (SQLAlchemy)

**📊 Interactive Dashboard:**

- Budget visualization (50/30/20 rule)- Budget visualization (50/30/20 rule)- Mensajería: Twilio WhatsApp Webhook (inbound) y TwiML de respuesta

- Compound interest simulator

- Investment comparison charts- Compound interest simulator- Contenedores: Docker + docker-compose (con opción de ngrok)

- Real-time data with Plotly

- Investment comparison charts

**💾 User Persistence:**

- SQLite database with SQLAlchemy- Real-time data with PlotlyEndpoints principales:

- Stores: income, debts, risk profile, savings goals

- Cross-channel identity management- Web chat: `GET /`



**🔐 Identity & Sessions:****💾 User Persistence:**- API chat: `POST /api/chat`

- **Web**: Cookie-based `uid` via login (DNI or nickname)

- **WhatsApp**: User ID from phone number- SQLite database with SQLAlchemy- Dashboard: `GET /dashboard`

- **Linking**: Secure one-time token to connect WhatsApp → Web

- Stores: income, debts, risk profile, savings goals- Salud: `GET /health`

**🐳 Easy Deployment:**

- Docker & Docker Compose ready- Cross-channel identity management- Perfil actual: `GET /api/user`

- Optimized for NAS deployment

- Optional ngrok tunnel for public access- Login web: `POST /api/login` (dni o nickname)



### 🏗️ Architecture**🔐 Identity & Sessions:**- Logout web: `POST /api/logout`



**Backend:**- **Web**: Cookie-based `uid` via login (DNI or nickname)- WhatsApp webhook: `POST /whatsapp-webhook`

- Flask (Python 3.12)

- SQLite + SQLAlchemy- **WhatsApp**: User ID from phone number- Vincular WA→web: `GET /claim/<token>` (redirige al dashboard y fija cookie)

- Twilio WhatsApp API

- **Linking**: Secure one-time token to connect WhatsApp → Web

**Frontend:**

- Responsive HTML/CSS/JS## Características destacadas

- Plotly.js for charts

- Mobile-optimized UI**🐳 Easy Deployment:**



**Infrastructure:**- Docker & Docker Compose ready- Memoria conversacional ampliada y persistencia por usuario

- Docker containers

- Health checks- Optimized for NAS deployment- Flujo mejorado en inversiones (reconoce “dale” y simula con contexto guardado)

- Volume persistence

- Optional ngrok tunnel for public access- Dashboard que usa tu perfil (ingreso mensual por defecto desde DB)

### 🚀 Quick Start

- Vinculación mínima y rápida desde WhatsApp (enlace 1 uso, expira a los 15 minutos)

**Local deployment with Docker:**

### 🏗️ Architecture

```bash

# Clone repository## Ejecutar localmente (Docker)

git clone https://github.com/rAmIro-89/finance-assistant-bot.git

cd finance-assistant-bot**Backend:**



# Start services- Flask (Python 3.12)```bash

docker-compose up -d

- SQLite + SQLAlchemy# Construir e iniciar

# Check health

curl http://localhost:5000/health- Twilio WhatsApp APIdocker-compose up -d

```



**Access:**

- Chat: http://localhost:5000/**Frontend:**# Verificar

- Dashboard: http://localhost:5000/dashboard

- Responsive HTML/CSS/JScurl http://localhost:5000/health

### 📡 API Endpoints

- Plotly.js for charts```

| Endpoint | Method | Description |

|----------|--------|-------------|- Mobile-optimized UI

| `/` | GET | Web chat interface |

| `/api/chat` | POST | Process chat messages |Accede luego a:

| `/dashboard` | GET | Interactive dashboard |

| `/health` | GET | Health check |**Infrastructure:**- Chat: http://localhost:5000/

| `/api/user` | GET | Current user profile |

| `/api/login` | POST | Web login (DNI/nickname) |- Docker containers- Dashboard: http://localhost:5000/dashboard

| `/api/logout` | POST | Web logout |

| `/whatsapp-webhook` | POST | WhatsApp inbound messages |- Health checks

| `/claim/<token>` | GET | Link WhatsApp to web session |

- Volume persistence## Despliegue en NAS

### 💬 WhatsApp Integration



1. Configure Twilio webhook: `https://YOUR_DOMAIN/whatsapp-webhook`

2. Send "vincular" via WhatsApp to receive a one-time link### 🚀 Quick StartConsulta la guía única y concisa: `docs/DEPLOY_NAS.md`.

3. Click the link to access your dashboard with WhatsApp data



### 📦 NAS Deployment

**Local deployment with Docker:**Incluye opciones de acceso externo (port forwarding, reverse proxy + HTTPS o ngrok) y configuración del webhook de WhatsApp.

See comprehensive guide: [`docs/DEPLOY_NAS.md`](docs/DEPLOY_NAS.md)



Includes:

- Docker setup on ASUSTOR/Synology/QNAP```bash## Uso de WhatsApp

- External access options (port forwarding, reverse proxy, ngrok)

- WhatsApp webhook configuration# Clone repository

- Troubleshooting tips

git clone https://github.com/rAmIro-89/finance-assistant-bot.git- Configura en Twilio tu webhook: `http(s)://TU_DOMINIO/whatsapp-webhook`

### 🧪 Testing

cd finance-assistant-bot- En el chat de WhatsApp, envía “vincular” para recibir un enlace único y asociar tu número al dashboard web.

```bash

# Install dependencies

pip install -r requirements.txt

# Start services## Datos y privacidad

# Run tests

pytest tests/docker-compose up -d

```

- Base: SQLite en `data/`

### 🛠️ Tech Stack

# Check health- Logs de chat: `chat_logs.csv`

- **Backend**: Python 3.12, Flask, SQLAlchemy

- **Frontend**: HTML5, CSS3, JavaScript, Plotly.jscurl http://localhost:5000/health- No incluyas secretos en el repo. Usa variables de entorno (ej.: `NGROK_AUTHTOKEN` si utilizas ngrok).

- **Database**: SQLite

- **Integration**: Twilio WhatsApp API```

- **Deployment**: Docker, Docker Compose

- **Testing**: pytest## Créditos y licencia



### 📄 License**Access:**



MIT License - See [`LICENSE`](LICENSE) file for details.- Chat: http://localhost:5000/Código con fines académicos y de portafolio.



**Author:** Ramiro Ottone Villar- Dashboard: http://localhost:5000/dashboard



---- Licencia: MIT — ver el archivo `LICENSE` en la raíz del repositorio.



<a name="español"></a>### 📡 API Endpoints

## 🇦🇷 Español

Autor: Ramiro Ottone Villar

> Asistente educativo financiero con simuladores, dashboard interactivo y memoria por usuario. Desplegable en NAS con Docker. Disponible vía web y WhatsApp.

| Endpoint | Method | Description |

### 📸 Capturas de Pantalla|----------|--------|-------------|

| `/` | GET | Web chat interface |

<div align="center">| `/api/chat` | POST | Process chat messages |

| `/dashboard` | GET | Interactive dashboard |

**Interfaz de Chat Web**  | `/health` | GET | Health check |

*Próximamente*| `/api/user` | GET | Current user profile |

| `/api/login` | POST | Web login (DNI/nickname) |

**Dashboard Interactivo**  | `/api/logout` | POST | Web logout |

*Próximamente*| `/whatsapp-webhook` | POST | WhatsApp inbound messages |

| `/claim/<token>` | GET | Link WhatsApp to web session |

**Integración con WhatsApp**  

*Próximamente*### 💬 WhatsApp Integration



</div>1. Configure Twilio webhook: `https://YOUR_DOMAIN/whatsapp-webhook`

2. Send "vincular" via WhatsApp to receive a one-time link

### 📋 Resumen3. Click the link to access your dashboard with WhatsApp data



Este proyecto implementa un chatbot financiero inteligente construido con Flask que funciona a través de interfaz web y WhatsApp. Características principales:### 📦 NAS Deployment



**🤖 IA Conversacional:**See comprehensive guide: `docs/DEPLOY_NAS.md`

- Detección de intenciones (presupuesto, ahorro, inversiones, deudas, calculadoras, educación)

- Respuestas contextuales con memoria entre conversacionesIncludes:

- Procesamiento de lenguaje natural para consultas financieras- Docker setup on ASUSTOR/Synology/QNAP

- External access options (port forwarding, reverse proxy, ngrok)

**📊 Dashboard Interactivo:**- WhatsApp webhook configuration

- Visualización de presupuesto (regla 50/30/20)- Troubleshooting tips

- Simulador de interés compuesto

- Gráficos de comparación de inversiones### 🧪 Testing

- Datos en tiempo real con Plotly

```bash

**💾 Persistencia de Usuario:**# Install dependencies

- Base de datos SQLite con SQLAlchemypip install -r requirements.txt

- Almacena: ingresos, deudas, perfil de riesgo, metas de ahorro

- Gestión de identidad multi-canal# Run tests

pytest tests/

**🔐 Identidad y Sesiones:**```

- **Web**: Cookie `uid` vía login (DNI o nickname)

- **WhatsApp**: ID de usuario desde número telefónico### 📄 License

- **Vinculación**: Token seguro de un solo uso para conectar WhatsApp → Web

MIT License - See `LICENSE` file for details.

**🐳 Despliegue Fácil:**

- Docker & Docker Compose listo**Author:** Ramiro Ottone Villar

- Optimizado para despliegue en NAS

- Túnel ngrok opcional para acceso público---



### 🏗️ Arquitectura<a name="español"></a>

## 🇦🇷 Español

**Backend:**

- Flask (Python 3.12)> Asistente educativo financiero con simuladores, dashboard interactivo y memoria por usuario. Desplegable en NAS con Docker. Disponible vía web y WhatsApp.

- SQLite + SQLAlchemy

- API de WhatsApp de Twilio### 📋 Resumen



**Frontend:**Este proyecto implementa un chatbot financiero inteligente construido con Flask que funciona a través de interfaz web y WhatsApp. Características principales:

- HTML/CSS/JS responsivo

- Plotly.js para gráficos**🤖 IA Conversacional:**

- UI optimizada para móviles- Detección de intenciones (presupuesto, ahorro, inversiones, deudas, calculadoras, educación)

- Respuestas contextuales con memoria entre conversaciones

**Infraestructura:**- Procesamiento de lenguaje natural para consultas financieras

- Contenedores Docker

- Health checks**📊 Dashboard Interactivo:**

- Persistencia con volúmenes- Visualización de presupuesto (regla 50/30/20)

- Simulador de interés compuesto

### 🚀 Inicio Rápido- Gráficos de comparación de inversiones

- Datos en tiempo real con Plotly

**Despliegue local con Docker:**

**💾 Persistencia de Usuario:**

```bash- Base de datos SQLite con SQLAlchemy

# Clonar repositorio- Almacena: ingresos, deudas, perfil de riesgo, metas de ahorro

git clone https://github.com/rAmIro-89/finance-assistant-bot.git- Gestión de identidad multi-canal

cd finance-assistant-bot

**🔐 Identidad y Sesiones:**

# Iniciar servicios- **Web**: Cookie `uid` vía login (DNI o nickname)

docker-compose up -d- **WhatsApp**: ID de usuario desde número telefónico

- **Vinculación**: Token seguro de un solo uso para conectar WhatsApp → Web

# Verificar salud

curl http://localhost:5000/health**🐳 Despliegue Fácil:**

```- Docker & Docker Compose listo

- Optimizado para despliegue en NAS

**Acceder a:**- Túnel ngrok opcional para acceso público

- Chat: http://localhost:5000/

- Dashboard: http://localhost:5000/dashboard### 🏗️ Arquitectura



### 📡 Endpoints de API**Backend:**

- Flask (Python 3.12)

| Endpoint | Método | Descripción |- SQLite + SQLAlchemy

|----------|--------|-------------|- API de WhatsApp de Twilio

| `/` | GET | Interfaz de chat web |

| `/api/chat` | POST | Procesar mensajes del chat |**Frontend:**

| `/dashboard` | GET | Dashboard interactivo |- HTML/CSS/JS responsivo

| `/health` | GET | Verificación de salud |- Plotly.js para gráficos

| `/api/user` | GET | Perfil del usuario actual |- UI optimizada para móviles

| `/api/login` | POST | Login web (DNI/nickname) |

| `/api/logout` | POST | Logout web |**Infraestructura:**

| `/whatsapp-webhook` | POST | Mensajes entrantes de WhatsApp |- Contenedores Docker

| `/claim/<token>` | GET | Vincular WhatsApp a sesión web |- Health checks

- Persistencia con volúmenes

### 💬 Integración con WhatsApp

### 🚀 Inicio Rápido

1. Configurar webhook de Twilio: `https://TU_DOMINIO/whatsapp-webhook`

2. Enviar "vincular" por WhatsApp para recibir enlace de un solo uso**Despliegue local con Docker:**

3. Hacer clic en el enlace para acceder al dashboard con datos de WhatsApp

```bash

### 📦 Despliegue en NAS# Clonar repositorio

git clone https://github.com/rAmIro-89/finance-assistant-bot.git

Ver guía completa: [`docs/DEPLOY_NAS.md`](docs/DEPLOY_NAS.md)cd finance-assistant-bot



Incluye:# Iniciar servicios

- Configuración de Docker en ASUSTOR/Synology/QNAPdocker-compose up -d

- Opciones de acceso externo (port forwarding, reverse proxy, ngrok)

- Configuración de webhook de WhatsApp# Verificar salud

- Consejos de troubleshootingcurl http://localhost:5000/health

```

### 🧪 Testing

**Acceder a:**

```bash- Chat: http://localhost:5000/

# Instalar dependencias- Dashboard: http://localhost:5000/dashboard

pip install -r requirements.txt

### 📡 Endpoints de API

# Ejecutar tests

pytest tests/| Endpoint | Método | Descripción |

```|----------|--------|-------------|

| `/` | GET | Interfaz de chat web |

### 🛠️ Stack Tecnológico| `/api/chat` | POST | Procesar mensajes del chat |

| `/dashboard` | GET | Dashboard interactivo |

- **Backend**: Python 3.12, Flask, SQLAlchemy| `/health` | GET | Verificación de salud |

- **Frontend**: HTML5, CSS3, JavaScript, Plotly.js| `/api/user` | GET | Perfil del usuario actual |

- **Base de Datos**: SQLite| `/api/login` | POST | Login web (DNI/nickname) |

- **Integración**: API de WhatsApp de Twilio| `/api/logout` | POST | Logout web |

- **Despliegue**: Docker, Docker Compose| `/whatsapp-webhook` | POST | Mensajes entrantes de WhatsApp |

- **Testing**: pytest| `/claim/<token>` | GET | Vincular WhatsApp a sesión web |



### 📄 Licencia### 💬 Integración con WhatsApp



Licencia MIT - Ver archivo [`LICENSE`](LICENSE) para detalles.1. Configurar webhook de Twilio: `https://TU_DOMINIO/whatsapp-webhook`

2. Enviar "vincular" por WhatsApp para recibir enlace de un solo uso

**Autor:** Ramiro Ottone Villar3. Hacer clic en el enlace para acceder al dashboard con datos de WhatsApp


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
