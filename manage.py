import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src.config.config import Config


from src.models import db
from src import create_app

app = create_app()
db.app = app
db.init_app(app)

# app.config.from_object(os.environ['APP_SETTINGS'])
app.config['APP_SETTINGS'] = Config

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()