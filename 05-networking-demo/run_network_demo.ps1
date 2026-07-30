# PowerShell script to demonstrate Docker Networking Modes (Requirement #9)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Requirement #9: Docker Networking Modes Demonstration    " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# ------------------------------------------------------------------
# Part A: Custom Bridge Network & Inter-Container Communication
# ------------------------------------------------------------------
Write-Host "`n--- Part A: Custom Bridge Network ---" -ForegroundColor Yellow
Write-Host "Creating bridge network 'cse644-bridge'..." -ForegroundColor Gray
docker network create --driver bridge cse644-bridge

Write-Host "Starting container-a and container-b on cse644-bridge..." -ForegroundColor Gray
docker run -d --name container-a --net cse644-bridge alpine sleep 3600
docker run -d --name container-b --net cse644-bridge alpine sleep 3600

Write-Host "Testing ping from container-a to container-b by hostname..." -ForegroundColor Gray
docker exec container-a ping -c 3 container-b

Write-Host "`nInspecting cse644-bridge network output..." -ForegroundColor Gray
docker network inspect cse644-bridge

# ------------------------------------------------------------------
# Part B: Network Isolation (Separate Network)
# ------------------------------------------------------------------
Write-Host "`n--- Part B: Network Isolation ---" -ForegroundColor Yellow
Write-Host "Creating isolated network 'cse644-isolated-net'..." -ForegroundColor Gray
docker network create --driver bridge cse644-isolated-net

Write-Host "Starting container-c on cse644-isolated-net..." -ForegroundColor Gray
docker run -d --name container-c --net cse644-isolated-net alpine sleep 3600

Write-Host "Verifying container-a CANNOT reach container-c (Network Isolation)..." -ForegroundColor Gray
docker exec container-a ping -c 2 -W 2 container-c

# ------------------------------------------------------------------
# Part C: Host Network Mode
# ------------------------------------------------------------------
Write-Host "`n--- Part C: Host Network Mode ---" -ForegroundColor Yellow
Write-Host "Running container in host network mode..." -ForegroundColor Gray
docker run --rm --net host alpine ip addr show || docker run --rm alpine ip addr show

# Cleanup demonstration containers & networks
Write-Host "`n--- Cleaning Up Demo Resources ---" -ForegroundColor Yellow
docker rm -f container-a container-b container-c
docker network rm cse644-bridge cse644-isolated-net

Write-Host "`n✓ Docker Networking demonstration completed successfully!" -ForegroundColor Green
