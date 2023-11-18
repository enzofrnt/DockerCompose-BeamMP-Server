FROM node:18.16-alpine AS build

WORKDIR /build

# Récupération des sources et installation des dépendances
COPY ./front /build
RUN  npm install --force

# Build de l'application
RUN  npm run build

# Création de l'image de release
FROM nginx:1.15.2-alpine as release

# Copie des fichiers de configuration et de l'application depuis le build
WORKDIR /usr/share/nginx/html
COPY --from=build /build/dist/frontend /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/nginx.conf

COPY ./startup.sh /start/startup.sh
COPY ./nginx-startup.sh /start/nginx-startup.sh
COPY ./supervisord.conf /etc/supervisord.conf

CMD ["sh", "/start/startup.sh"]