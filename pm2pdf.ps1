cd src/pm

nbmerge -o pm.ipynb -v receitas.ipynb despesas.ipynb

jupyter nbconvert --to=webpdf --no-input --execute --embed-images pm.ipynb

Remove-Item -Path ..\..\pm.pdf -Recurse -Force

Move-Item -Path .\pm.pdf -Destination ..\..\pm.pdf

Remove-Item -Path .\pm.ipynb

cd ../..

Write-Host "Pressione ENTER para finalizar:"
Read-Host