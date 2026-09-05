@echo off
echo [*] Rejoining Fido split archive...
copy /b fido_bundle.part* fido_offline_bundle.zip
if not exist fido_offline_bundle.zip (
    echo [!] Error: Failed to reassemble fido_offline_bundle.zip
    pause
    exit /b 1
)
echo [*] Extracting fido_offline_bundle.zip...
tar -xf fido_offline_bundle.zip
echo [!] Setup complete! You can now run setup.bat or tools\fido.bat
pause
