from battleship.models.game import GameModel
from battleship.models.ship import ShipModel
from battleship.models.location import LocationShipModel


class StartGame:
    def __init__(self, payload):
        self.payload = payload
        self.game_model = GameModel(len(self.payload))
        self.game_model.save_to_db()

    def create_ships(self):
        for ship in self.payload:
            ship_db = ShipModel(
                game_id=self.game_model.id,
                origin_x=ship["x"],
                origin_y=ship["y"],
                size=ship["size"],
                direction=ship["direction"],
            )
            ship_db.save_to_db()
            location_check = self.check_ships_location(
                ship_id=ship_db.id, x=ship["x"], y=ship["y"], size=ship["size"], direction=ship["direction"]
            )
            if not location_check:
                return False
        return True

    def _ship_in_game_board(self, position_x, position_y):
        """
        check if this coordinate in game board
        """
        return (position_x >= 0 and position_x <= 9) and (position_y >= 0 and position_y <= 9)

    def check_ships_location(self, ship_id, x, y, size, direction):
        """
        calculate all position that ship took
        """
        if direction == "H":  # check the orientation is Horizontal
            start = x
            end = x + size
            return self.check_all_locations_in_board(ship_id=ship_id, start=start, end=end, position_y=y)

        else:
            if direction == "V":  # check the orientation is Vertical
                start = y
                end = y + size
                return self.check_all_locations_in_board(ship_id=ship_id, start=start, end=end, position_x=x)

    def check_all_locations_in_board(self, start, end, ship_id, position_x=None, position_y=None):
        """
        check ships in game board
        """
        for pos in range(start, end):
            if position_x:
                if not self._ship_in_game_board(position_x, pos):
                    return False
                if start == pos:  # check it's first piece of ship to retun SINK if hit this position
                    ship_location = LocationShipModel(position_x, pos, first_piece_of_ship=True, ship_id=ship_id)
                elif end == pos:  # check it's last piece of ship to retun SINK if hit this position
                    ship_location = LocationShipModel(position_x, pos, last_piece_of_ship=True, ship_id=ship_id)
                else:
                    ship_location = LocationShipModel(position_x, pos, ship_id=ship_id)

                ship_location.save_to_db()  # save location model in database

            else:
                if not self._ship_in_game_board(pos, position_y):
                    return False
                if start == pos:
                    ship_location = LocationShipModel(pos, position_y, first_piece_of_ship=True, ship_id=ship_id)
                elif end == pos:
                    ship_location = LocationShipModel(pos, position_y, last_piece_of_ship=True, ship_id=ship_id)
                else:
                    ship_location = LocationShipModel(pos, position_y, ship_id=ship_id)
            ship_location.save_to_db()
        return True

    def check_duplicate_ships_location(self):
        locations = LocationShipModel.query.all()
        locations_list = [location.get_ship_position() for location in locations]
        locations_set = set(locations_list)  # to remove any duplicate records
        return len(locations_list) == len(locations_set)

