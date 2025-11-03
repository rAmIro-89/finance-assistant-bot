import json
import glob

# Buscar todos los archivos de resultados de test
result_files = glob.glob("*_results.json")

summary = {}
for file in result_files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    total = len(data)
    success = 0
    errors = 0
    for item in data:
        # Considera éxito si status 200 y hay respuesta
        if isinstance(item, dict):
            if item.get("status") == 200 and item.get("reply"):
                success += 1
            elif item.get("error"):
                errors += 1
    summary[file] = {
        "total": total,
        "success": success,
        "errors": errors,
        "success_rate": round(success/total*100,2) if total else 0
    }

with open("errors_report.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print("Reporte generado en errors_report.json")
