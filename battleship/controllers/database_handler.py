from battleship.models.game import GameModel
from battleship.models.ship import ShipModel
from battleship.models.location import LocationShipModel


def delete_records():
    delete_location_records()
    delete_ship_records()
    delete_game_records()


def delete_location_records():
    locations = LocationShipModel.query.all()
    for location in locations:
        location.delete_from_db()


def delete_ship_records():
    ships = ShipModel.query.all()
    for ship in ships:
        ship.delete_from_db()


def delete_game_records():
    games = GameModel.query.all()
    for game in games:
        game.delete_from_db()

