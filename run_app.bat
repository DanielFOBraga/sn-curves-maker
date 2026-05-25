@echo off
:: Map network UNC path to a temporary drive letter if started from a network share
pushd "%~dp0"

title S-N Curves Maker Launcher
echo =======================================================================
echo                 S-N Curves Maker Launcher (pyLife)
echo =======================================================================
echo.

:: Check if Python or Python Launcher (py) is installed
set "PYTHON_CMD="
python --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=python"
) else (
    py --version >nul 2>&1
    if not errorlevel 1 (
        set "PYTHON_CMD=py"
    )
)

if "%PYTHON_CMD%"=="" (
    echo [ERROR] Python is not installed or not in your system PATH.
    echo Please install Python 3.9 or higher and check "Add Python to PATH" during installation.
    echo.
    pause
    popd
    exit /b 1
)

:: Define local virtual environment path in user's AppData to avoid network latency/locking
set "VENV_DIR=%LOCALAPPDATA%\sn-curves-maker\venv"

:: Create virtual environment if it doesn't exist
if not exist "%VENV_DIR%" (
    echo [INFO] Creating Python virtual environment in "%VENV_DIR%" using %PYTHON_CMD%...
    %PYTHON_CMD% -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        popd
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created successfully!
    echo.
)

:: Activate virtual environment
echo [INFO] Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    popd
    exit /b 1
)
echo [SUCCESS] Activated!
echo.

:: Clean up corrupted pip tilde directories in site-packages
if exist "%VENV_DIR%\Lib\site-packages" (
    for /d %%i in ("%VENV_DIR%\Lib\site-packages\~*") do (
        echo [INFO] Cleaning up corrupted package directory: %%~nxi
        rd /s /q "%%i" >nul 2>&1
    )
)

:: Check if dependencies are already installed to avoid slow pip checks
echo [INFO] Verifying installed packages...
python -c "import pylife, streamlit, pandas, numpy, matplotlib, openpyxl" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Dependencies are not fully installed. Installing now...
    echo This might take a few moments on the first run...
    python -m pip install pylife openpyxl pandas numpy matplotlib streamlit
    if errorlevel 1 (
        echo [ERROR] Dependency installation failed.
        pause
        popd
        exit /b 1
    )
    echo [SUCCESS] All dependencies are ready!
    echo.
) else (
    echo [SUCCESS] All dependencies verified successfully!
    echo.
)

:: Generate sample data if not present
if not exist sample_data.xlsx (
    echo [INFO] Generating realistic fatigue test dataset...
    python sample_generator.py
    if errorlevel 1 (
        echo [WARNING] Failed to generate sample data. The app will still run, but you will need to upload your own Excel file.
    ) else (
        echo [SUCCESS] Generated sample data successfully!
    )
    echo.
)

:: Run Streamlit App in Headless mode to prevent email prompt and run cleanly
echo [INFO] Launching Streamlit web application...
echo The app should open automatically in your default browser.
echo If it doesn't, copy-paste the URL shown below into your browser.
echo.
streamlit run sn_curves_app.py --server.headless=true --browser.gatherUsageStats=false

:: Restore original directory context and unmap temporary drive letter
popd
pause
