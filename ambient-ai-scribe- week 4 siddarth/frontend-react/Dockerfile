## Build stage
FROM node:18-alpine AS build
WORKDIR /app
COPY frontend-react/package.json frontend-react/package-lock.json* ./
COPY frontend-react/ .
RUN npm ci && npm run build

## Production stage
FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY frontend-react/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
