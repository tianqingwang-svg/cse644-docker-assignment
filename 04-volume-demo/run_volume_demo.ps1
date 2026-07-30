# PowerShell script to demonstrate Docker Persistent Volume survival (Requirement #8)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Requirement #8: Docker Persistent Storage Demonstration " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Create Docker Volume
Write-Host "`n1. Creating Docker Volume: cse644-persistent-vol..." -ForegroundColor Yellow
docker volume create cse644-persistent-vol

# 2. Inspect created volume
Write-Host "`n2. Inspecting Volume..." -ForegroundColor Yellow
docker volume inspect cse644-persistent-vol

# 3. Write data using Container 1 (writer-container)
Write-Host "`n3. Launching writer-container and writing data to /data/test_data.txt..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
docker run --rm --name writer-container -v cse644-persistent-vol:/data alpine sh -c "echo 'CSE644 Persistent Volume Test Data written at $timestamp' > /data/test_data.txt; cat /data/test_data.txt"

# 4. Confirm container removal
Write-Host "`n4. Writer container removed. Verifying container list..." -ForegroundColor Yellow
docker ps -a --filter name=writer-container

# 5. Launch Container 2 (reader-container) mounted to the SAME volume and read data
Write-Host "`n5. Launching reader-container mounted to cse644-persistent-vol..." -ForegroundColor Yellow
docker run --rm --name reader-container -v cse644-persistent-vol:/data alpine sh -c "echo '[Reader Container Output]: Reading persistent data:'; cat /data/test_data.txt"

Write-Host "`n✓ Volume persistent storage demonstration completed successfully!" -ForegroundColor Green
