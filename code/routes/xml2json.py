from io import StringIO
from flask import Blueprint, request, send_file, render_template
import xmltodict
import json

xml2json_bp = Blueprint('xml2json_bp', __name__)

@xml2json_bp.route('/xml2json', methods=['GET'])
def upload_form():
    return render_template('xml2json.html')

@xml2json_bp.route('/xml2json', methods=['POST'])
def upload_xml():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file:
        xml_data = file.read().decode('utf-8')
        xml_data = xml_data.replace('&', '&amp;')
        dict_data = xmltodict.parse(xml_data)

        tekme_data = dict_data.get('tekme', {}).get('tekma', [])
        json_data = json.dumps({"tekme": tekme_data}, indent=4)

        json_filename = 'converted.json'
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json_file.write(json_data)

        return send_file(json_filename, as_attachment=True)

    return render_template('xml2json.html')
