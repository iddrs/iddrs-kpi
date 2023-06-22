Remove-Item -Path .\docs\* -Recurse -Force

Copy-Item -Path .\_build\html\* -Destination .\docs\ -Recurse

Write-Host "Pressione ENTER para finalizar:"
Read-Host