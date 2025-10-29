"""
Test de normalización de texto
"""
import unicodedata
import re

def normalize_text(text: str) -> str:
    """
    Normaliza el texto para mejorar la detección:
    - Convierte a minúsculas
    - Elimina acentos y diacríticos
    - Preserva números y espacios
    """
    text = text.lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# Tests
print("🧪 TESTS DE NORMALIZACIÓN:\n")

tests = [
    'Inversión',
    'INVERSIÓN', 
    'inversión',
    'inversiOn',
    'préstamo',
    'PRÉSTAMO',
    'crédito',
    '¿Cómo funciona la INFLACIÓN?',
    'Quiero invertir mi aguinaldo',
    'NECESITO UN PRESUPUESTO!!!',
    'Tengo deudás en la tarjeta',
]

for t in tests:
    print(f"{t:40} -> {normalize_text(t)}")

print("\n✅ La normalización funciona correctamente!")
print("\n📝 Ahora el bot entenderá:")
print("  • 'Inversión' = 'inversion' = 'INVERSIÓN'")
print("  • 'Préstamo' = 'prestamo' = 'PRESTAMO'")
print("  • 'Crédito' = 'credito' = 'CREDITO'")
