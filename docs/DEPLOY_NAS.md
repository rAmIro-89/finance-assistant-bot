# Despliegue en NAS (Guía Única y Concisa)

Esta guía resume cómo correr el bot en tu NAS (ASUSTOR, Synology, QNAP, TrueNAS o similar), exponerlo en internet y conectarlo a WhatsApp.

## Requisitos

- Docker y docker-compose instalados en el NAS
- Terminal/SSH habilitado
- Puerto 5000 libre (o el que prefieras mapear)
- RAM libre recomendada: 512 MB+

## Estructura de carpetas en el NAS

Crea una carpeta, por ejemplo:

- /volume1/docker/chatbot (Synology/ASUSTOR)
- /share/Container/chatbot (QNAP)
- /mnt/pool/chatbot (TrueNAS)

Dentro de esa carpeta coloca los archivos del proyecto (Dockerfile, docker-compose.yml, código fuente y requirements.txt). Asegúrate de tener un subdirectorio `data/` para la base de datos.

## Despliegue básico (Docker Compose)

1) Copia los archivos del proyecto a la carpeta en tu NAS.
2) Entra por SSH a esa carpeta y ejecuta:

```bash
# Construir e iniciar en segundo plano
docker-compose up -d

# Ver logs
docker logs -f chatbot-financiero
```

3) Prueba local:

```bash
curl http://localhost:5000/health
```

Si responde `{"status":"ok"}`, está corriendo.

4) Prueba desde tu PC (en la misma red):

```powershell
curl http://IP_DEL_NAS:5000
```

## Acceso externo (elige 1)

- Port Forwarding en tu router: abre el puerto externo 5000 hacia IP_NAS:5000.
- Reverse Proxy + HTTPS del propio NAS (recomendado): crea un host (ej. subdominio) que apunte a `localhost:5000` y aplica Let’s Encrypt.
- Ngrok (sin tocar router): usa `docker-compose-with-ngrok.yml`, crea un `.env` con `NGROK_AUTHTOKEN` y levanta el túnel. La URL pública estará en `http://IP_NAS:4040`.

## WhatsApp (Twilio)

- Configura en Twilio (Sandbox o número verificado) el webhook de recepción con tu URL pública:
  - `http(s)://TU_DOMINIO/whatsapp-webhook`
- Para vincular tu sesión web con tu número de WhatsApp: envía “vincular” en el chat de WhatsApp. Te devolverá un enlace único válido por 15 minutos; ábrelo y te redirige al dashboard con tu sesión ya vinculada.

## Operación habitual

- Ver estado: `GET /health`
- Chat web: `GET /` (chat.html)
- API chat: `POST /api/chat`
- Dashboard: `GET /dashboard`
- Perfil actual: `GET /api/user`
- Login web: `POST /api/login` (dni o nickname)
- Logout web: `POST /api/logout`

## Persistencia

- Base de datos SQLite en `data/`
- Logs de chat en `chat_logs.csv` (mapeado por volumen)

## Troubleshooting rápido

- Contenedor no inicia: `docker logs chatbot-financiero`
- No se accede desde fuera: revisar firewall del NAS, port forwarding o ngrok.
- Healthcheck falla: prueba `http://IP_NAS:5000/health` y revisa puertos.

## Seguridad

- Usa HTTPS (reverse proxy del NAS o dominio propio con certificado)
- Mantén tokens/secretos fuera del repo (usa variables de entorno o .env)
- Limita el puerto expuesto solo a lo necesario

---

Para detalles específicos de cada marca (ASUSTOR, Synology, QNAP, TrueNAS), los pasos son equivalentes: crear carpeta, copiar archivos, `docker-compose up -d`, y luego elegir cómo exponer al exterior.
