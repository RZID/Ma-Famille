# Single origin for college.rzidinc.com/ma-famille:
# nginx serves the built SPA at /ma-famille/ and proxies /ma-famille/api/ to FastAPI.
FROM node:20-alpine AS build
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
ARG VITE_BASE_PATH=/ma-famille/
ARG VITE_API_URL
ENV VITE_BASE_PATH=$VITE_BASE_PATH VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM nginx:alpine
COPY web/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html/ma-famille/
EXPOSE 8080
