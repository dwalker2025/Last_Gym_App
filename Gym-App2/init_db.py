# init_db.py (in root directory)
from app import create_app, db
from flask_migrate import Migrate, upgrade, init, migrate

app = create_app()
migrate = Migrate(app, db)

with app.app_context():
    init()
    migrate(message="Initial migration")
    upgrade()

print("Database initialized successfully!")
