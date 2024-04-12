# routes/upload.py
from flask import Blueprint, request, send_file, render_template
import xmltodict
import json
import os

json2xml_bp = Blueprint('json2xml_bp', __name__)

@json2xml_bp.route('/json2xml', methods=['GET'])
def upload_form():
    return render_template('json2xml.html')

@json2xml_bp.route('/json2xml', methods=['POST'])
def upload_xml():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file:
        json_data = json.load(file)
        if isinstance(json_data, dict):
            root_element_name = "root"
            wrapped_json_data = {root_element_name: json_data}
        else:
            return "Invalid JSON structure", 400

        xml_data = xmltodict.unparse(wrapped_json_data, pretty=True)

        xml_filename = 'converted.xml'
        with open(xml_filename, 'w', encoding='utf-8') as xml_file:
            xml_file.write(xml_data)

        return send_file(xml_filename, as_attachment=True)
