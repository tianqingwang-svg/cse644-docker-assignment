# Customized Nginx Dockerfile for CSE644 Docker Assignment (Requirement 5)
FROM nginx:alpine

# Copy custom web page into Nginx standard html path
COPY index.html /usr/share/nginx/html/index.html

# Expose HTTP port 80
EXPOSE 80

# Run Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
