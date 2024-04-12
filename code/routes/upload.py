# routes/upload.py
from flask import Blueprint, request, render_template, jsonify
import json
import xml.etree.ElementTree as ET
from io import StringIO

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/upload-json', methods=['GET', 'POST'])
def upload_json():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return "No file uploaded", 400

        content = json.load(file)

        if isinstance(content, dict):
            if len(content) == 1 and isinstance(next(iter(content.values())), list):
                content = next(iter(content.values()))
            else:
                content = [content]

        return render_template('display_json.html', data=content)

    return render_template('upload_json.html')



@upload_bp.route('/upload-xml', methods=['GET', 'POST'])
def upload_xml():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return "No file uploaded", 400

        xml_content = file.read().decode('utf-8')
        xml_content = xml_content.replace('&', '&amp;')

        xml_file_like = StringIO(xml_content)

        tree = ET.parse(xml_file_like)
        root = tree.getroot()

        # Pretvorba XML v seznam slovarjev za prikaz v tabeli
        data = [{child.tag: child.text for child in element} for element in root]

        return render_template('display_xml.html', data=data)

    return render_template('upload_xml.html')

