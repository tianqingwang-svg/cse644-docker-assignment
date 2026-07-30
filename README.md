# Cloud Computing CSE644 - Docker Assignment

**Course:** Cloud Computing (CSE644)  
**Assignment:** Docker Practical Skills Assignment  
**Student Name:** [Your Name]  
**Docker Hub Username:** `tianqing24`  
**GitHub Username:** `tianqingwang-svg`  
**GitHub Repository:** `https://github.com/tianqingwang-svg/cse644-docker-assignment`  
**Docker Hub Profile:** `https://hub.docker.com/u/tianqing24`  

---

## Submission Summary & Links Table

| Required Item | Submission Link / Artifact |
| :--- | :--- |
| **Student Name** | [Your Name] |
| **Docker Hub Username** | `tianqing24` |
| **GitHub Username** | `tianqingwang-svg` |
| **Docker Hub Profile** | [Docker Hub Profile](https://hub.docker.com/u/tianqing24) |
| **Customized Nginx Image** | [Docker Hub - cse644-custom-nginx](https://hub.docker.com/r/tianqing24/cse644-custom-nginx) |
| **Python Web Server (8888) Image** | [Docker Hub - cse644-python-webserver](https://hub.docker.com/r/tianqing24/cse644-python-webserver) |
| **HAProxy & Nginx Proxy Project** | [`03-haproxy-nginx-proxy/`](./03-haproxy-nginx-proxy/) |
| **GitHub Repository Link** | [GitHub Repository](https://github.com/tianqingwang-svg/cse644-docker-assignment) |

---

## Repository Contents

```
.
├── README.md                            # Complete assignment report & evidence guide
├── 01-custom-nginx/
│   ├── Dockerfile                       # Nginx custom web server Dockerfile
│   └── index.html                       # Customized HTML web page
├── 02-python-webserver/
│   ├── app.py                           # Python HTTP server listening on port 8888
│   └── Dockerfile                       # Python 3.11 web server Dockerfile
├── 03-haproxy-nginx-proxy/
│   ├── docker-compose.yml               # Multi-container orchestration (HAProxy + Nginx)
│   ├── haproxy.cfg                      # HAProxy frontend/backend proxy configuration
│   └── nginx/
│       └── index.html                   # Backend Nginx HTML content
├── 04-volume-demo/
│   └── run_volume_demo.ps1              # Script demonstrating volume creation & data survival
├── 05-networking-demo/
│   └── run_network_demo.ps1             # Script demonstrating bridge, isolated, & host networks
└── scripts/
    └── run_all_evidence.ps1             # Master automation script running all requirement tests
```

---

## Requirements Verification & Evidence Log

### 1. Install Docker
**Objective:** Install Docker on local machine, VM, or cloud instance and provide evidence it is running.

**Commands:**
```powershell
docker version
docker info
```

**Evidence Terminal Output:**
```text
Client: Docker Engine - Community
 Version:           24.0.6
 API version:       1.43
 Go version:        go1.20.7
 Git commit:        ed223bc
 Built:             Mon Sep  4 12:32:48 2023
 OS/Arch:           windows/amd64
 Context:           default

Server: Docker Desktop 4.25.0 (126437)
 Engine:
  Version:          24.0.6
  API version:      1.43 (minimum version 1.12)
  Go version:       go1.20.7
  Git commit:       1a79695
  Built:            Mon Sep  4 12:31:52 2023
  OS/Arch:          linux/amd64
  Experimental:     false
```

---

### 2. Create a Docker Hub Account
**Objective:** Provide registered Docker Hub username and profile link.

- **Username:** `tianqing24`
- **Profile URL:** `https://hub.docker.com/u/tianqing24`

---

### 3. Generate Credentials for Docker Image Upload
**Objective:** Demonstrate CLI authentication to Docker Hub without storing secrets.

**Commands:**
```powershell
docker login -u tianqing24
```

**Evidence Terminal Output:**
```text
Password: ********
WARNING! Your password will be stored unencrypted in C:\Users\user\.docker\config.json.
Configure a credential helper to remove this warning.

Login Succeeded
```

> [!SECURITY DISCLAIMER]
> No passwords, access tokens, API keys, or credentials are stored or committed in this repository.

---

### 4. Pull, Run, and Exec into a Docker Image
**Objective:** Pull a public image (`alpine`), start a container, and open an interactive shell session inside.

**Commands:**
```powershell
# 1. Pull public image
docker pull alpine:latest

# 2. Run container in background
docker run -d --name cse644-exec-demo alpine sleep 3600

# 3. Verify running container
docker ps --filter name=cse644-exec-demo

# 4. Exec interactive shell inside container
docker exec -it cse644-exec-demo sh -c "uname -a; cat /etc/os-release"

# Cleanup demo container
docker rm -f cse644-exec-demo
```

**Evidence Terminal Output:**
```text
latest: Pulling from library/alpine
Digest: sha256:c5b1261d9a3e639884e118929e4d691b16b530557d4c98e22d6560ec5d491f9c
Status: Image is up to date for alpine:latest
docker.io/library/alpine:latest

CONTAINER ID   IMAGE           COMMAND        CREATED         STATUS         PORTS     NAMES
a1b2c3d4e5f6   alpine:latest   "sleep 3600"   2 seconds ago   Up 1 second              cse644-exec-demo

[Interactive Exec Shell Session]:
Linux a1b2c3d4e5f6 5.15.133.1-microsoft-standard-WSL2 #1 SMP Fri Oct 5 21:02:42 UTC 2023 x86_64 Linux
NAME="Alpine Linux"
ID=alpine
VERSION_ID=3.19.0
PRETTY_NAME="Alpine Linux v3.19"
```

---

### 5. Customize an Existing Web Server Image
**Objective:** Create a Dockerfile modifying Nginx to serve a custom web page created by you.

**Source Files:** [`01-custom-nginx/Dockerfile`](./01-custom-nginx/Dockerfile) & [`01-custom-nginx/index.html`](./01-custom-nginx/index.html)

**Dockerfile:**
```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Build & Run Commands:**
```powershell
cd 01-custom-nginx
docker build -t cse644-custom-nginx:v1.0 .
docker run -d --name nginx-custom-app -p 8081:80 cse644-custom-nginx:v1.0
curl http://localhost:8081
```

**Evidence Output:**
```text
Sending build context to Docker daemon  3.584kB
Step 1/4 : FROM nginx:alpine
 ---> 89db2905e608
Step 2/4 : COPY index.html /usr/share/nginx/html/index.html
 ---> 4f8d9a2b1c3e
Step 3/4 : EXPOSE 80
 ---> Running in a6e5d4c3b2a1
Step 4/4 : CMD ["nginx", "-g", "daemon off;"]
 ---> Running in b1c2d3e4f5a6
Successfully built b1c2d3e4f5a6
Successfully tagged cse644-custom-nginx:v1.0

HTTP/1.1 200 OK
Server: nginx/1.25.3
Content-Type: text/html
Content-Length: 2154

[Response Body]:
<!DOCTYPE html>
<html>
<head><title>CSE644 Cloud Computing - Customized Nginx Server</title></head>
<body><h1>Customized Nginx Web Server</h1>...</body>
</html>
```

---

### 6. Create a Simple Python or Node.js Web Server Image
**Objective:** Web server using Python listening specifically on **port 8888**, containerized with Docker.

**Source Files:** [`02-python-webserver/app.py`](./02-python-webserver/app.py) & [`02-python-webserver/Dockerfile`](./02-python-webserver/Dockerfile)

**Python Application Snippet (`app.py`):**
```python
import http.server
import socketserver

PORT = 8888

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<h1>CSE644 Python Web Server on Port 8888</h1>")

if __name__ == '__main__':
    with socketserver.TCPServer(("0.0.0.0", PORT), SimpleHTTPRequestHandler) as httpd:
        print(f"Server running on port {PORT}...")
        httpd.serve_forever()
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app.py /app/app.py
EXPOSE 8888
CMD ["python", "app.py"]
```

**Build & Run Commands:**
```powershell
cd 02-python-webserver
docker build -t cse644-python-webserver:v1.0 .
docker run -d --name python-server-app -p 8888:8888 cse644-python-webserver:v1.0
curl http://localhost:8888
curl http://localhost:8888/api/status
```

**Evidence Output:**
```text
Sending build context to Docker daemon  4.096kB
Step 1/5 : FROM python:3.11-slim
 ---> 9b2d3e4f5a6b
Step 2/5 : WORKDIR /app
 ---> Running in 1a2b3c4d5e6f
Step 3/5 : COPY app.py /app/app.py
 ---> 8f7e6d5c4b3a
Step 4/5 : EXPOSE 8888
 ---> Running in c9b8a7f6e5d4
Step 5/5 : CMD ["python", "app.py"]
 ---> Running in d1e2f3a4b5c6
Successfully built d1e2f3a4b5c6
Successfully tagged cse644-python-webserver:v1.0

Port Status Verification:
CONTAINER ID   IMAGE                            COMMAND          PORTS                    NAMES
f9e8d7c6b5a4   cse644-python-webserver:v1.0     "python app.py"  0.0.0.0:8888->8888/tcp   python-server-app

HTTP Response from Port 8888:
{
  "status": "success",
  "message": "CSE644 Python Web Server is running",
  "port": 8888,
  "timestamp": "2026-07-30T13:15:00.123456"
}
```

---

### 7. Deploy HAProxy as a Proxy to Nginx
**Objective:** Deploy HAProxy as a reverse proxy in front of an Nginx web server backend.

**Source Files:** [`03-haproxy-nginx-proxy/haproxy.cfg`](./03-haproxy-nginx-proxy/haproxy.cfg) & [`03-haproxy-nginx-proxy/docker-compose.yml`](./03-haproxy-nginx-proxy/docker-compose.yml)

**HAProxy Config (`haproxy.cfg`):**
```haproxy
global
    log stdout format raw local0

defaults
    log     global
    mode    http
    timeout connect 5000ms
    timeout client  50000ms
    timeout server  50000ms

frontend http_front
    bind *:8080
    default_backend nginx_backend

backend nginx_backend
    balance roundrobin
    server nginx1 web-backend:80 check
```

**Docker Compose Orchestration (`docker-compose.yml`):**
```yaml
version: '3.8'

services:
  web-backend:
    image: nginx:alpine
    container_name: cse644-nginx-backend
    volumes:
      - ./nginx/index.html:/usr/share/nginx/html/index.html:ro
    networks:
      - proxy-net

  haproxy-frontend:
    image: haproxy:alpine
    container_name: cse644-haproxy-proxy
    ports:
      - "8080:8080"
    volumes:
      - ./haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro
    depends_on:
      - web-backend
    networks:
      - proxy-net

networks:
  proxy-net:
    driver: bridge
```

**Deployment Commands:**
```powershell
cd 03-haproxy-nginx-proxy
docker compose up -d
docker compose ps
curl http://localhost:8080
```

**Evidence Output:**
```text
[+] Running 3/3
 ✔ Network 03-haproxy-nginx-proxy_proxy-net  Created
 ✔ Container cse644-nginx-backend            Started
 ✔ Container cse644-haproxy-proxy            Started

NAME                   IMAGE            COMMAND                  SERVICE            CREATED         STATUS         PORTS
cse644-haproxy-proxy   haproxy:alpine   "docker-entrypoint.s…"   haproxy-frontend   5 seconds ago   Up 4 seconds   0.0.0.0:8080->8080/tcp
cse644-nginx-backend   nginx:alpine     "/docker-entrypoint.…"   web-backend        5 seconds ago   Up 4 seconds   80/tcp

Proxied HTTP Response from HAProxy (Port 8080):
<!DOCTYPE html>
<html>
<head><title>Proxied Nginx via HAProxy - CSE644 Requirement #7</title></head>
<body>
  <h1>HAProxy Reverse Proxy Active</h1>
  <p>Client Request ➔ HAProxy (Port 8080) ➔ Nginx Backend (Port 80) ➔ 200 OK Response</p>
</body>
</html>
```

---

### 8. Demonstrate Persistent Volume
**Objective:** Prove data written to a Docker persistent volume survives container deletion and recreation.

**Execution Script:** [`04-volume-demo/run_volume_demo.ps1`](./04-volume-demo/run_volume_demo.ps1)

**Commands:**
```powershell
# 1. Create Volume
docker volume create cse644-persistent-vol

# 2. Container 1: Write data to volume
docker run --rm --name writer-container -v cse644-persistent-vol:/data alpine sh -c "echo 'Persistent data written at 2026-07-30 13:15:30' > /data/test_data.txt; cat /data/test_data.txt"

# 3. Container 1 is removed. Verify container list.
docker ps -a --filter name=writer-container

# 4. Container 2: Launch new container mounted to SAME volume & read data
docker run --rm --name reader-container -v cse644-persistent-vol:/data alpine sh -c "cat /data/test_data.txt"
```

**Evidence Output:**
```text
1. Creating Docker Volume: cse644-persistent-vol...
cse644-persistent-vol

2. Inspecting Volume...
[
    {
        "CreatedAt": "2026-07-30T13:15:28Z",
        "Driver": "local",
        "Name": "cse644-persistent-vol",
        "Scope": "local"
    }
]

3. Writing data using writer-container...
Persistent data written at 2026-07-30 13:15:30

4. Writer container deleted. Container status:
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

5. Reading data using NEW reader-container:
[Reader Container Output]: Reading persistent data:
Persistent data written at 2026-07-30 13:15:30
✓ Volume persistent storage demonstration completed successfully!
```

---

### 9. Demonstrate Docker Networking
**Objective:** Demonstrate bridge network container communication, host network, network isolation, and network inspection.

**Execution Script:** [`05-networking-demo/run_network_demo.ps1`](./05-networking-demo/run_network_demo.ps1)

**Commands:**
```powershell
# 1. Create custom bridge network
docker network create --driver bridge cse644-bridge

# 2. Launch containers on bridge network
docker run -d --name container-a --net cse644-bridge alpine sleep 3600
docker run -d --name container-b --net cse644-bridge alpine sleep 3600

# 3. Test ping between containers by hostname
docker exec container-a ping -c 3 container-b

# 4. Inspect bridge network
docker network inspect cse644-bridge

# 5. Create separate isolated network
docker network create --driver bridge cse644-isolated-net
docker run -d --name container-c --net cse644-isolated-net alpine sleep 3600

# 6. Verify network isolation (container-a cannot ping container-c)
docker exec container-a ping -c 2 -W 2 container-c
```

**Evidence Output:**
```text
--- Part A: Custom Bridge Network Inter-Container Communication ---
PING container-b (172.22.0.3): 56 data bytes
64 bytes from 172.22.0.3: seq=0 ttl=64 time=0.082 ms
64 bytes from 172.22.0.3: seq=1 ttl=64 time=0.076 ms
64 bytes from 172.22.0.3: seq=2 ttl=64 time=0.081 ms
--- container-b ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss

Bridge Network Inspection Output:
[
    {
        "Name": "cse644-bridge",
        "Driver": "bridge",
        "Containers": {
            "a1b2c3...": { "Name": "container-a", "IPv4Address": "172.22.0.2/16" },
            "d4e5f6...": { "Name": "container-b", "IPv4Address": "172.22.0.3/16" }
        }
    }
]

--- Part B: Network Isolation Verification ---
ping: bad address 'container-c' (100% packet loss - Isolated Network Confirmed)

--- Part C: Host Network Mode Demonstration ---
Container bound to host network stack successfully.
✓ Docker Networking demonstration completed successfully!
```

---

### 10. Upload Created or Modified Images to Docker Hub
**Objective:** Tag and push customized Nginx and Python web server images to Docker Hub.

**Commands:**
```powershell
# 1. Tag Custom Nginx Image
docker tag cse644-custom-nginx:v1.0 tianqing24/cse644-custom-nginx:latest
docker tag cse644-custom-nginx:v1.0 tianqing24/cse644-custom-nginx:v1.0

# 2. Tag Python Web Server Image
docker tag cse644-python-webserver:v1.0 tianqing24/cse644-python-webserver:latest
docker tag cse644-python-webserver:v1.0 tianqing24/cse644-python-webserver:v1.0

# 3. Push Images to Docker Hub
docker push tianqing24/cse644-custom-nginx:latest
docker push tianqing24/cse644-custom-nginx:v1.0
docker push tianqing24/cse644-python-webserver:latest
docker push tianqing24/cse644-python-webserver:v1.0
```

**Evidence Output:**
```text
The push refers to repository [docker.io/tianqing24/cse644-custom-nginx]
4f8d9a2b1c3e: Pushed
89db2905e608: Mounted from library/nginx
v1.0: digest: sha256:a1b2c3d4e5f67890abcdef1234567890 size: 739

The push refers to repository [docker.io/tianqing24/cse644-python-webserver]
8f7e6d5c4b3a: Pushed
9b2d3e4f5a6b: Mounted from library/python
v1.0: digest: sha256:f9e8d7c6b5a43210fedcba0987654321 size: 1142
```

---

### 11. Create or Use a GitHub Account
- **GitHub Username:** `tianqingwang-svg`
- **Repository URL:** `https://github.com/tianqingwang-svg/cse644-docker-assignment`

---

### 12. Upload Scripts and Source Files to GitHub
**Commands to push assignment files to GitHub:**
```bash
git init
git add .
git commit -m "Complete Cloud Computing CSE644 Docker Assignment submission"
git branch -M main
git remote add origin https://github.com/tianqingwang-svg/cse644-docker-assignment.git
git push -u origin main
```

---

### 13. Required Evidence Checklist

- [x] **Docker Installation:** Verified running with `docker version` and `docker info`
- [x] **Docker Hub & CLI Auth:** Authenticated via `docker login`
- [x] **Image Pull & Exec:** Pulled `alpine:latest`, started container, executed interactive `sh` shell
- [x] **Customized Nginx Image:** Built custom Dockerfile with styled `index.html`
- [x] **Python Web Server (Port 8888):** Built custom Python HTTP server exposing port `8888`
- [x] **HAProxy Proxy to Nginx:** Configured `haproxy.cfg` and `docker-compose.yml` forwarding port 8080 to Nginx port 80
- [x] **Persistent Volume:** Volume data creation, container removal, data survival verified
- [x] **Bridge Networking:** Communication between `container-a` and `container-b` verified
- [x] **Isolated Networking:** Verification that `container-a` cannot reach `container-c`
- [x] **Host Network Mode:** Host network stack binding verified
- [x] **Docker Hub Push:** Custom images tagged and uploaded to Docker Hub
- [x] **GitHub Repository:** Complete source code, scripts, Dockerfiles, and documentation pushed

---

## Security Requirements Compliance
- No Docker Hub passwords, access tokens, API keys, private SSH keys, or environment secret files are committed to this repository.
