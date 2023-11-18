"""

"""
from flask import Flask, jsonify, request, send_file, redirect
from multiprocessing import Process
from time import sleep
import os
import docker
import tomli
import tomli_w
import io
import requests
import os

client = docker.from_env()
app = Flask(__name__)
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
    container_info = {
        'id': container.id,
        'image': container.image.tags,
        'status': container.status,
        'name': container.name
    }
    # Récupérer l'état de santé si disponible
    health_status = container.attrs.get('State', {}).get('Health', {}).get('Status')
    if health_status:
        container_info['health'] = health_status
    return container_info

# Set the right conf related to the key
def set_conf(key):
    try :
        app.logger.info("set_conf")
        app.logger.info(request.get_data(as_text=True))
        with open(conf_file, 'rb') as conf:
             conf_content = tomli.load(conf)
             general_section = conf_content.get("General", {})
             general_section[key] = request.get_data(as_text=True)  
        with open(conf_file, 'wb') as conf:
             tomli_w.dump(conf_content, conf)
        return True
    except:
        app.logger.info("set_conf error")
        return False

"""
Working request example :
curl https://{URL_TO_BEAMMP_API}/config
"""
@app.route('/config', methods=['GET'])
def get_config():
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
curl https://{URL_TO_BEAMMP_API}/getmods
"""
@app.route('/getmods', methods=['GET'])
def get_mod():
    folder_content = {}
    for nom in os.listdir(mod_folder):
        chemin_complet = os.path.join(mod_folder, nom)
        if os.path.isdir(chemin_complet):
            type_element = "dossier"
        else:
            type_element = "fichier"

        folder_content[nom] = {
            "type": type_element,
            "chemin": chemin_complet,
        }
    return jsonify(folder_content)

"""
Working request example :
curl https://{URL_TO_BEAMMP_API}/getmod/{mod_name}
"""
@app.route('/downmod/<mod_name>', methods=['GET'])
def download_mod(mod_name):
    # Get the path of the mod
    mod_path = os.path.join(mod_folder, mod_name)
    
    # Verify if the mod exists
    if os.path.exists(mod_path):
        # Verify if the mod is a file (and not a directory)
        if os.path.isfile(mod_path):
            return send_file(
               mod_path
            )
        else:
            return jsonify({"error": "Wrong mod"}), 404
    else:
        return jsonify({"error": "Wrong mod"}), 404
    
"""
Working request example :
https://{URL_TO_BEAMMP_API}/upmod/{mod_name}
"""
@app.route('/upmod', methods=['POST'])
def upload_mod():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and file.filename.endswith('.zip') :
        # Enregistrer le fichier
        file.save('path/to/save/' + file.filename)
        return 'Fichier uploadé avec succès !'
    return jsonify({"error": "File need to be a zip"}), 400


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
    return jsonify(request.json)

@app.route('/setconf/debug', methods=['POST'])
def set_conf_debug():
    return jsonify({"message": "Not implemented"}), 501

@app.route('/setconf/description', methods=['POST'])
def set_conf_description():
    return jsonify({"message": "Not implemented"}), 501

@app.route('/setconf/logchat', methods=['POST'])
def set_conf_logchat():
    return jsonify({"message": "Not implemented"}), 501

"""
Working request example :
curl -X POST https://beamapi.enzo-frnt.fr/setconf/map -H "Content-Type: application/json" -d '/levels/{Your_map}/info.json' 
"""
@app.route('/setconf/map', methods=['POST'])
def set_conf_map():
    app.logger.info(maps)
    request_data = request.get_data(as_text=True)
    app.logger.info(request_data)
    request_data_split = request_data.split("/")
    app.logger.info(request_data_split)
    app.logger.info(len(request_data))
    if len(request_data_split) == 4 and request_data_split[0] == "" and request_data_split[1] == "levels" and request_data_split[3] == "info.json" and request_data_split[2] in maps:
        if set_conf("Map") :
            return jsonify({"message": "Map changed"})
        else:
            return jsonify({"message": "Map not changed"})
    return jsonify({"error": "Wrong map"}), 501

@app.route('/setconf/maxcars', methods=['POST'])
def set_conf_maxcars():
    return jsonify({"message": "Not implemented"}), 501

@app.route('/setconf/maxplayers', methods=['POST'])
def set_conf_maxplayers():
    return jsonify({"message": "Not implemented"}), 501

@app.route('/setconf/name', methods=['POST'])
def set_conf_name():
    return jsonify({"message": "Not implemented"}), 501


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)

#Passage en prod
#gunicorn -w 4 -b 0.0.0.0:8081 myapp:app