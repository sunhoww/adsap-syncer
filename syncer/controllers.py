from flask import request, json, url_for
from werkzeug.exceptions import BadRequest

from syncer import models, db
from syncer.helpers import get_epoch, get_stime, \
    bad_request, not_found, missing_parameters, already_exists, \
    success_insert, success_update, success_remove
from config import syncer_admin_key as KEY

def is_correct_login_format(p):
    if 'userid' in p and 'key' in p:
        if request.path == '/login':
            return True
        if request.path == '/message' and 'messages' in p:
            return True
    return False

def is_correct_message_format(p):
    if 'id' in p and 'body' in p and 'number' in p:
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
        if not user.has_number(msg['number']):
            resp['error'].append({
                'id': msg['id'],
                'cause': p['userid'] + ' does not have access to ' + msg['number']
            })
            continue
        if msg_exists(msg):
            resp['success'].append({
                'id': msg['id']
            })
            continue
        tmp = models.Message(id=msg['id'], body=msg['body'])
        tmp.user = user
        tmp.device = user.devices.filter_by(number=msg['number']).first()
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

# admin

def list_items(id):
    resp = {}
    if id is None:
        if request.path == '/users':
            resp['users'] = []
            for r in models.User.query.all():
                resp['users'].append(r.get(count_links=True))
        elif request.path == '/devices':
            resp['devices'] = []
            for r in models.Device.query.all():
                resp['devices'].append(r.get(count_links=True))
    else:
        r = None
        if request.path == '/users/' + id:
            r = models.User.query.get(id)
        elif request.path == '/devices/' + id:
            r = models.Device.query.get(id)
        if r is None:
            return not_found(id)
        resp = r.get(with_links=True, count_messages=True)
    return json.jsonify(resp)

def insert_item():
    try:
        p = request.get_json()
    except BadRequest:
        return bad_request()
    if 'id' not in p:
        return missing_parameters()
    r = None
    if request.path == '/users':
        if not models.User.query.get(p['id']) is None:
            return already_exists(p['id'])
        r = models.User(p['id'])
    elif request.path == '/devices':
        if not models.Device.query.get(p['id']) is None:
            return already_exists(p['id'])
        r = models.Device(p['id'])
    r.put(p)
    db.session.add(r)
    db.session.commit()
    return success_insert(p['id'])

def update_item(id):
    try:
        p = request.get_json()
    except BadRequest:
        return bad_request()
    r = None
    if request.path == '/users/' + id:
        r = models.User.query.get(id)
    elif request.path == '/devices/' + id:
        r = models.Device.query.get(id)
    if r is None:
        return not_found(id)
    r.put(p)
    if 'link' in p:
        r.link(p['link'])
    if 'unlink' in p:
        r.unlink(p['unlink'])
    db.session.add(r)
    db.session.commit()
    return success_update(id)

def remove_item(id):
    r = None
    if request.path == '/users/' + id:
        r = models.User.query.get(id)
    elif request.path == '/devices/' + id:
        r = models.Device.query.get(id)
    if r is None:
        return not_found(id)
    db.session.delete(r)
    db.session.commit()
    return success_remove(id)
