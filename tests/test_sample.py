import unittest
from os import path

from flask_sqlalchemy import SQLAlchemy

from boltfile import PROJECT_ROOT
import json
from battleship.api import app
from battleship.models import db


class TestSampleClass(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + path.join(PROJECT_ROOT, "data.db")
        with app.test_request_context():
            db.init_app(app)
            db.drop_all()
            db.create_all()
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def _load_json_data(self, file_name):
        with open(path.join("tests/test_data", file_name + ".txt")) as json_file:
            data = json.load(json_file)
        return data

    def test_main_api(self):
        response = self.app.get("/", follow_redirects=False)
        self.assertEqual(response.status_code, 404)

    def test_create_invalid_game_in_x(self):
        my_ships = self._load_json_data("game_with_out_of_border_x")

        response = self.app.post("/battleship", json=my_ships)
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_game_in_y(self):
        my_ships = self._load_json_data("game_with_out_of_border_y")

        response = self.app.post("/battleship", json=my_ships)
        self.assertEqual(response.status_code, 400)

    def test_create_game(self):
        my_ships = self._load_json_data("game_start")

        response = self.app.post("/battleship", json=my_ships)
        self.assertEqual(response.status_code, 200)

    def test_create_game_with_overlapped(self):
        my_ships = self._load_json_data("game_with_overlapped")

        response = self.app.post("/battleship", json=my_ships)
        self.assertEqual(response.status_code, 400)

    def test_hit_shot(self):
        my_ships = self._load_json_data("game_start")

        response = self.app.post("/battleship", json=my_ships)

        hit_position = {"x": 3, "y": 1}

        response = self.app.put("/battleship", json=hit_position)
        self.assertEqual(response.json["message"], "HIT..!!")

    def test_missing_shot(self):
        my_ships = self._load_json_data("game_start")

        response = self.app.post("/battleship", json=my_ships)

        hit_position = {"x": 0, "y": 0}

        response = self.app.put("/battleship", json=hit_position)
        self.assertEqual(response.json["message"], "WATER")

    def test_sink_shot(self):
        my_ships = self._load_json_data("game_start")

        response = self.app.post("/battleship", json=my_ships)

        hit_position = {"x": 2, "y": 1}

        response = self.app.put("/battleship", json=hit_position)
        self.assertEqual(response.json["message"], "SINK..!!")

    def test_end_game(self):
        my_ships = self._load_json_data("game_start")

        response = self.app.post("/battleship", json=my_ships)

        response = self.app.delete("/battleship")
        self.assertEqual(response.json["message"], "GAME END..")

    def tearDown(self):
        with app.test_request_context():
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
