# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
ENV CI=true
COPY package.json ./
COPY tsconfig.json ./
COPY vite.config.ts ./
COPY index.html ./
COPY src ./src
RUN npm ci --no-audit --no-fund
RUN npm run build

# Stage 2: Runtime (using nginx to serve static files)
FROM nginx:1.27-alpine
WORKDIR /usr/share/nginx/html
COPY --from=builder /app/dist ./
# Provide a minimal nginx.conf to handle SPA routing
RUN apk add --no-cache bash
RUN printf 'server { \n\
  listen 80; \n\
  server_name _; \n\
  root /usr/share/nginx/html; \n\
  include /etc/nginx/mime.types; \n\
  location / { try_files $uri /index.html; } \n\
}\n' > /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
