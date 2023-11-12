FROM python:3.13-rc-alpine3.17

# Installe tzdata pour la configuration du fuseau horaire
RUN apk add --no-cache tzdata

# Définit le fuseau horaire (remplacez par votre fuseau horaire souhaité)
ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de dépendances Python dans le conteneur
COPY ./Python-src/ /app/

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Execute le script Python
CMD [ "tail", "-f", "/dev/null" ]
#CMD [ "python", "./app.py" ]