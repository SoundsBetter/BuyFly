# Визначення базового образу
FROM node:lts-alpine

# Встановлення робочої директорії в контейнері
WORKDIR /app

# Копіювання файлів `package.json` і `package-lock.json` (якщо існують)
COPY package*.json ./

# Встановлення залежностей проекту
RUN npm install

# Копіювання всіх файлів проекту у контейнер
COPY . .

# Команда для запуску проекту
CMD ["npm", "run", "serve"]
