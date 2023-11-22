import os
import time

from flask import Blueprint, jsonify, redirect, request, send_file


mod_folder = "/root/shared/Resources/Client/"

mods = Blueprint('mods',__name__)

"""
Working request example :
curl https://{URL_TO_BEAMMP_API}/getmods
"""
@mods.route('/getmods', methods=['GET'])
def get_mod():
    folder_content = {}
    for nom in os.listdir(mod_folder):
        chemin_complet = os.path.join(mod_folder, nom)
        if os.path.isfile(chemin_complet):
            type_element = "fichier"
            if nom.endswith(".stop") and nom[:-5].endswith(".zip") :
                mod_status = False
                folder_content[nom[:-5]] = {
                    "type": type_element,
                    "path": chemin_complet[:-5],
                    "enable": mod_status
                }
            elif nom.endswith(".zip"):
                mod_status = True
                folder_content[nom] = {
                    "type": type_element,
                    "path": chemin_complet,
                    "enable": mod_status
                }
    return jsonify(folder_content)

"""
Working request example :
curl https://{URL_TO_BEAMMP_API}/disable/{mod_name}
"""
@mods.route('/disable/<mod>', methods=['GET'])
def disable_mod(mod):
    if os.path.exists(os.path.join(mod_folder, mod + ".zip")):
        os.rename(os.path.join(mod_folder, mod + ".zip"), os.path.join(mod_folder, mod + ".zip" + ".stop"))
        current_time = time.time()
        os.utime(os.path.join(mod_folder, mod + ".zip" + ".stop"), (current_time, current_time))
        return jsonify({"message": "Mod disabled"})
    else:
        return jsonify({"error": "Mod not found"}), 404


"""
Working request example :
curl https://{URL_TO_BEAMMP_API}/enable/{mod_name}
"""
@mods.route('/enable/<mod>', methods=['GET'])
def enable_mod(mod):
    if os.path.exists(os.path.join(mod_folder, mod + ".zip" + ".stop")):
        os.rename(os.path.join(mod_folder, mod + ".zip" + ".stop"), os.path.join(mod_folder, mod + ".zip"))
        current_time = time.time()
        os.utime(os.path.join(mod_folder, mod + ".zip"), (current_time, current_time))
        return jsonify({"message": "Mod enabled"})
    else:
        return jsonify({"error": "Mod not found"}), 404

"""
Working request example :
curl https://{URL_TO_BEAMMP_API}/downmod/{mod_name}
"""
@mods.route('/downmod/<mod_name>', methods=['GET'])
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
@mods.route('/upmod', methods=['POST'])
def upload_mod():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and file.filename.endswith('.zip') :
        # Check if the mod already exists
        if os.path.exists(os.path.join(mod_folder, file.filename)):
            return jsonify({"error": "Mod already exists"}), 400
        file.save('/root/shared/Resources/Client/' + file.filename)
        return 'Fichier uploadé avec succès !'
    return jsonify({"error": "File need to be a zip"}), 400