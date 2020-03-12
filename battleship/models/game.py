from . import db
from .ship import ShipModel
from datetime import datetime

class GameModel(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    number_of_ships = db.Column(db.Integer)
    ships = db.relationship("ShipModel", backref="game")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, number_of_ships):
        self.number_of_ships = number_of_ships

    def get_number_of_ships(self):
        return self.number_of_ships

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

