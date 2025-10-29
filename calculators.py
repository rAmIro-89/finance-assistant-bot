"""
Calculadoras financieras avanzadas
"""
import math
from typing import Dict, List


def calcular_interes_compuesto(capital: float, tasa_anual: float, años: float, 
                                aporte_mensual: float = 0) -> Dict:
    """
    Calcula interés compuesto con aportes mensuales opcionales.
    
    Args:
        capital: Capital inicial
        tasa_anual: Tasa de interés anual (ej: 10 para 10%)
        años: Años de inversión
        aporte_mensual: Aporte mensual adicional
    
    Returns:
        Dict con monto final, total invertido, ganancia
    """
    tasa_mensual = (tasa_anual / 100) / 12
    meses = int(años * 12)
    
    monto = capital
    total_invertido = capital
    
    for mes in range(meses):
        monto = monto * (1 + tasa_mensual) + aporte_mensual
        total_invertido += aporte_mensual
    
    ganancia = monto - total_invertido
    
    return {
        "monto_final": round(monto, 2),
        "total_invertido": round(total_invertido, 2),
        "ganancia": round(ganancia, 2),
        "rendimiento_porcentaje": round((ganancia / total_invertido) * 100, 2)
    }


def calcular_cuota_prestamo(monto: float, tasa_anual: float, meses: int) -> Dict:
    """
    Calcula cuota mensual de un préstamo (sistema francés).
    
    Args:
        monto: Monto del préstamo
        tasa_anual: Tasa de interés anual (ej: 50 para 50%)
        meses: Plazo en meses
    
    Returns:
        Dict con cuota mensual, total a pagar, intereses totales
    """
    tasa_mensual = (tasa_anual / 100) / 12
    
    if tasa_mensual == 0:
        cuota = monto / meses
    else:
        cuota = monto * (tasa_mensual * (1 + tasa_mensual)**meses) / \
                ((1 + tasa_mensual)**meses - 1)
    
    total_pagar = cuota * meses
    intereses = total_pagar - monto
    
    return {
        "cuota_mensual": round(cuota, 2),
        "total_a_pagar": round(total_pagar, 2),
        "intereses_totales": round(intereses, 2)
    }


def plan_ahorro(objetivo: float, meses: int, ingreso_mensual: float = None) -> Dict:
    """
    Calcula plan de ahorro para alcanzar objetivo.
    
    Args:
        objetivo: Monto objetivo a ahorrar
        meses: Plazo en meses
        ingreso_mensual: Ingreso mensual (opcional, para calcular porcentaje)
    
    Returns:
        Dict con ahorro mensual necesario, porcentaje del ingreso
    """
    ahorro_mensual = objetivo / meses
    
    result = {
        "ahorro_mensual": round(ahorro_mensual, 2),
        "monto_objetivo": objetivo,
        "plazo_meses": meses
    }
    
    if ingreso_mensual:
        porcentaje = (ahorro_mensual / ingreso_mensual) * 100
        result["porcentaje_ingreso"] = round(porcentaje, 2)
        result["factibilidad"] = "Excelente" if porcentaje < 20 else \
                                 "Bueno" if porcentaje < 30 else \
                                 "Desafiante" if porcentaje < 40 else "Muy difícil"
    
    return result


def tiempo_pagar_deuda(deuda: float, pago_mensual: float, tasa_anual: float = 0) -> Dict:
    """
    Calcula cuánto tiempo tomará pagar una deuda.
    
    Args:
        deuda: Monto de la deuda
        pago_mensual: Cuánto pagas por mes
        tasa_anual: Tasa de interés anual (0 si no hay interés)
    
    Returns:
        Dict con meses necesarios, total pagado, intereses
    """
    if pago_mensual <= 0:
        return {"error": "El pago mensual debe ser mayor a 0"}
    
    tasa_mensual = (tasa_anual / 100) / 12
    
    if tasa_mensual == 0:
        meses = math.ceil(deuda / pago_mensual)
        total = deuda
        intereses = 0
    else:
        # Con interés
        if pago_mensual <= deuda * tasa_mensual:
            return {"error": "El pago mensual no cubre ni los intereses. Nunca terminarás de pagar."}
        
        meses = math.log(pago_mensual / (pago_mensual - deuda * tasa_mensual)) / math.log(1 + tasa_mensual)
        meses = math.ceil(meses)
        total = pago_mensual * meses
        intereses = total - deuda
    
    return {
        "meses_necesarios": meses,
        "años": round(meses / 12, 1),
        "total_a_pagar": round(total, 2),
        "intereses_totales": round(intereses, 2)
    }


def presupuesto_50_30_20(ingreso: float) -> Dict:
    """
    Calcula distribución de presupuesto según regla 50/30/20.
    
    Args:
        ingreso: Ingreso mensual
    
    Returns:
        Dict con distribución sugerida
    """
    return {
        "ingreso_mensual": ingreso,
        "necesidades_basicas": round(ingreso * 0.50, 2),
        "gastos_personales": round(ingreso * 0.30, 2),
        "ahorro_inversion": round(ingreso * 0.20, 2)
    }


def comparar_inversiones(monto: float, años: int) -> List[Dict]:
    """
    Compara diferentes opciones de inversión con el mismo monto y plazo.
    
    Args:
        monto: Monto a invertir
        años: Plazo en años
    
    Returns:
        Lista de opciones con rendimientos
    """
    opciones = [
        {"nombre": "Plazo Fijo", "tasa": 8.0, "riesgo": "Bajo"},
        {"nombre": "FCI Money Market", "tasa": 10.0, "riesgo": "Bajo"},
        {"nombre": "Bonos Corporativos", "tasa": 12.0, "riesgo": "Medio"},
        {"nombre": "Fondos Balanceados", "tasa": 15.0, "riesgo": "Medio"},
        {"nombre": "ETF S&P500", "tasa": 18.0, "riesgo": "Medio-Alto"},
        {"nombre": "Acciones Individuales", "tasa": 25.0, "riesgo": "Alto"},
        {"nombre": "Criptomonedas", "tasa": 50.0, "riesgo": "Muy Alto"},
    ]
    
    resultados = []
    for opcion in opciones:
        calc = calcular_interes_compuesto(monto, opcion["tasa"], años)
        resultados.append({
            "nombre": opcion["nombre"],
            "riesgo": opcion["riesgo"],
            "tasa_anual": opcion["tasa"],
            "monto_final": calc["monto_final"],
            "ganancia": calc["ganancia"]
        })
    
    return resultados


def jubilacion_estimada(edad_actual: int, edad_jubilacion: int, 
                        ahorro_mensual: float, tasa_anual: float = 12.0) -> Dict:
    """
    Estima cuánto tendrás para la jubilación.
    
    Args:
        edad_actual: Tu edad actual
        edad_jubilacion: Edad a la que te jubilas (ej: 65)
        ahorro_mensual: Cuánto ahorras por mes
        tasa_anual: Tasa de rendimiento anual estimada
    
    Returns:
        Dict con estimación de capital para jubilación
    """
    años = edad_jubilacion - edad_actual
    
    if años <= 0:
        return {"error": "Ya pasaste la edad de jubilación o la edad es inválida"}
    
    calc = calcular_interes_compuesto(0, tasa_anual, años, ahorro_mensual)
    
    # Estimar cuánto tiempo durará el capital (retiro 4% anual)
    retiro_mensual_seguro = (calc["monto_final"] * 0.04) / 12
    
    return {
        "años_hasta_jubilacion": años,
        "total_ahorrado": calc["total_invertido"],
        "capital_estimado": calc["monto_final"],
        "ganancia_intereses": calc["ganancia"],
        "retiro_mensual_seguro": round(retiro_mensual_seguro, 2),
        "nota": "Retiro seguro = 4% anual (regla conservadora)"
    }
