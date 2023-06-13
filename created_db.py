from fakepin import database, app
from fakepin.models import Usuario, Foto


with app.app_context():
  database.create_all()