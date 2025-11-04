import re

def test_parsing():
    text = "2 años"
    t = text.lower()
    
    # Extraer números y desambiguar horizonte vs monto
    nums_raw = re.findall(r"\d+(?:[.,]\d+)?", text)
    nums = [float(n.replace('.', '').replace(',', '')) for n in nums_raw]
    print(f"Text: '{text}'")
    print(f"Nums raw: {nums_raw}")
    print(f"Nums: {nums}")
    
    # CRÍTICO: Detectar primero si hay palabras temporales
    tiene_mes = any(k in t for k in ["mes", "meses", "m."])
    tiene_ano = any(k in t for k in ["año", "años", "anio", "anios", "a."])
    print(f"Tiene mes: {tiene_mes}")
    print(f"Tiene año: {tiene_ano}")
    
    horizonte_meses = None
    
    if tiene_ano:
        candidatos = [int(x) for x in nums if x <= 50]  # hasta 50 años
        print(f"Candidatos años: {candidatos}")
        if candidatos:
            horizonte_meses = candidatos[0] * 12
            # Remover de nums para no confundir con monto
            nums = [x for x in nums if x != candidatos[0]]
            print(f"Horizonte meses: {horizonte_meses}")
            print(f"Nums after removal: {nums}")

if __name__ == "__main__":
    test_parsing()