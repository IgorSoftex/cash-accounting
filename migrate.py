from app import app, db
from flask_migrate import Migrate


migrate = Migrate(app, db, command='db')   # https://flask-migrate.readthedocs.io/en/latest/
app.app_context().push()    # Ihor

# you can create a migration repository with the following command:
# flask db init

# You can then generate an initial migration:
# flask db migrate -m "Initial migration."

# Then you can apply the changes described by the migration script to your database:
# flask db upgrade
