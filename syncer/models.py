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

    def has_number(self, num):
        d = Device.query.filter_by(number=num).first()
        if d in self.devices:
            return True
        return False

    def get(self, with_password=False, with_links=False, count_links=False, count_messages=False):
        r = {}
        r['id'] = self.id
        r['name'] = self.name
        if with_password:
            r['password'] = seld.password
        if with_links:
            r['devices'] = []
            for d in self.devices.all():
                r['devices'].append(d.get())
        if count_links:
            r['devicecount'] = len(self.devices.all())
        if count_messages:
            r['messagecount'] = len(self.messages.all())
        return r

    def get_msgs(self):
        r = []
        for m in self.messages.all():
                tmp = {}
                tmp['id'] = m.id
                tmp['deviceid'] = m.device.id
                tmp['time'] = m.time
                tmp['body'] = m.body
                tmp['direction'] = m.direction
                tmp['synctime'] = m.synctime
                r.append(tmp)
        return r

    def put(self, p):
        if 'name' in p:
            self.name = p['name']
        if 'password' in p:
            self.password = p['password']

    def link(self, darr):
        for d in darr:
            i = Device.query.get(d)
            if not i is None and not self.has_device(d):
                self.devices.append(i)

    def unlink(self, darr):
        for d in darr:
            if self.has_device(d):
                self.devices.remove(i)

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

    def get(self, with_password=False, with_links=False, count_links=False, count_messages=False):
        r = {}
        r['id'] = self.id
        r['name'] = self.name
        r['number'] = self.number
        r['protocol'] = self.protocol
        if with_password:
            r['password'] = seld.password
        if with_links:
            r['users'] = []
            for d in self.users.all():
                r['users'].append(d.get())
        if count_links:
            r['usercount'] = len(self.users.all())
        if count_messages:
            r['messagecount'] = len(self.messages.all())
        return r
    def get_msgs(self):
        r = []
        for m in self.messages.all():
                tmp = {}
                tmp['id'] = m.id
                tmp['deviceid'] = m.user.id
                tmp['time'] = m.time
                tmp['body'] = m.body
                tmp['direction'] = m.direction
                tmp['synctime'] = m.synctime
                r.append(tmp)
        return r

    def put(self, p):
        if 'name' in p:
            self.name = p['name']
        if 'password' in p:
            self.password = p['password']
        if 'number' in p:
            self.number = p['number']
        if 'name' in p:
            self.protocol = p['protocol']

        def link(self, darr):
            for d in darr:
                i = User.query.get(d)
                if not i is None:
                    self.devices.append(i)

        def unlink(self, darr):
            for d in darr:
                i = User.query.get(d)
                if not i is None:
                    self.devices.remove(i)

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
    body = db.Column(db.String(160))
    direction = db.Column(db.Integer)
    synctime = db.Column(db.Integer)

    def __init__(self, id, body):
        self.id = id
        self.body = body

    def __repr__(self):
        return '<Message %r - %r>' % (self.synctime, self.body)
