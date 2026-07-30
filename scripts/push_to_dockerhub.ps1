# PowerShell script to login, build, and push Docker images to Docker Hub (tianqing24)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Pushing Docker Images to Docker Hub (tianqing24)        " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Login to Docker Hub
Write-Host "`nStep 1: Logging in to Docker Hub as tianqing24..." -ForegroundColor Yellow
docker login -u tianqing24

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker login failed. Please check Docker Desktop engine status and credentials." -ForegroundColor Red
    Read-Host -Prompt "Press Enter to exit"
    exit 1
}

# 2. Build and Push Custom Nginx Image
Write-Host "`nStep 2: Building & Pushing Customized Nginx Image (tianqing24/cse644-custom-nginx:v1.0)..." -ForegroundColor Yellow
Set-Location "e:\hk\01-custom-nginx"
docker build -t tianqing24/cse644-custom-nginx:v1.0 -t tianqing24/cse644-custom-nginx:latest .
docker push tianqing24/cse644-custom-nginx:v1.0
docker push tianqing24/cse644-custom-nginx:latest

# 3. Build and Push Python Web Server Image
Write-Host "`nStep 3: Building & Pushing Python Web Server Image (tianqing24/cse644-python-webserver:v1.0)..." -ForegroundColor Yellow
Set-Location "e:\hk\02-python-webserver"
docker build -t tianqing24/cse644-python-webserver:v1.0 -t tianqing24/cse644-python-webserver:latest .
docker push tianqing24/cse644-python-webserver:v1.0
docker push tianqing24/cse644-python-webserver:latest

Set-Location "e:\hk"
Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host " ✓ All images pushed to https://hub.docker.com/u/tianqing24! " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Read-Host -Prompt "Press Enter to exit"
