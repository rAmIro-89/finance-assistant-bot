# Chatbot Financiero 24/7 (Web + WhatsApp)

> Asistente educativo financiero con simuladores, dashboard y memoria por usuario. Desplegable en NAS con Docker.

## Resumen (Abstract)

Este proyecto implementa un chatbot financiero en Flask que funciona por web y WhatsApp. Incluye:
- Procesamiento de intenciones (presupuesto, ahorro, inversiones, deudas, calculadoras, educación)
- Dashboard interactivo con Plotly (presupuesto 50/30/20, interés compuesto, comparación de inversiones)
- Persistencia por usuario (SQLite): ingresos, deudas, perfil de riesgo, etc.
- Identidad y sesión:
	- Web: cookie `uid` vía login con DNI o nickname
	- WhatsApp: id por número `From`
	- Vinculación mínima WhatsApp→Web por enlace seguro de un solo uso
- Despliegue simple con Docker/Docker Compose, pensado para NAS

## Arquitectura

- Backend: Flask (Python)
- UI: HTML/JS + Plotly
- Persistencia: SQLite (SQLAlchemy)
- Mensajería: Twilio WhatsApp Webhook (inbound) y TwiML de respuesta
- Contenedores: Docker + docker-compose (con opción de ngrok)

Endpoints principales:
- Web chat: `GET /`
- API chat: `POST /api/chat`
- Dashboard: `GET /dashboard`
- Salud: `GET /health`
- Perfil actual: `GET /api/user`
- Login web: `POST /api/login` (dni o nickname)
- Logout web: `POST /api/logout`
- WhatsApp webhook: `POST /whatsapp-webhook`
- Vincular WA→web: `GET /claim/<token>` (redirige al dashboard y fija cookie)

## Características destacadas

- Memoria conversacional ampliada y persistencia por usuario
- Flujo mejorado en inversiones (reconoce “dale” y simula con contexto guardado)
- Dashboard que usa tu perfil (ingreso mensual por defecto desde DB)
- Vinculación mínima y rápida desde WhatsApp (enlace 1 uso, expira a los 15 minutos)

## Ejecutar localmente (Docker)

```bash
# Construir e iniciar
docker-compose up -d

# Verificar
curl http://localhost:5000/health
```

Accede luego a:
- Chat: http://localhost:5000/
- Dashboard: http://localhost:5000/dashboard

## Despliegue en NAS

Consulta la guía única y concisa: `docs/DEPLOY_NAS.md`.

Incluye opciones de acceso externo (port forwarding, reverse proxy + HTTPS o ngrok) y configuración del webhook de WhatsApp.

## Uso de WhatsApp

- Configura en Twilio tu webhook: `http(s)://TU_DOMINIO/whatsapp-webhook`
- En el chat de WhatsApp, envía “vincular” para recibir un enlace único y asociar tu número al dashboard web.

## Datos y privacidad

- Base: SQLite en `data/`
- Logs de chat: `chat_logs.csv`
- No incluyas secretos en el repo. Usa variables de entorno (ej.: `NGROK_AUTHTOKEN` si utilizas ngrok).

## Créditos y licencia

Código con fines académicos y de portafolio.

- Licencia: MIT — ver el archivo `LICENSE` en la raíz del repositorio.

Autor: Ramiro Ottone Villar
