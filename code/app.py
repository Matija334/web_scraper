from datetime import datetime

from flask import Flask
from extensions import db
from models.match import Match
from routes.match import match_bp
from routes.xml2json import xml2json_bp
from routes.json2xml import json2xml_bp
from routes.scraper import scraper_bp
from routes.upload import upload_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(match_bp)
    app.register_blueprint(xml2json_bp)
    app.register_blueprint(json2xml_bp)
    app.register_blueprint(scraper_bp)
    app.register_blueprint(upload_bp)

    with app.app_context():
        db.create_all()
        initialize_data()

    return app


def initialize_data():
    if Match.query.count() == 0:
        matches = [
            Match(home_team="Slovenia", away_team="Kazahstan", datetime=datetime(2023, 3, 15, 20, 0),
                  result="2:1", competition_type="Kvalifikacije za EP 2024")
        ]
        db.session.add_all(matches)

    db.session.commit()


if __name__ == '__main__':
    create_app().run(debug=True)
