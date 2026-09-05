@echo off
setlocal
set PYTHON_EXE=C:\Users\reedz\OneDrive\Documents\Automation\MM\Python\Master_skills\.venv\Scripts\python.exe
if not exist "%PYTHON_EXE%" (
    set PYTHON_EXE=python
)
"%PYTHON_EXE%" "C:\Users\reedz\OneDrive\Documents\Automation\MM\Python\Master_skills\tools\fido.py" %*
endlocal
