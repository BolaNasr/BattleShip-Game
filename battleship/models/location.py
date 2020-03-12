from . import db


class LocationShipModel(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    position_x = db.Column(db.SmallInteger, nullable=False)
    position_y = db.Column(db.SmallInteger, nullable=False)
    first_piece = db.Column(db.Boolean, default=False)
    last_piece = db.Column(db.Boolean, default=False)

    ship_id = db.Column(db.Integer, db.ForeignKey("ships.id"))

    def __init__(self, position_x, position_y, first_piece_of_ship=False, last_piece_of_ship=False, ship_id=0):
        self.ship_id = ship_id
        self.position_x = position_x
        self.position_y = position_y
        self.first_piece = first_piece_of_ship
        self.last_piece = last_piece_of_ship

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def get_ship_position(self):
        return (self.position_x, self.position_y)

    def check_first_piece_of_ship(self):
        return self.first_piece

    def check_last_piece_of_ship(self):
        return self.last_piece
