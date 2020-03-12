from battleship.models.game import GameModel
from battleship.models.ship import ShipModel
from battleship.models.location import LocationShipModel


class GameShot:
    def hit_ship(self, pos_x, pos_y):
        locations = LocationShipModel.query.all()
        locations_list = [location.get_ship_position() for location in locations]
        if (pos_x, pos_y) in locations_list:
            location = LocationShipModel.query.filter_by(position_x=pos_x, position_y=pos_y).one()
            ship = ShipModel.query.filter_by(
                id=location.ship_id
            ).one()  # get ship model that have the same id of ship_id in location model
            if (
                location.check_last_piece_of_ship()
                or location.check_first_piece_of_ship()
                or (ship.hit + 1) == ship.size
            ):

                ship.sink = True  # save this ship is sink
                ship.save_to_db()
                return "SINK"

            else:
                ship.hit += 1
                ship.save_to_db()
                return "HIT"
        return "WATER"
