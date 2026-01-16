# Стадия 1 — сборка (builder)
FROM node:20-alpine AS builder

WORKDIR /app

# Копируем только зависимости сначала — для кэширования
COPY package*.json ./
RUN npm ci

# Копируем весь код и собираем
COPY . .
RUN npm run build

# Стадия 2 — финальный образ (nginx)
FROM nginx:alpine

# Копируем собранные файлы из builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Копируем конфиг nginx (чтобы SPA работала с любыми путями)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]