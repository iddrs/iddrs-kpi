Start-Process -FilePath notepad .\_config.yml -Wait


Remove-Item -Path .\docs\* -Recurse -Force

Copy-Item -Path .\_build\html\* -Destination .\docs\ -Recurse

# Conforme orientação de https://jupyterbook.org/en/stable/publish/gh-pages.html
New-Item -Path .\docs\.nojekyll -ItemType File

Write-Host "Pressione ENTER para finalizar:"
Read-Host