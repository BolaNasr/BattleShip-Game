from .location import LocationShipModel
from . import db


class ShipModel(db.Model):
    __tablename__ = "ships"

    id = db.Column(db.Integer, primary_key=True)
    origin_x = db.Column(db.SmallInteger, nullable=False)
    origin_y = db.Column(db.SmallInteger, nullable=False)
    size = db.Column(db.SmallInteger, nullable=False)
    direction = db.Column(db.String(1))
    sink = db.Column(db.Boolean, default=False, index=True)
    hit = db.Column(db.SmallInteger, default=0, index=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    locations = db.relationship("LocationShipModel", backref="ship", lazy="dynamic")

    def __init__(self, game_id, origin_x, origin_y, size, direction):
        self.game_id = game_id
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.size = size
        self.direction = direction

    def get_ship_size(self):
        return self.size

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
