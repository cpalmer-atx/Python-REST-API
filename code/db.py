from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy object that will link to flask app and
# look at all the objects we tell it to which allows us
# to map those objects to rows in a database
db = SQLAlchemy()