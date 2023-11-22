FROM node:18.16-alpine AS build

# Define the working directory
WORKDIR /build

# Get the source code
COPY ./front /build
RUN rm -r /build/node_modules && rm -r /build/dist && rm -r /build/package-lock.json
RUN npm install --force

# Build the application
RUN npm run build

# Création de l'image de release
FROM nginx:1.15.2-alpine as release

#Install supervisord
RUN apk update && apk add --no-cache supervisor curl tzdata gettext

# Define the timezone
ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install cloudflared
RUN curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/bin/cloudflared
RUN chmod +x /usr/bin/cloudflared


# Copy the build files to the nginx directory
WORKDIR /usr/share/nginx/html
COPY --from=build /build/dist/frontend /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/nginx.conf

# Copy the startup script
COPY ./startup.sh /start/startup.sh
COPY ./nginx-startup.sh /start/nginx-startup.sh
COPY ./supervisord.conf /etc/supervisord.conf

CMD ["sh", "/start/startup.sh"]