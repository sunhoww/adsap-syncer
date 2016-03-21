from syncer import models, db
from syncer.helpers import get_epoch, get_stime
from flask import request
from config import SYNCER_ADMIN_KEY as KEY

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
        # tmp['id'] = d.id
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

SENT = 1
RCVD = 0

def add_record(p):

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
        tmp.synctime = get_epoch()
        if not 'time' in msg:
            tmp.time = tmp.synctime
        else:
            tmp.time = get_epoch(msg['time'])
        if not 'direction' in msg:
            tmp.direction = RCVD
        elif msg['direction'] == 'S':
            tmp.direction = SENT
        elif msg['direction'] == 'R':
            tmp.direction = RCVD
        else:
            tmp.direction = -1
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
            elif p['action'] == 'add':
                u.number = p['id']
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

def get_user_dict(p, show_usr_pass=False, show_dev_pass=False, show_messages=False, show_dev_id_only=False):
    r = {}
    if p is None:
        return r
    r['id'] = p.id
    r['name'] = p.name
    if show_usr_pass:
        r['password'] = p.password
    r['devices'] = []
    for d in p.devices.all():
        tmp = {}
        tmp['id'] = d.id
        if not show_dev_id_only:
            tmp['name'] = d.name
            tmp['number'] = d.number
            if show_dev_pass:
                tmp['password'] = d.password
            tmp['protocol'] = d.protocol
        r['devices'].append(tmp)
    if show_messages:
        r['messages'] = []
        for m in p.messages.all():
            tmp = {}
            tmp['id'] = m.id
            tmp['deviceid'] = m.deviceid
            tmp['time'] = get_stime(m.time)
            tmp['body'] = m.body
            if m.direction == RCVD:
                tmp['direction'] = 'received'
            elif m.direction == SENT:
                tmp['direction'] = 'sent'
            else:
                tmp['direction'] = ''
            tmp['synctime'] = get_stime(m.synctime)
            r['messages'].append(tmp)
    r['messageCount'] = len(p.messages.all())
    return r

def list_users(p):
    resp = {}
    show_usr_pass = False
    show_dev_pass = False
    show_messages = False
    show_dev_id_only = False
    if 'include' in p:
        show_usr_pass = 'userpassword' in p['include']
        show_dev_pass = 'devicepassword' in p['include']
        show_messages = 'messages' in p['include']
    if 'id' in p:
        user = models.User.query.get(p['id'])
        if user is None:
            return {'error': p['id'] + ' does not exist!'}
        resp = get_user_dict(user, show_usr_pass, show_dev_pass, show_messages)
    else:
        resp['users'] = []
        for u in models.User.query.all():
            resp['users'].append(get_user_dict(u, show_usr_pass, show_dev_pass, show_messages, not show_dev_id_only))
    return resp
