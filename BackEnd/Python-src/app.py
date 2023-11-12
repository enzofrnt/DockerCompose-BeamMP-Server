"""

"""
from flask import Flask, jsonify, request
from multiprocessing import Process
from time import sleep
import os
import docker

client = docker.from_env()
app = Flask(__name__)
container_name = "beammp-server"
mod_folder = "/root/shared/Resources/Client/"

# Get the right container
def get_container():
    return client.containers.list(all=True,filters={"name": container_name})[0]

# Get status of the right container
def get_container_status():
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

@app.route('/start', methods=['GET'])
def start_container():
    # Start the container
    get_container().start()

    #Verify if the container is started
    if get_container_status()['status'] == 'running':
        return jsonify({"message": "Container started"})
    else:
        return jsonify({"message": "Container not started"})

@app.route('/stop', methods=['GET'])
def stop_container():
    # Stop the container
    get_container().stop()

    #Verify if the container is stopped
    if get_container_status()['status'] == 'exited':
        return jsonify({"message": "Container stopped"})
    else:
        return jsonify({"message": "Container not stopped"})

@app.route('/restart', methods=['GET'])
def restart_container():
    # Restart the container in a separte process
    Process(target=get_container().restart).start()

    sleep(1)

    #Verify if the container is restarring
    if get_container_status()['status'] == 'running':
        if get_container_status()['health'] == 'starting':
            return jsonify({"message": "Container restarting"})

    return jsonify({"message": "Container not restarting"})

@app.route('/status', methods=['GET'])
def status_container():
    return jsonify(get_container_status())



@app.route('/getmod', methods=['GET'])
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




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)