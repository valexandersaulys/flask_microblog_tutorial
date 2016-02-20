from app import db

class User(db.Model):
    """
    The user class that we just created has fields defined as class variables. 
    These fields are created as instances of the db.Column class, which takes a
    field type as an argument plus some other optional arguments.

    The __repr__ method tells python how to print objects of this class. It is
    used for debugging.
    """
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # This is key!

    def __repr__(self):
        return '<Post %r>' % (self.body)
