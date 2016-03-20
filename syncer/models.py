from syncer import db
from syncer.helpers import java_string_hashcode

protocols = ['gpsq103', 'gt02']

assoc = db.Table('assoc',
    db.Column('userid', db.String(128), db.ForeignKey('user.id')),
    db.Column('deviceid', db.String(128), db.ForeignKey('device.id'))
)

class User(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(128), index=True)
    password = db.Column(db.String(32))
    devices = db.relationship('Device', secondary=assoc,
        back_populates='users', lazy='dynamic')
    messages = db.relationship('Message', backref='user', lazy='dynamic')

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<User %r %r>' % (self.id, self.name)

    def key(self):
        return java_string_hashcode(self.id + self.password)

    def has_device(self, deviceid):
        d = Device.query.get(deviceid)
        if d in self.devices:
            return True
        return False

class Device(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(128), index=True)
    password = db.Column(db.String(16))
    number = db.Column(db.String(16), index=True, unique=True)
    protocol = db.Column(db.String(16))
    users = db.relationship('User', secondary=assoc,
        back_populates='devices', lazy='dynamic')
    messages = db.relationship('Message', backref='device', lazy='dynamic')

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<Device %r - %r>' % (self.id, self.name)

    def commands(self):
        r = {}
        if self.protocol == 'gps103':
            r['stop'] = 'stop' + self.password
            r['resume'] = 'resume' + self.password
            r['arm'] = 'arm' + self.password
            r['disarm'] = 'disarm' + self.password
            r['monitor'] = 'monitor' + self.password
            r['track'] = 'tracker' + self.password
        if self.protocol == 'gt06':
            r['stop'] = '#stopelec#' + self.password + '#'
            r['resume'] = '#supplyelec#' + self.password + '#'
            r['arm'] = '#ACC#ON#'
            r['disarm'] = '#ACC#OFF#'
            r['monitor'] = '#monitor#' + self.password + '#'
            r['track'] = '#tracker#' + self.password + '#'
            r['call'] = '#call#' + self.password + '#'
        return r

    def alerts(self):
        r = {}
        if self.protocol == 'gps103':
            r['door'] = 'Door alarm!'
            r['acc'] = 'ACC alarm!'
            r['sos'] = 'help me!'
            r['sensor'] = 'sensor alarm!'
            r['power'] = 'power alarm!'
        if self.protocol == 'gt06':
            r['acc'] = 'ACC!!'
            r['sos'] = 'SOS alarm!'
            r['power'] = 'cut power alert!'
        return r

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(128), db.ForeignKey('user.id'))
    deviceid = db.Column(db.String(128), db.ForeignKey('device.id'))
    time = db.Column(db.Integer)
    body = db.Column(db.String(140))
    direction = db.Column(db.Integer)
    synctime = db.Column(db.Integer)

    def __init__(self, id, body):
        self.id = id
        self.body = body

    def __repr__(self):
        return '<Message %r - %r>' % (self.synctime, self.body)
