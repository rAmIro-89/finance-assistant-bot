@echo off
setlocal enabledelayedexpansion

rem ============================================
rem Script de Deploy Local → NAS → Docker
rem ============================================

set LOCAL_DIR=E:\Tecnica de Procesamiento del Habla\Trabajo TPH
set NAS_DIR=Y:\deploy-nas
set NAS_IP=192.168.1.42

echo.
echo ====================================
echo   Deploy Local - NAS - Docker
echo ====================================
echo.

rem --- Paso 1: Verificar conectividad NAS ---
echo [1/5] Verificando NAS...
if not exist %NAS_DIR%\ (
    echo ERROR: NAS no montado en Y:\
    echo Ejecuta: net use Y: \\192.168.1.42\Docker
    pause
    exit /b 1
)
echo OK: NAS accesible en %NAS_DIR%


rem --- Paso 2: Copiar archivos y carpetas clave al NAS ---
echo.
echo [2/5] Copiando archivos y carpetas al NAS...
set FILES=web_app.py chatbot_core.py calculators.py database.py visualizations.py requirements.txt chat.html Dockerfile docker-compose.yml docker-compose-with-ngrok.yml
for %%F in (%FILES%) do (
    if exist "%LOCAL_DIR%\%%F" (
        echo   - Copiando %%F...
        copy /Y "%LOCAL_DIR%\%%F" "%NAS_DIR%\%%F" >nul 2>&1
        if errorlevel 1 (
            echo     ERROR copiando %%F
        ) else (
            echo     OK
        )
    ) else (
        echo   - WARN: %%F no existe en local
    )
)

rem --- Copiar carpeta templates ---
if exist "%LOCAL_DIR%\templates" (
    echo   - Copiando carpeta templates...
    xcopy /E /I /Y "%LOCAL_DIR%\templates" "%NAS_DIR%\templates" >nul 2>&1
    if errorlevel 1 (
        echo     ERROR copiando carpeta templates
    ) else (
        echo     OK carpeta templates
    )
) else (
    echo   - WARN: carpeta templates no existe en local
)

rem --- Copiar carpeta data ---
if exist "%LOCAL_DIR%\data" (
    echo   - Copiando carpeta data...
    xcopy /E /I /Y "%LOCAL_DIR%\data" "%NAS_DIR%\data" >nul 2>&1
    if errorlevel 1 (
        echo     ERROR copiando carpeta data
    ) else (
        echo     OK carpeta data
    )
) else (
    echo   - WARN: carpeta data no existe en local
)

rem --- Paso 3: Reiniciar contenedor Docker ---
echo.
echo [3/5] Reiniciando contenedor Docker en NAS...
echo   (Esto toma 30-40 segundos para reinstalar deps...)
echo.

rem Intentar via API de Portainer (requiere token - skip por ahora)
rem curl -X POST http://%NAS_IP%:19900/api/endpoints/1/docker/containers/chatbot-financiero/restart

echo   MANUAL: Abre Portainer y haz Restart en chatbot-financiero
echo   http://%NAS_IP%:19900/#/containers
echo.
pause

rem --- Paso 4: Esperar que levante ---
echo.
echo [4/5] Esperando que el servidor levante...
timeout /t 10 /nobreak >nul

rem --- Paso 5: Verificar deployment ---
echo.
echo [5/5] Verificando deployment...
echo.
echo   - Test /debug:    http://%NAS_IP%:5000/debug
echo   - Test chat:      http://%NAS_IP%:5000
echo   - Ngrok dash:     http://%NAS_IP%:4040
echo.

rem Intentar curl al debug endpoint
where curl >nul 2>&1
if %errorlevel%==0 (
    echo Respuesta de /debug:
    curl -s http://%NAS_IP%:5000/debug | more
    echo.
) else (
    echo   (Instala curl para ver respuesta automática)
)

echo.
echo ====================================
echo   Deploy completado
echo ====================================
echo.
echo Próximos pasos:
echo 1. Verifica http://%NAS_IP%:5000/debug muestra cwd=/app
echo 2. Prueba "Invertir 50000" - debe ir a escenario inversiones
echo 3. Si funciona, commitea a GitHub:
echo    cd "%LOCAL_DIR%"
echo    git add .
echo    git commit -m "Fix: inversiones intent detection + debug endpoint"
echo    git push
echo.
pause
