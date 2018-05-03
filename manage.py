from flask_migrate import  MigrateCommand
from flask_script import Manager
import os

from app import  db, create_app


manager = Manager(create_app)
manager.add_option("-c", "--development", dest="config_module", required=False)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
   