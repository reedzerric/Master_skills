Write-Host '[*] Rejoining Fido split archive...' -ForegroundColor Cyan
cmd.exe /c 'copy /b fido_bundle.part* fido_offline_bundle.zip'
Write-Host '[*] Extracting fido_offline_bundle.zip...' -ForegroundColor Cyan
Expand-Archive -Path 'fido_offline_bundle.zip' -DestinationPath '.' -Force
Write-Host '[+] Successfully unpacked!' -ForegroundColor Green
