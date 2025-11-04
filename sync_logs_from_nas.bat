@echo off
REM ============================================================================
REM Script para descargar logs desde el NAS para análisis local
REM Los logs NO se suben a GitHub por privacidad
REM ============================================================================

echo.
echo ========================================
echo  SINCRONIZAR LOGS DESDE NAS
echo ========================================
echo.

REM Verificar que Y: esté mapeado
if not exist Y:\deploy-nas (
    echo ERROR: La unidad Y: no esta mapeada
    echo.
    echo Ejecuta primero: mapear_nas_abrir_vscode.bat
    pause
    exit /b 1
)

REM Verificar que exista chat_logs.csv en el NAS
if not exist Y:\deploy-nas\chat_logs.csv (
    echo ADVERTENCIA: No se encontro chat_logs.csv en el NAS
    echo Puede que aun no haya interacciones registradas
    pause
    exit /b 0
)

REM Crear backup del log local si existe
if exist chat_logs.csv (
    echo Creando backup del log local...
    copy /Y chat_logs.csv chat_logs_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%.csv >nul
    echo   [OK] Backup creado
)

REM Copiar log desde NAS
echo.
echo Descargando logs desde el NAS...
copy /Y Y:\deploy-nas\chat_logs.csv chat_logs.csv >nul
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Logs sincronizados correctamente
) else (
    echo   [ERROR] No se pudo copiar el archivo
    pause
    exit /b 1
)

REM Mostrar estadísticas rápidas
echo.
echo ========================================
echo  ESTADISTICAS DEL LOG
echo ========================================
for /f %%A in ('find /c /v "" ^< chat_logs.csv') do set lines=%%A
set /a interactions=%lines%-1
echo Total de interacciones: %interactions%
echo.

REM Preguntar si quiere analizar
echo Deseas analizar los logs ahora? (S/N)
choice /C SN /N /M "Opcion: "
if %ERRORLEVEL% EQU 1 (
    echo.
    echo Ejecutando analisis...
    python analyze_logs.py
)

echo.
echo ========================================
echo  SINCRONIZACION COMPLETADA
echo ========================================
echo.
echo Los logs estan en: %CD%\chat_logs.csv
echo Este archivo NO se sube a GitHub (privacidad)
echo.
pause
