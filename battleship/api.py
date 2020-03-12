from http import HTTPStatus

from flask import Flask, jsonify, request

app = Flask(__name__)

from battleship.controllers.game_start import StartGame
from battleship.controllers.game_shot import GameShot
from battleship.controllers.database_handler import delete_records


@app.route("/battleship", methods=["POST"])
def create_battleship_game():
    delete_records()
    request_data = request.get_json()
    game_start = StartGame(request_data["ships"])

    ship_locations_are_correct = game_start.create_ships()
    if not ship_locations_are_correct:
        return jsonify(message="Please, check request data."), HTTPStatus.BAD_REQUEST

    ships_has_unique_location = game_start.check_duplicate_ships_location()
    if not ships_has_unique_location:
        return jsonify(message="Please, check request data."), HTTPStatus.BAD_REQUEST

    return jsonify(message="Game created successfully."), HTTPStatus.OK


@app.route("/battleship", methods=["PUT"])
def shot():
    request_data = request.get_json()
    result = GameShot().hit_ship(request_data["x"], request_data["y"])
    if result == "HIT":
        return jsonify(message="HIT..!!"), HTTPStatus.OK
    elif result == "SINK":
        return jsonify(message="SINK..!!"), HTTPStatus.OK
    else:
        return jsonify(message="WATER"), HTTPStatus.OK


@app.route("/battleship", methods=["DELETE"])
def delete_battleship_game():
    delete_records()
    return jsonify(message="GAME END.."), HTTPStatus.OK

