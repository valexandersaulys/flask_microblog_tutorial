WTF_CSRF_ENABLED = True
SECRET_KEY = "beautiful_little_world_is_mine"


# - - - - - For the Database Configuration
import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
