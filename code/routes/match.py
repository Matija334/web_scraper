# routes/match.py
from flask import Blueprint, request, jsonify, render_template
from models.match import Match
from extensions import db
from datetime import datetime

match_bp = Blueprint('match_bp', __name__)

@match_bp.route('/matches', methods=['GET'])
def get_matches():
    matches = Match.query.all()
    return render_template('matches.html', matches=matches)


@match_bp.route('/match', methods=['POST'])
def add_match():
    data = request.get_json()
    if 'home_team' not in data or 'away_team' not in data or 'datetime' not in data or 'result' not in data or 'competition_type' not in data:
        return jsonify({'message': 'Missing data, could not create match'}), 400

    try:
        match_datetime = datetime.strptime(data['datetime'], '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return jsonify({'message': 'Invalid datetime format, use YYYY-MM-DDTHH:MM:SS'}), 400

    new_match = Match(id_match=data["id_match"], home_team=data['home_team'], away_team=data['away_team'], datetime=match_datetime,
                      result=data['result'], competition_type=data['competition_type'])
    db.session.add(new_match)
    db.session.commit()
    return jsonify({'message': 'Match added successfully', 'id': new_match.id}), 201


@match_bp.route('/match/<int:id>', methods=['GET'])
def get_match(id):
    match = Match.query.get(id)
    if not match:
        return jsonify({'message': 'Match not found'}), 404

    match_data = {
        'id': match.id,
        'home_team': match.home_team,
        'away_team': match.away_team,
        'datetime': match.datetime.isoformat(),
        'result': match.result,
        'competition_type': match.competition_type
    }
    return jsonify(match_data), 200


@match_bp.route('/match/<int:id>', methods=['PUT'])
def update_match(id):
    match = Match.query.get(id)
    if not match:
        return jsonify({'message': 'Match not found'}), 404

    data = request.get_json()
    if 'home_team' in data:
        match.home_team = data['home_team']
    if 'away_team' in data:
        match.away_team = data['away_team']
    if 'datetime' in data:
        try:
            match.datetime = datetime.strptime(data['datetime'], '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            return jsonify({'message': 'Invalid datetime format, use YYYY-MM-DDTHH:MM:SS'}), 400
    if 'result' in data:
        match.result = data['result']
    if 'competition_type' in data:
        match.competition_type = data['competition_type']

    db.session.commit()
    return jsonify({'message': 'Match updated successfully'}), 200


@match_bp.route('/match/<int:id>', methods=['DELETE'])
def delete_match(id):
    match = Match.query.get(id)
    if not match:
        return jsonify({'message': 'Match not found'}), 404

    db.session.delete(match)
    db.session.commit()
    return jsonify({'message': 'Match deleted successfully'}), 200
