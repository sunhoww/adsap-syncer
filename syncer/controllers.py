from syncer import models, db
from time import time
from flask import request

KEY = 'password'

def is_correct_login_format(p):
    if 'userid' in p and 'key' in p:
        if request.path == '/login':
            return True
        if request.path == '/message' and 'messages' in p:
            return True
    return False

def is_correct_message_format(p):
    if 'id' in p and 'body' in p and 'deviceid' in p:
        return True
    return False

def is_user(p):
    user = models.User.query.get(p['userid'])
    if not user or p['key'] != user.key():
        return False
    return True

def get_conf(p):
    user = models.User.query.get(p['userid'])
    devices = user.devices
    resp = {}
    resp['name'] = user.name
    resp['devices'] = []
    for d in devices:
        tmp = {}
        tmp['name'] = d.name
        tmp['number'] = d.number
        tmp['commands'] = d.commands()
        tmp['alerts'] = d.alerts()
        resp['devices'].append(tmp)
    return resp

def get_conf_alt(p):
    user = models.User.query.get(p['userid'])
    devices = models.Device.query.filter_by(user=user).all()
    resp = {}
    resp['name'] = user.name
    resp['devices'] = []
    resp['commands'] = []
    resp['alerts'] = []
    for d in devices:
        tmp = {}
        tmp['id'] = d.id
        tmp['name'] = d.name
        tmp['number'] = d.number
        resp['devices'].append(tmp)
        for c in d.commands():
            tmp = {}
            tmp['commandname'] = c
            tmp['deviceid'] = d.id
            tmp['string'] = d.commands()[c]
            resp['commands'].append(tmp)
        for c in d.alerts():
            tmp = {}
            tmp['alertname'] = c
            tmp['deviceid'] = d.id
            tmp['string'] = d.alerts()[c]
            resp['alerts'].append(tmp)
    resp['status'] = 'OK'
    return conf

def msg_exists(p):
    if not models.Message.query.get(p['id']) is None:
        return True
    return False

def add_record(p):
    SENT = 1
    RCVD = 0
    resp = {
        'success': [],
        'error': []
    }
    user = models.User.query.get(p['userid'])
    for msg in p['messages']:
        if not is_correct_message_format(msg):
            if 'id' in msg:
                resp['error'].append({
                    'id': msg['id'],
                    'cause': 'Incorrect format'
                })
            else:
                resp['error'].append({
                    'id': '',
                    'cause': 'No id found'
                })
            continue
        if not user.has_device(msg['deviceid']):
            resp['error'].append({
                'id': msg['id'],
                'cause': p['userid'] + ' does not have access to ' + msg['deviceid']
            })
            continue
        if msg_exists(msg):
            resp['success'].append({
                'id': msg['id']
            })
            continue
        tmp = models.Message(id=msg['id'], body=msg['body'])
        tmp.user = user
        tmp.device = models.Device.query.get(msg['deviceid'])
        tmp.synctime = int(time() * 1000)
        if not 'time' in msg:
            tmp.time = tmp.synctime
        else:
            tmp.time = int(msg['time'])
        if not 'direction' in msg:
            tmp.direction = RCVD
        elif msg['direction'] == 'sent':
            tmp.direction = SENT
        elif msg['direction'] == 'received':
            tmp.direction = RCVD
        else:
            tmp.direction = RCVD
        try:
            db.session.add(tmp)
            db.session.commit()
            resp['success'].append({
                'id': msg['id']
            })
        except:
            resp['error'].append({
                'id': msg['id'],
                'cause': 'Fault with database insertion'
            })
    if len(resp['error']) == 0:
        del resp['error']
    return resp

def authenticate(p):
    if 'key' not in p:
        return False
    if p['key'] != KEY:
        return False
    return True

def user(p):
    if 'id' not in p or 'action' not in p:
        return {'error': 'Unacceptable format!'}
    u = models.User.query.get(p['id'])
    if p['action'] == 'update' or p['action'] == 'delete':
        if u is None:
            return {'error': p['id'] + ' not found!'}
        msg = ' ' + p['action'] +'d!'
    elif p['action'] == 'add':
        if not u is None:
            return {'error': p['id'] + ' exists. Impossible to overwrite!'}
        u = models.User(id=p['id'])
        msg = ' added!'
    else:
        return {'error': 'Unknown action!'}
    try:
        if p['action'] == 'delete':
            db.session.delete(u)
        else:
            if 'name' in p:
                u.name = p['name']
            if 'password' in p:
                u.password = p['password']
            if p['action'] == 'add':
                db.session.add(u)
        db.session.commit()
        return {'success': u.id + msg}
    except:
        return {'error': 'Insertion failed!'}

def device(p):
    if 'id' not in p or 'action' not in p:
        return {'error': 'Unacceptable format!'}
    u = models.Device.query.get(p['id'])
    if p['action'] == 'update' or p['action'] == 'delete':
        if u is None:
            return {'error': p['id'] + ' not found!'}
        msg = ' ' + p['action'] +'d!'
    elif p['action'] == 'add':
        if not u is None:
            return {'error': p['id'] + ' exists. Impossible to overwrite!'}
        u = models.Device(id=p['id'])
        msg = ' added!'
    else:
        return {'error': 'Unknown action!'}
    try:
        if p['action'] == 'delete':
            db.session.delete(u)
        else:
            if 'name' in p:
                u.name = p['name']
            if 'password' in p:
                u.password = p['password']
            if 'number' in p:
                u.number = p['number']
            if 'protocol' in p:
                u.protocol = p['protocol']
            if p['action'] == 'add':
                db.session.add(u)
        db.session.commit()
        return {'success': u.id + msg}
    except:
        return {'error': 'Insertion failed!'}

def relation(p):
    if 'userid' not in p or 'deviceid' not in p:
        return {'error': 'Unacceptable format!'}
    u = models.User.query.get(p['userid'])
    d = models.Device.query.get(p['deviceid'])
    if u is None:
        return {'error': p['userid'] + ' does not exist!'}
    if d is None:
        return {'error': p['deviceid'] + ' does not exist!'}
    if p['action'] == 'add':
        if d in u.devices.all():
            return {'error': 'Possible duplicate relation found!'}
        u.devices.append(d)
        msg = ' added to '
    elif p['action'] == 'delete':
        if d not in u.devices.all():
            return {'error': 'No relation found!'}
        u.devices.remove(d)
        msg = ' deleted from '
    else:
        return {'error': 'Unknown action!'}
    try:
        db.session.commit()
        return {'success': p['deviceid'] + msg + p['userid'] + '!'}
    except:
        return {'error': 'Modifying relationship failed!'}
