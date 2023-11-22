"""

"""
from flask import Flask, jsonify, request, send_file, redirect
from flask_cors import CORS
from multiprocessing import Process
from time import sleep
import os
import docker
import tomli
import tomli_w
import io
import requests
import os
import pytz
from datetime import datetime
import re

client = docker.from_env()

global app
app = Flask(__name__)
origins = re.compile(r"https?://([a-z0-9]+[.])*beamui.enzo-frnt.fr")
CORS(app, origins=origins)

from mods import mods

app.register_blueprint(mods)

container_name = os.getenv('SERVER_CONTAINER_NAME')
mod_folder = "/root/shared/Resources/Client/"
conf_file = "/root/shared/ServerConfig.toml"
maps = [item.strip() for item in (os.getenv('MAPS_LIST') or '').split(',')]


# Get the right container
def get_container():
    return client.containers.list(all=True,filters={"name": container_name})[0]

# Get status of the right container
def get_container_infos():
    container = get_container()

    # Obtenir la chaîne de date et d'heure UTC
    utc_str = container.attrs.get('State', {}).get('StartedAt')

    # Tronquer les microsecondes à six chiffres si nécessaire
    if len(utc_str) > 26:
        utc_str = utc_str[:26] + 'Z'

    # Analyser la chaîne pour obtenir un objet datetime avec le fuseau horaire UTC
    utc = datetime.strptime(utc_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    utc = utc.replace(tzinfo=pytz.utc)

    # Convertir en heure locale de Paris
    paris_timezone = pytz.timezone('Europe/Paris')
    local = utc.astimezone(paris_timezone)

    # Créer un dictionnaire avec les informations du conteneur
    container_info = {
        'id': container.id,
        'image': container.image.tags,
        'status': container.status,
        'name': container.name,
        'startedat': local.strftime('%Y-%m-%d %H:%M:%S')  # Formaté pour l'affichage
    }
    # Récupérer l'état de santé si disponible
    health_status = container.attrs.get('State', {}).get('Health', {}).get('Status')
    if health_status:
        container_info['health'] = health_status
    return container_info

# Set the right conf related to the key
def set_conf(key, value):
    try :
        with open(conf_file, 'rb') as conf:
             conf_content = tomli.load(conf)
             general_section = conf_content.get("General", {})
             general_section[key] = value
        with open(conf_file, 'wb') as conf:
             tomli_w.dump(conf_content, conf)
        return True
    except:
        return False
    
@app.route('/uptodate', methods=['GET'])
def upToDate():
    lastContainerStart = get_container_infos().get('startedat')
    lastConfModif = datetime.fromtimestamp(os.path.getmtime(conf_file)).strftime('%Y-%m-%d %H:%M:%S')
    if lastContainerStart == lastConfModif or lastContainerStart > lastConfModif:
        for nom in os.listdir(mod_folder):
            chemin_complet = os.path.join(mod_folder, nom)
            if os.path.isfile(chemin_complet):
                if nom.endswith(".zip") or nom.endswith(".zip.stop") and datetime.fromtimestamp(os.path.getmtime(chemin_complet)).strftime('%Y-%m-%d %H:%M:%S') > lastContainerStart:
                    return jsonify({"needreboot":True})
        return jsonify({"needreboot":False})
    else :
        return jsonify({"needreboot":True})

    
"""
Working request example :
curl https://{URL_TO_BEAMMP_API}/config
"""
@app.route('/config', methods=['GET'])
def get_config():
    api_config = {
        "name": "BeamMP API",
        "version": "1.0.0",
        "CORS": True
    }


    return jsonify({
        "apiConfig": api_config
    })

"""
Working request example :
curl https://{URL_TO_BEAMMP_API}/servconfig
"""
@app.route('/servconfig', methods=['GET'])
def get_serv_config():
    return jsonify({
        "container_name": container_name,
        "mod_folder": mod_folder,
        "conf_file": conf_file,
        "maps": maps
    })

"""=
Working request example :
curl -X POST https://{URL_TO_BEAMMP_API}/start
"""
@app.route('/start', methods=['GET'])
def start_container():
    # Start the container
    get_container().start()

    #Verify if the container is started
    if get_container_infos()['status'] == 'running':
        return jsonify({"message": "Container started"})
    else:
        return jsonify({"message": "Container not started"})

"""
Working request example :
curl -X POST https://{URL_TO_BEAMMP_API}/stop
"""
@app.route('/stop', methods=['GET'])
def stop_container():
    # Stop the container
    get_container().stop()

    #Verify if the container is stopped
    if get_container_infos()['status'] == 'exited':
        return jsonify({"message": "Container stopped"})
    else:
        return jsonify({"message": "Container not stopped"})

"""
Working request example :
curl -X POST https://{URL_TO_BEAMMP_API}/restart
"""
@app.route('/restart', methods=['GET'])
def restart_container():
    # Restart the container in a separte process
    Process(target=get_container().restart).start()

    sleep(1)

    #Verify if the container is restarring
    if get_container_infos()['status'] == 'running':
        if get_container_infos()['health'] == 'starting':
            return jsonify({"message": "Container restarting"})

    return jsonify({"message": "Container not restarting"})

"""
Working request example :
curl https://{URL_TO_BEAMMP_API}/status
"""
@app.route('/status', methods=['GET'])
def status_container():
    return jsonify(get_container_infos())


"""
Working request example :
curl https://{URL_TO_BEAMMP_API}/getconf
"""
@app.route('/getconf', methods=['GET'])
def get_conf():
    with open(conf_file, 'rb') as conf:
        conf_content = tomli.load(conf)
    return jsonify(conf_content)

"""
Working request example :
curl https://{URL_TO_BEAMMP_API}/getconf/{key}
"""
@app.route('/getconf/<key>', methods=['GET'])
def get_conf_key(key):
    with open(conf_file, 'rb') as conf:
        conf_content = tomli.load(conf)["General"]
        match key:
            case "AuthKey":
                return jsonify({key: conf_content[key]})
            case "Debug":
                return jsonify({key: conf_content[key]})
            case "Description":
                return jsonify({key: conf_content[key]})
            case "LogChat":
                return jsonify({key: conf_content[key]})
            case "Map":
                return jsonify({key: conf_content[key]})
            case "MaxCars":
                return jsonify({key: conf_content[key]})
            case "MaxPlayers":
                return jsonify({key: conf_content[key]})
            case "Name":
                return jsonify({key: conf_content[key]})
            case _:
                return jsonify({"message": "Key not found"}), 404
            

@app.route('/setconf/authkey', methods=['POST'])     
def set_conf_authkey():
    if set_conf("AuthKey", request.get_data(as_text=True)) :
        return jsonify({"message": "AuthKey changed"})
    return jsonify({"message": "AuthKey not changed"})

@app.route('/setconf/debug', methods=['POST'])
def set_conf_debug():
    request_data = request.get_data()
    if request_data.isinstance(bool):
        if set_conf("Debug", bool(request.get_data(as_text=True))) :
            return jsonify({"message": "Debug changed"})
    return jsonify({"message": "Debug not changed"})

@app.route('/setconf/description', methods=['POST'])
def set_conf_description():
    request = request.get_data(as_text=True)
    if set_conf("Description", request.get_data(as_text=True)) :
        return jsonify({"message": "Description changed"})
    return jsonify({"message": "Description not changed"})

@app.route('/setconf/logchat', methods=['POST'])
def set_conf_logchat():
    request_data = request.get_data(as_text=True)
    if request_data.isinstance(bool):
        if set_conf("LogChat", bool(request.get_data(as_text=True))) :
            return jsonify({"message": "LogChat changed"})
    return jsonify({"message": "LogChat not changed"})

"""
Working request example :
curl -X POST https://{URL_TO_BEAMMP_API}/setconf/map -H "Content-Type: application/json" -d '/levels/{Your_map}/info.json' 
"""
@app.route('/setconf/map', methods=['POST'])
def set_conf_map():
    request_data = request.get_data(as_text=True)
    request_data_split = request_data.split("/")
    if len(request_data_split) == 4 and request_data_split[0] == "" and request_data_split[1] == "levels" and request_data_split[3] == "info.json" and request_data_split[2] in maps:
        if set_conf("Map", request.get_data(as_text=True)) :
            return jsonify({"message": "Map changed"})
        else:
            return jsonify({"message": "Map not changed"})
    return jsonify({"error": "Wrong map"}), 501

@app.route('/setconf/maxcars', methods=['POST'])
def set_conf_maxcars():
    request_data = request.get_data(as_text=True)
    if request_data.isdigit() and int(request_data) > 0 and int(request_data) < 10:
        if set_conf("MaxCars", int(request.get_data(as_text=True))) :
            return jsonify({"message": "MaxCars changed"})
    return jsonify({"message": "MaxCars not changed"})

@app.route('/setconf/maxplayers', methods=['POST'])
def set_conf_maxplayers():
    request_data = request.get_data(as_text=True)
    if request_data.isdigit() and int(request_data) > 0 and int(request_data) < 20:
        if set_conf("MaxPlayers", int(request.get_data(as_text=True))) :
            return jsonify({"message": "MaxPlayers changed"})
    return jsonify({"message": "MaxPlayers not changed"})

@app.route('/setconf/name', methods=['POST'])
def set_conf_name():
    if set_conf("Name", request.get_data(as_text=True)) :
        return jsonify({"message": "Name changed"})
    return jsonify({"message": "Name not changed"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)

#Passage en prod
#gunicorn -w 4 -b 0.0.0.0:8081 myapp:app