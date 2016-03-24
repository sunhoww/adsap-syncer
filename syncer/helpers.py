import time
from flask import json, Response, url_for, request

VALIDITY = 1800

def get_epoch(s=None):
    if s is None:
        return int(time.time())
    try:
        if len(s) < 14:
            raise ValueError
        return int(time.mktime(time.strptime(s[:14], "%Y%m%d%H%M%S")))
    except ValueError:
        return -1

def get_stime(s=None):
    if s < 0:
        return time.asctime()
    return time.asctime(time.gmtime(s))

# http://garage.pimentech.net/libcommonPython_src_python_libcommon_javastringhashcode/
def java_string_hashcode(s):
    h = 0
    for c in s:
        h = (31 * h + ord(c)) & 0xFFFFFFFF
    return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000

def stamp():
    return ''

def bad_request():
    """for handling bad requests"""
    js = json.dumps({'error': 'Accepts only JSON.'})
    return Response(js, status=400, mimetype='application/json')

def incorrect_format():
    """for handling incorrect json format"""
    js = json.dumps({'error': 'Incorrect format.'})
    return Response(js, status=422, mimetype='application/json')

def unauthorized():
    """for unauthorized connections"""
    js = json.dumps({'error': 'Unauthorized access.'})
    return Response(js, status=403, mimetype='application/json')

def not_found(s):
    js = json.dumps({'error': str(s) + ' does not exist!'})
    return Response(js, status=404, mimetype='application/json')

def missing_parameters():
    js = json.dumps({'error': 'Parameters missing!'})
    return Response(js, status=422, mimetype='application/json')

def already_exists(s):
    js = json.dumps({'error': str(s) + ' already exist!'})
    return Response(js, status=409, mimetype='application/json')

def success_insert(s):
    js = json.dumps({'success': str(s) + ' inserted!'})
    resp = Response(js, status=201, mimetype='application/json')
    resp.headers['Location'] = url_for(request.path[1:]) + '/' + s
    return resp

def success_update(s):
    return json.jsonify({'success': str(s) + ' updated!'})

def success_remove(s):
    return json.jsonify({'success': str(s) + ' removed!'})
