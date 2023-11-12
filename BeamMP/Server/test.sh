#!/bin/bash

# Obtenez le STIME pour le PID 1 (plutôt que 0, car Linux n'a pas de processus PID 0)
stime=$(ps -eo pid,stime | grep '^ *1 ' | awk '{print $2}')
echo "from: $stime"

# Obtenir l'anne actuelle
current_year=$(date +"%Y")
echo "curr: $current_year"

# Convertir le STIME en format de date compréhensible par `date` command
if [[ $stime == *:* ]]; then
    # Si l'heure est donne (HH:MM), supposez que c'est aujourd'hui
    stime=$(date +"%Y-%m-%d $stime")
    echo "new : $stime"
elif [[ $stime == ???[0-9]* ]]; then
    # Si le format est MMMDD (par exemple, Nov11)
    stime="$current_year-${stime:0:3}-${stime:3:2}"
    echo "new : $stime"
else
    # Autre format non pris en charge
    echo "Format de date non reconnu: $stime"
    exit 1
fi

# Convertir les deux dates en secondes depuis l'époque et calculer la différence
start_sec=$(date -d "$stime" +"%s")
now_sec=$(date +"%s")
uptime_sec=$((now_sec - start_sec))

# Convertir les secondes en format lisible (jours, heures, minutes)
days=$((uptime_sec / 86400))
hours=$(( (uptime_sec % 86400) / 3600 ))
minutes=$(( (uptime_sec % 3600) / 60 ))

echo "Uptime: $days days, $hours hours, $minutes minutes"

