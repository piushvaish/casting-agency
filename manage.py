from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app
from models import db
# https://stackoverflow.com/questions/29872867/using-flask-migrate-with-flask-script-and-application-factory/29882346#29882346

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()