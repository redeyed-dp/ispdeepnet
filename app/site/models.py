from app import db

class Region(db.Model):
    __bind_key__ = 'site'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    ru = db.Column(db.String(64))
    ua = db.Column(db.String(64))

class Price(db.Model):
    __bind_key__ = 'site'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    region = db.Column(db.Integer, db.ForeignKey('region.id'))
    service = db.Column(db.String(1))
    ru = db.Column(db.String(64))
    ua = db.Column(db.String(64))
    speed = db.Column(db.Integer)
    price = db.Column(db.Numeric(precision=6, scale=2))

class Feedback(db.Model):
    __bind_key__ = 'site'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    time = db.Column(db.DateTime)
    ip = db.Column(db.String(15))
    name = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    message = db.Column(db.String(2048))

class Articles(db.Model):
    __bind_key__ = 'site'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    visible = db.Column(db.Boolean)
    ru_name = db.Column(db.String(128))
    ua_name = db.Column(db.String(128))
    ru_text = db.Column(db.Text)
    ua_text = db.Column(db.Text)