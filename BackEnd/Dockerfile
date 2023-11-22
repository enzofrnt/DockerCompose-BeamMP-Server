FROM python:3.13-rc-alpine3.17

# Installe tzdata pour la configuration du fuseau horaire
RUN apk add --no-cache tzdata supervisor curl gettext

# Définit le fuseau horaire (remplacez par votre fuseau horaire souhaité)
ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/bin/cloudflared
RUN chmod +x /usr/bin/cloudflared

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de dépendances Python dans le conteneur
COPY ./Python-src/ /app/

# Copie du fihcier de configuration de supervisord
COPY ./supervisord.conf /etc/supervisord.conf

# Copie du fihcier de démarrage
COPY ./startup.sh /start/startup.sh 

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Execute pour debug
#CMD [ "tail", "-f", "/dev/null" ]

# Utiliser supervisord pour démarrer les services
CMD ["sh", "/start/startup.sh"]