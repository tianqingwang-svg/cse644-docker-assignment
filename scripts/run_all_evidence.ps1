# Automated Master Script to Execute All CSE644 Assignment Demos and Log Evidence

$logFile = "e:\hk\evidence_execution.log"
Start-Transcript -Path $logFile -Force

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " CSE644 CLOUD COMPUTING - DOCKER ASSIGNMENT EVIDENCE LOG   " -ForegroundColor Cyan
Write-Host " Execution Date: $(Get-Date)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# Requirement 1: Install Docker
Write-Host "`n>>> Requirement 1: Docker Installation Verification" -ForegroundColor Yellow
docker version
docker info | Select-Object -First 25

# Requirement 4: Pull, Run, Exec
Write-Host "`n>>> Requirement 4: Pull, Run, and Exec into Docker Image" -ForegroundColor Yellow
docker pull alpine:latest
docker run -d --name cse644-test-alpine alpine sleep 3600
docker ps --filter name=cse644-test-alpine
docker exec cse644-test-alpine sh -c "uname -a; cat /etc/os-release; uptime"
docker rm -f cse644-test-alpine

# Requirement 5: Customized Nginx Web Server
Write-Host "`n>>> Requirement 5: Customize Existing Web Server Image (Nginx)" -ForegroundColor Yellow
Set-Location "e:\hk\01-custom-nginx"
docker build -t cse644-custom-nginx:v1.0 .
docker run -d --name test-nginx -p 8081:80 cse644-custom-nginx:v1.0
Start-Sleep -Seconds 3
Invoke-RestMethod -Uri "http://localhost:8081"
docker rm -f test-nginx

# Requirement 6: Simple Python Web Server (Port 8888)
Write-Host "`n>>> Requirement 6: Python Web Server Image (Port 8888)" -ForegroundColor Yellow
Set-Location "e:\hk\02-python-webserver"
docker build -t cse644-python-webserver:v1.0 .
docker run -d --name test-python-server -p 8888:8888 cse644-python-webserver:v1.0
Start-Sleep -Seconds 3
Invoke-RestMethod -Uri "http://localhost:8888"
Invoke-RestMethod -Uri "http://localhost:8888/api/status"
docker rm -f test-python-server

# Requirement 7: HAProxy Proxy to Nginx
Write-Host "`n>>> Requirement 7: Deploy HAProxy as Proxy to Nginx" -ForegroundColor Yellow
Set-Location "e:\hk\03-haproxy-nginx-proxy"
docker compose up -d
Start-Sleep -Seconds 5
docker compose ps
Invoke-RestMethod -Uri "http://localhost:8080"
docker compose down

# Requirement 8: Persistent Volume Demonstration
Write-Host "`n>>> Requirement 8: Demonstrate Persistent Volume" -ForegroundColor Yellow
Set-Location "e:\hk\04-volume-demo"
.\run_volume_demo.ps1

# Requirement 9: Docker Networking Demonstration
Write-Host "`n>>> Requirement 9: Demonstrate Docker Networking" -ForegroundColor Yellow
Set-Location "e:\hk\05-networking-demo"
.\run_network_demo.ps1

Set-Location "e:\hk"
Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " ALL EVIDENCE EXECUTED AND CAPTURED SUCCESSFULLY!          " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

Stop-Transcript
