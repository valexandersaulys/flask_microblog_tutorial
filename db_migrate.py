#!flask/bin/python
"""
The script looks more complicated than it is. The way SQLAlchemy-migrate creates
a migration is by comparing the structure of the database (obtained in our case
from app.db) against the structure of our models (obtained from app/models.py).
The differences between the two are recorded as a migration script inside the 
migration repository. The migration script knows how to apply a migration or 
undo it, so it is always possible to upgrade or downgrade a database format.

To make it more easy for SQLAlchemy-migrate to determine the changes, 
  - never rename existing fields
  - limit changes to adding or removing models or fields
  - changing types of existing fields
"""
import imp
from migrate.versioning import api
from app import db
from config import SQLALCHEMY_DATABASE_URI  # where the database is located
from config import SQLALCHEMY_MIGRATE_REPO
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
tmp_module = imp.new_module('old_model')
old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
exec(old_model, tmp_module.__dict__)
script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
                                          tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print "New Migration saved as " + migration;
print "Current Database version: " + str(v)
