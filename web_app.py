from flask import Flask, request, jsonify, send_from_directory, Response, redirect
import os
import hashlib
from datetime import datetime
from pathlib import Path
from chatbot_core import ChatBot, stamp, is_night
from twilio.twiml.messaging_response import MessagingResponse
from database import get_or_create_user, update_user_fields, get_user, create_link_token, claim_link_token

import json
from visualizations import (
    grafico_presupuesto, grafico_interes_compuesto,
    grafico_comparacion_inversiones
)
from calculators import presupuesto_50_30_20, calcular_interes_compuesto


app = Flask(__name__, static_folder=str(Path(__file__).parent))
# Diccionario de bots por usuario para mantener estado conversacional
user_bots = {}
BASE_DIR = Path(__file__).parent


@app.get("/health")
def health():
    """Endpoint simple de estado para healthchecks"""
    return jsonify({"status": "ok"})


@app.get("/api/user")
def api_user_get():
    """Devuelve el perfil del usuario vigente (cookie 'uid')."""
    uid = request.cookies.get('uid')
    user = get_user(uid) if uid else None
    if not user:
        return jsonify({"exists": False})
    return jsonify({
        "exists": True,
        "phone": user.phone,
        "name": user.name,
        "monthly_income": user.monthly_income,
        "total_debt": user.total_debt,
        "savings_goal": user.savings_goal,
        "current_savings": user.current_savings,
        "risk_profile": user.risk_profile,
        "last_interaction": user.last_interaction.isoformat() if user.last_interaction else None,
    })


@app.post("/api/login")
def api_login():
    """Login simple: acepta DNI o nickname y fija cookie 'uid'."""
    data = request.get_json(silent=True) or {}
    dni = (data.get('dni') or '').strip()
    nick = (data.get('nickname') or '').strip()
    name = (data.get('name') or '').strip() or None

    user_id = None
    if dni:
        # DNI solo dígitos
        clean = ''.join(ch for ch in dni if ch.isdigit())
        if not clean:
            return jsonify({"error": "DNI inválido"}), 400
        user_id = f"dni:{clean}"
    elif nick:
        if len(nick) < 3:
            return jsonify({"error": "El nickname debe tener al menos 3 caracteres"}), 400
        user_id = f"nick:{nick.lower()}"
    else:
        return jsonify({"error": "Debes enviar 'dni' o 'nickname'"}), 400

    # Crear/actualizar perfil
    user = get_or_create_user(user_id, name=name)
    if name and not user.name:
        update_user_fields(user_id, name=name)

    resp = jsonify({"ok": True, "uid": user_id})
    resp.set_cookie('uid', user_id, max_age=60*60*24*365, samesite='Lax')
    return resp


@app.post("/api/logout")
def api_logout():
    resp = jsonify({"ok": True})
    resp.delete_cookie('uid')
    return resp


@app.get("/")
def index():
    # Sirve el HTML simple del chat
    return send_from_directory(BASE_DIR, "chat.html")


@app.post("/api/chat")
def api_chat():
    data = request.get_json(silent=True) or {}
    text = (data.get("message") or "").strip()
    when_str = (data.get("when") or "").strip()

    if not text:
        return jsonify({"error": "message vacío"}), 400

    when = None
    if when_str:
        try:
            # Acepta formato ISO o HH:MM del día actual
            if len(when_str) <= 5 and ":" in when_str:
                now = datetime.now()
                hh, mm = when_str.split(":")
                when = now.replace(hour=int(hh), minute=int(mm), second=0, microsecond=0)
            else:
                when = datetime.fromisoformat(when_str)
        except Exception:
            when = None

    # Identidad del usuario web por cookie 'uid'
    uid = request.cookies.get('uid')
    if not uid:
        # Generar uid simple basado en hora y hash
        uid = f"web_{hashlib.sha1(str(datetime.now().timestamp()).encode()).hexdigest()[:10]}"
    
    # Obtener o crear bot específico para este usuario
    if uid not in user_bots:
        user_bots[uid] = ChatBot()
        user_bots[uid].user_phone = uid
    bot = user_bots[uid]
    
    # Vincular al bot y garantizar perfil en DB
    get_or_create_user(uid)

    res = bot.process(text, when=when)
    periodo = "noche" if is_night(res.when) else "día"
    resp = jsonify({
        "reply": res.reply,
        "scenario": res.scenario,
        "timestamp": res.when.isoformat(timespec='seconds'),
        "period": periodo,
        "sentiment": res.sentiment,
        "emotion": res.emotion,
    })
    # Asegurar que el cliente mantenga la cookie
    if not request.cookies.get('uid'):
        resp.set_cookie('uid', uid, max_age=60*60*24*365, samesite='Lax')
    return resp


@app.get("/debug")
def debug_info():
    """Devuelve información para verificar la carpeta activa en el contenedor."""
    BASE = BASE_DIR

    def file_meta(p: Path):
        try:
            data = p.read_bytes()
            return {
                "exists": True,
                "size": len(data),
                "mtime": p.stat().st_mtime,
                "sha1": hashlib.sha1(data).hexdigest()[:12],
                "path": str(p)
            }
        except FileNotFoundError:
            return {"exists": False, "path": str(p)}

    files = ["web_app.py", "chatbot_core.py", "calculators.py", "database.py", "chat.html"]
    meta = {f: file_meta(BASE / f) for f in files}

    return jsonify({
        "cwd": os.getcwd(),
        "base_dir": str(BASE),
        "list_py": sorted([f for f in os.listdir(BASE) if f.endswith('.py')]),
        "meta": meta
    })


@app.get("/dashboard")
def dashboard():
    """Página de dashboard con visualizaciones"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Dashboard Financiero</title>
        <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
        <style>
            * { box-sizing: border-box; }
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; margin: 0; padding: 15px; background: #f5f5f5; }
            h1 { color: #333; text-align: center; font-size: 24px; margin: 10px 0 20px; }
            h2 { font-size: 18px; margin: 0 0 15px; color: #333; }
            .container { max-width: 1200px; margin: 0 auto; }
            .chart { background: white; padding: 16px; margin: 0 0 16px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .form-group { margin: 12px 0; }
            label { display: block; margin-bottom: 5px; font-weight: 600; font-size: 14px; }
            input { padding: 10px; width: 100%; max-width: 300px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px; }
            button { padding: 10px 20px; background: #45B7D1; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 15px; font-weight: 500; margin-top: 8px; }
            button:hover { background: #3a9db5; }
            button:active { transform: scale(0.98); }
            .back-link { display: inline-block; padding: 12px 24px; background: #4ECDC4; color: white; text-decoration: none; border-radius: 8px; font-size: 16px; font-weight: 500; margin: 20px 0; }
            .back-link:hover { background: #42b8ad; }
            .form-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 12px; }

            @media (max-width: 768px) {
                body { padding: 10px; }
                h1 { font-size: 20px; margin: 5px 0 15px; }
                h2 { font-size: 16px; margin: 0 0 10px; }
                .chart { padding: 12px; margin: 0 0 12px; }
                input { max-width: 100%; font-size: 16px; }
                button { width: 100%; padding: 12px; }
                .form-row { grid-template-columns: 1fr; gap: 10px; }
                .back-link { display: block; text-align: center; width: 100%; padding: 14px; }
            }

            @media (max-width: 480px) {
                body { padding: 8px; }
                h1 { font-size: 18px; }
                h2 { font-size: 15px; }
                .chart { padding: 10px; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>💰 Dashboard Financiero Personal</h1>
            
            <div class="chart">
                <h2>📊 Simulador de Presupuesto</h2>
                <div class="form-group">
                    <label>Ingreso Mensual:</label>
                    <input type="number" id="ingreso" value="50000" />
                    <button onclick="actualizarPresupuesto()">Calcular</button>
                </div>
                <div id="chart-presupuesto"></div>
            </div>
            
            <div class="chart">
                <h2>📈 Simulador de Inversión (Interés Compuesto)</h2>
                <div class="form-row">
                    <div class="form-group">
                        <label>Capital Inicial ($):</label>
                        <input type="number" id="capital" value="10000" />
                    </div>
                    <div class="form-group">
                        <label>Tasa Anual (%):</label>
                        <input type="number" id="tasa" value="12" />
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Años:</label>
                        <input type="number" id="años" value="5" />
                    </div>
                    <div class="form-group">
                        <label>Aporte Mensual ($):</label>
                        <input type="number" id="aporte" value="1000" />
                    </div>
                </div>
                <button onclick="actualizarInversion()">Simular</button>
                <div id="chart-inversion"></div>
            </div>
            
            <div class="chart">
                <h2>⚖️ Comparación de Inversiones</h2>
                <div class="form-row">
                    <div class="form-group">
                        <label>Monto a Invertir ($):</label>
                        <input type="number" id="monto-comp" value="100000" />
                    </div>
                    <div class="form-group">
                        <label>Años:</label>
                        <input type="number" id="años-comp" value="10" />
                    </div>
                </div>
                <button onclick="actualizarComparacion()">Comparar</button>
                <div id="chart-comparacion"></div>
            </div>
            
            <div style="text-align: center; margin: 30px 0 10px;">
                <a href="/" class="back-link">
                    💬 Volver al Chat
                </a>
            </div>
        </div>
        
        <script>
            // Make charts responsive
            const config = { responsive: true, displayModeBar: false };

            async function cargarPerfil() {
                try {
                    const r = await fetch('/api/user');
                    const u = await r.json();
                    if (u && u.exists && u.monthly_income) {
                        const ingresoEl = document.getElementById('ingreso');
                        if (ingresoEl) ingresoEl.value = Math.round(u.monthly_income);
                    }
                } catch (e) { /* no-op */ }
            }

            function actualizarPresupuesto() {
                const ingreso = parseFloat(document.getElementById('ingreso').value);
                fetch(`/api/grafico/presupuesto?ingreso=${ingreso}`)
                    .then(r => r.json())
                    .then(data => {
                        Plotly.newPlot('chart-presupuesto', data.data, data.layout, config);
                    });
            }
            
            function actualizarInversion() {
                const capital = parseFloat(document.getElementById('capital').value);
                const tasa = parseFloat(document.getElementById('tasa').value);
                const años = parseInt(document.getElementById('años').value);
                const aporte = parseFloat(document.getElementById('aporte').value);
                
                fetch(`/api/grafico/inversion?capital=${capital}&tasa=${tasa}&años=${años}&aporte=${aporte}`)
                    .then(r => r.json())
                    .then(data => {
                        Plotly.newPlot('chart-inversion', data.data, data.layout, config);
                    });
            }
            
            function actualizarComparacion() {
                const monto = parseFloat(document.getElementById('monto-comp').value);
                const años = parseInt(document.getElementById('años-comp').value);
                
                fetch(`/api/grafico/comparacion?monto=${monto}&años=${años}`)
                    .then(r => r.json())
                    .then(data => {
                        Plotly.newPlot('chart-comparacion', data.data, data.layout, config);
                    });
            }
            
            // Cargar perfil y gráficos iniciales
            cargarPerfil().then(() => actualizarPresupuesto());
            actualizarInversion();
            actualizarComparacion();
        </script>
    </body>
    </html>
    """
    return html


@app.get("/api/grafico/presupuesto")
def api_grafico_presupuesto():
    """Genera gráfico de presupuesto"""
    # Usar ingreso del usuario si existe y no se especifica en query
    ingreso_arg = request.args.get('ingreso')
    if ingreso_arg is not None:
        ingreso = float(ingreso_arg)
    else:
        uid = request.cookies.get('uid')
        user = get_user(uid) if uid else None
        ingreso = float(user.monthly_income) if user and user.monthly_income else 50000.0
    dist = presupuesto_50_30_20(ingreso)
    grafico_json = grafico_presupuesto(
        dist['necesidades_basicas'],
        dist['gastos_personales'],
        dist['ahorro_inversion']
    )
    return jsonify(json.loads(grafico_json))


@app.get("/api/grafico/inversion")
def api_grafico_inversion():
    """Genera gráfico de interés compuesto"""
    capital = float(request.args.get('capital', 10000))
    tasa = float(request.args.get('tasa', 12))
    años = int(request.args.get('años', 5))
    aporte = float(request.args.get('aporte', 0))
    
    grafico_json = grafico_interes_compuesto(capital, tasa, años, aporte)
    return jsonify(json.loads(grafico_json))


@app.get("/api/grafico/comparacion")
def api_grafico_comparacion():
    """Genera gráfico de comparación de inversiones"""
    monto = float(request.args.get('monto', 100000))
    años = int(request.args.get('años', 10))
    
    grafico_json = grafico_comparacion_inversiones(monto, años)
    return jsonify(json.loads(grafico_json))


# --- WhatsApp (Twilio) Webhook ---
# Configura la URL del webhook en el sandbox/productivo de WhatsApp de Twilio apuntando a
# https://TU_DOMINIO_PUBLICO/whatsapp-webhook
@app.post("/whatsapp-webhook")
def whatsapp_webhook():
    """Webhook para mensajes entrantes de WhatsApp (Twilio).
    Lee el cuerpo del mensaje y responde con TwiML.
    """
    body = (request.form.get("Body") or "").strip()
    # Datos opcionales que envía Twilio
    wa_from = request.form.get("From", "")  # ej.: whatsapp:+1415xxxxxxx

    if not body:
        # Responder vacío evita reintentos innecesarios
        return Response("", status=204)

    # Normalizar id del usuario desde WhatsApp
    user_id = wa_from or "whatsapp_unknown"
    
    # Obtener o crear bot específico para este usuario de WhatsApp
    if user_id not in user_bots:
        user_bots[user_id] = ChatBot()
        user_bots[user_id].user_phone = user_id
    bot = user_bots[user_id]
    
    get_or_create_user(user_id)

    # Detectar solicitud de vinculación con la web/dashboard
    lower = body.lower()
    if any(k in lower for k in ["vincular", "vinculación", "vinculacion", "link", "enlace", "dashboard", "web"]):
        token = create_link_token(user_id, ttl_minutes=15)
        link = f"{request.url_root.rstrip('/')}/claim/{token}"
        twiml = MessagingResponse()
        twiml.message(
            "Para ver tu dashboard con tus datos, abrí este enlace (válido por 15 minutos):\n" + link
        )
        return Response(str(twiml), mimetype="application/xml")

    res = bot.process(body)
    twiml = MessagingResponse()
    twiml.message(res.reply)
    return Response(str(twiml), mimetype="application/xml")


@app.get("/claim/<token>")
def claim_token(token: str):
    """Consume un token de vinculación y establece cookie 'uid' al teléfono."""
    phone = claim_link_token(token)
    if not phone:
        return Response("Token inválido o expirado", status=400)
    resp = redirect("/dashboard")
    resp.set_cookie('uid', phone, max_age=60*60*24*365, samesite='Lax')
    return resp


if __name__ == "__main__":
    # Ejecuta el servidor accesible desde cualquier interfaz de red
    debug_enabled = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug_enabled)

    