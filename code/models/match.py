from extensions import db

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_team = db.Column(db.String(80), nullable=False)
    away_team = db.Column(db.String(80), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    result = db.Column(db.String(120), nullable=False)
    competition_type = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Match {self.home_team} vs {self.away_team} on {self.datetime}>'
