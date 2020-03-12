from battleship import api
from battleship.models import db
from flask_migrate import Migrate

with api.app.test_request_context():
    db.init_app(api.app)
    db.create_all()

api.app.run()
