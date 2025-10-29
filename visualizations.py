"""
Módulo de visualizaciones y gráficos financieros
"""
import plotly.graph_objects as go
import json


def grafico_presupuesto(necesidades: float, personales: float, ahorro: float) -> str:
    """
    Genera gráfico de pastel para distribución de presupuesto.
    Retorna JSON para Plotly.js
    """
    fig = go.Figure(data=[go.Pie(
        labels=['Necesidades Básicas (50%)', 'Gastos Personales (30%)', 'Ahorro/Inversión (20%)'],
        values=[necesidades, personales, ahorro],
        marker=dict(colors=['#FF6B6B', '#4ECDC4', '#45B7D1']),
        textinfo='label+percent+value',
        texttemplate='%{label}<br>$%{value:,.0f}<br>%{percent}',
        hovertemplate='%{label}<br>$%{value:,.2f}<br>%{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title='Distribución de Presupuesto (Regla 50/30/20)',
        showlegend=True,
        height=400
    )
    
    return fig.to_json()


def grafico_interes_compuesto(capital: float, tasa: float, años: int, aporte_mensual: float = 0) -> str:
    """
    Genera gráfico de crecimiento con interés compuesto.
    """
    meses = años * 12
    tasa_mensual = (tasa / 100) / 12
    
    # Calcular valores mes a mes
    meses_list = list(range(0, meses + 1))
    valores = []
    invertido_total = []
    
    monto = capital
    inv_acum = capital
    
    valores.append(capital)
    invertido_total.append(capital)
    
    for mes in range(1, meses + 1):
        monto = monto * (1 + tasa_mensual) + aporte_mensual
        inv_acum += aporte_mensual
        valores.append(monto)
        invertido_total.append(inv_acum)
    
    fig = go.Figure()
    
    # Línea de monto con interés
    fig.add_trace(go.Scatter(
        x=meses_list,
        y=valores,
        mode='lines',
        name='Con Interés Compuesto',
        line=dict(color='#45B7D1', width=3),
        fill='tozeroy',
        fillcolor='rgba(69, 183, 209, 0.2)'
    ))
    
    # Línea de inversión sin interés
    fig.add_trace(go.Scatter(
        x=meses_list,
        y=invertido_total,
        mode='lines',
        name='Sin Interés (solo aportes)',
        line=dict(color='#FF6B6B', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title=f'Crecimiento con Interés Compuesto ({tasa}% anual)',
        xaxis_title='Meses',
        yaxis_title='Monto ($)',
        hovermode='x unified',
        height=400
    )
    
    return fig.to_json()


def grafico_comparacion_inversiones(monto: float, años: int) -> str:
    """
    Compara rendimiento de diferentes inversiones.
    """
    opciones = [
        {"nombre": "Plazo Fijo", "tasa": 8.0},
        {"nombre": "FCI", "tasa": 10.0},
        {"nombre": "Bonos", "tasa": 12.0},
        {"nombre": "ETF", "tasa": 18.0},
        {"nombre": "Acciones", "tasa": 25.0},
    ]
    
    nombres = []
    valores_finales = []
    ganancias = []
    
    for op in opciones:
        tasa_mensual = (op["tasa"] / 100) / 12
        meses = años * 12
        valor_final = monto * ((1 + tasa_mensual) ** meses)
        ganancia = valor_final - monto
        
        nombres.append(op["nombre"])
        valores_finales.append(valor_final)
        ganancias.append(ganancia)
    
    fig = go.Figure(data=[
        go.Bar(
            x=nombres,
            y=valores_finales,
            text=[f'${v:,.0f}' for v in valores_finales],
            textposition='auto',
            marker=dict(color=['#95E1D3', '#F38181', '#AA96DA', '#FCBAD3', '#FFFFD2'])
        )
    ])
    
    fig.update_layout(
        title=f'Comparación de Inversiones (${monto:,.0f} por {años} años)',
        xaxis_title='Tipo de Inversión',
        yaxis_title='Monto Final ($)',
        showlegend=False,
        height=400
    )
    
    return fig.to_json()