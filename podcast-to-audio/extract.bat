@echo off
chcp 65001 > nul
setlocal

set "PYTHON_EXE=C:\Users\xjtul\AppData\Local\Programs\Python\Python312\python.exe"
set "SCRIPT_DIR=C:\Users\xjtul\.claude\skills\podcast-to-audio"
set "OUTPUT_DIR=%SCRIPT_DIR%\audio"

if "%~1"=="" (
    echo 用法：extract.bat "小宇宙链接"
    echo 示例：extract.bat "https://www.xiaoyuzhoufm.com/episode/69eb5dfc1d989496e76d373c"
    exit /b 1
)

"%PYTHON_EXE%" "%SCRIPT_DIR%\scripts\podcast_to_audio.py" --input "%~1" --out-dir "%OUTPUT_DIR%"

endlocal
