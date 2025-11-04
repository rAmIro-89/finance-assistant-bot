#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard HTML estático para análisis de logs
Genera un archivo HTML que puedes abrir localmente sin servidor
"""

import csv
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
import json

def generate_dashboard():
    """Genera un dashboard HTML con estadísticas de los logs"""
    
    log_path = Path(__file__).parent / "chat_logs.csv"
    
    if not log_path.exists():
        print("❌ No se encontró chat_logs.csv")
        print("   Ejecuta sync_logs_from_nas.bat primero")
        return
    
    # Leer logs
    with open(log_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        logs = list(reader)
    
    print(f"📊 Analizando {len(logs)} interacciones...")
    
    # Análisis
    scenarios = Counter(log['scenario'] for log in logs)
    sentiments = Counter(log['sentiment'] for log in logs)
    emotions = Counter(log['emotion'] for log in logs if log['emotion'] != 'none')
    
    # Actividad por hora
    hours = defaultdict(int)
    for log in logs:
        try:
            dt = datetime.fromisoformat(log['timestamp'])
            hours[dt.hour] += 1
        except:
            pass
    
    # Detectar pérdida de contexto
    perdidas = []
    for i in range(1, len(logs)):
        prev = logs[i-1]
        curr = logs[i]
        user_msg = curr['user'].strip().lower()
        
        if (len(user_msg.split()) <= 3 and 
            curr['scenario'] == 'ayuda' and 
            prev['scenario'] != 'ayuda' and
            prev['scenario'] in ['ahorro', 'presupuesto', 'deudas', 'inversiones']):
            perdidas.append({
                'timestamp': curr['timestamp'][:16],
                'prev_scenario': prev['scenario'],
                'prev_user': prev['user'][:50],
                'curr_user': curr['user'],
            })
    
    # Mensajes no entendidos
    ayuda_msgs = [log['user'].lower().strip() for log in logs if log['scenario'] == 'ayuda']
    saludos = ['hola', 'buenos dias', 'buenas tardes', 'buenas noches', 'hey', 'hi']
    ayuda_msgs = [msg for msg in ayuda_msgs if msg not in saludos and len(msg) > 2]
    msg_freq = Counter(ayuda_msgs)
    
    # Generar HTML
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Dashboard de Análisis - Bot Financiero</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        h1 {{
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 36px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .subtitle {{
            text-align: center;
            color: rgba(255,255,255,0.9);
            font-size: 18px;
            margin-bottom: 40px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            text-align: center;
            transition: transform 0.3s;
        }}
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        .stat-value {{
            font-size: 48px;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        .stat-label {{
            color: #666;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .chart-card {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }}
        .chart-title {{
            font-size: 24px;
            margin-bottom: 20px;
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        .alert {{
            background: #fff3cd;
            border: 2px solid #ffc107;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .alert-danger {{
            background: #f8d7da;
            border-color: #dc3545;
        }}
        .alert-success {{
            background: #d4edda;
            border-color: #28a745;
        }}
        .alert h3 {{
            margin-bottom: 10px;
            color: #333;
        }}
        .list {{
            list-style: none;
            padding: 0;
        }}
        .list li {{
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 5px;
            font-size: 12px;
            font-weight: bold;
            margin-right: 8px;
        }}
        .badge-primary {{ background: #667eea; color: white; }}
        .badge-success {{ background: #28a745; color: white; }}
        .badge-danger {{ background: #dc3545; color: white; }}
        .badge-warning {{ background: #ffc107; color: #333; }}
        .footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Dashboard de Análisis del Bot</h1>
        <div class="subtitle">
            Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}<br>
            Total de interacciones analizadas: {len(logs)}
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{len(logs)}</div>
                <div class="stat-label">Total Interacciones</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{scenarios.get('inversiones', 0)}</div>
                <div class="stat-label">📈 Inversiones</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{scenarios.get('presupuesto', 0)}</div>
                <div class="stat-label">📊 Presupuestos</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{scenarios.get('ahorro', 0)}</div>
                <div class="stat-label">🏦 Ahorros</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{scenarios.get('deudas', 0)}</div>
                <div class="stat-label">💳 Deudas</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{scenarios.get('ayuda', 0)}</div>
                <div class="stat-label">❓ Sin clasificar</div>
            </div>
        </div>
        
        {'<div class="alert alert-danger"><h3>⚠️ PÉRDIDA DE CONTEXTO DETECTADA</h3><p>Se detectaron <strong>' + str(len(perdidas)) + '</strong> casos donde el bot perdió el contexto de la conversación.</p><ul class="list">' + ''.join(f'<li><span class="badge badge-danger">{p["prev_scenario"]}</span> "{p["prev_user"]}" → "{p["curr_user"]}" (no entendido)</li>' for p in perdidas[:5]) + '</ul></div>' if len(perdidas) > 0 else '<div class="alert alert-success"><h3>✅ Contexto Funcionando Bien</h3><p>No se detectaron pérdidas de contexto significativas.</p></div>'}
        
        <div class="chart-card">
            <h2 class="chart-title">📊 Distribución por Escenario</h2>
            <div id="chart-scenarios"></div>
        </div>
        
        <div class="chart-card">
            <h2 class="chart-title">😊 Análisis de Sentimientos</h2>
            <div id="chart-sentiments"></div>
        </div>
        
        <div class="chart-card">
            <h2 class="chart-title">🕐 Actividad por Hora del Día</h2>
            <div id="chart-hours"></div>
        </div>
        
        {f'''<div class="chart-card">
            <h2 class="chart-title">💭 Top 10 Mensajes No Entendidos</h2>
            <ul class="list">
                {''.join(f'<li><span class="badge badge-warning">{count}x</span> {msg[:80]}</li>' for msg, count in msg_freq.most_common(10))}
            </ul>
        </div>''' if len(ayuda_msgs) > 0 else ''}
        
        <div class="footer">
            <p>🔒 Este análisis es privado y NO se sube a GitHub</p>
            <p>Ejecuta <code>sync_logs_from_nas.bat</code> para actualizar los datos</p>
        </div>
    </div>
    
    <script>
        // Gráfico de escenarios
        var dataScenarios = {{
            labels: {json.dumps([k for k, v in scenarios.most_common()])},
            values: {json.dumps([v for k, v in scenarios.most_common()])},
            type: 'pie',
            marker: {{
                colors: ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a']
            }}
        }};
        
        var layoutScenarios = {{
            height: 400,
            margin: {{ t: 0, b: 0, l: 0, r: 0 }}
        }};
        
        Plotly.newPlot('chart-scenarios', [dataScenarios], layoutScenarios, {{displayModeBar: false}});
        
        // Gráfico de sentimientos
        var dataSentiments = {{
            x: {json.dumps([k for k, v in sentiments.items()])},
            y: {json.dumps([v for k, v in sentiments.items()])},
            type: 'bar',
            marker: {{
                color: ['#28a745', '#dc3545', '#6c757d'],
            }}
        }};
        
        var layoutSentiments = {{
            height: 400,
            xaxis: {{ title: 'Sentimiento' }},
            yaxis: {{ title: 'Cantidad' }},
            margin: {{ t: 20, b: 60, l: 60, r: 20 }}
        }};
        
        Plotly.newPlot('chart-sentiments', [dataSentiments], layoutSentiments, {{displayModeBar: false}});
        
        // Gráfico de horas
        var dataHours = {{
            x: {json.dumps([f'{h:02d}:00' for h in sorted(hours.keys())])},
            y: {json.dumps([hours[h] for h in sorted(hours.keys())])},
            type: 'bar',
            marker: {{
                color: '#667eea',
            }}
        }};
        
        var layoutHours = {{
            height: 400,
            xaxis: {{ title: 'Hora del día' }},
            yaxis: {{ title: 'Interacciones' }},
            margin: {{ t: 20, b: 60, l: 60, r: 20 }}
        }};
        
        Plotly.newPlot('chart-hours', [dataHours], layoutHours, {{displayModeBar: false}});
    </script>
</body>
</html>"""
    
    # Guardar HTML
    output_path = Path(__file__).parent / "logs_dashboard.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ Dashboard generado: {output_path}")
    print(f"\n   Abre el archivo en tu navegador:")
    print(f"   file:///{output_path.absolute()}")
    print(f"\n   O ejecuta: start {output_path.name}")
    
    # Abrir automáticamente
    import webbrowser
    webbrowser.open(str(output_path.absolute()))

if __name__ == "__main__":
    generate_dashboard()
