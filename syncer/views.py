from syncer import app, controllers, models, helpers
from flask import request, json, Response
from functools import wraps
from werkzeug.exceptions import BadRequest

@app.route('/login', methods=['POST'])
def login():
    try:
        p = request.get_json(force=True)
    except BadRequest:
        return 'Error: Don\'t panic!'
    if not controllers.is_correct_login_format(p):
        return json.jsonify({'error': 'Incorrect format.'})
    if not controllers.is_user(p):
        return json.jsonify({'error': 'Unauthorized access.'})
    return json.jsonify(controllers.get_conf(p))

@app.route('/message', methods=['POST'])
def message():
    try:
        p = request.get_json()
    except BadRequest:
        return 'Error: Resistance is futile.'
    if not controllers.is_correct_login_format(p):
        return json.jsonify({'error': 'Incorrect format.'})
    if not controllers.is_user(p):
        return json.jsonify({'error': 'Unauthorized access.'})
    return json.jsonify(controllers.add_record(p))

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    js = json.dumps({'error': 'Do or do not. There is no try.'})
    resp = Response(js, status=401, mimetype='application/json')
    resp.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
    return resp

def badreq():
    """for handling bad requests"""
    js = json.dumps({'error': 'I\'m sorry, Dave. I\'m afraid I can\'t do that.'})
    resp = Response(js, status=400, mimetype='application/json')
    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/list/users', methods=['GET'])
@requires_auth
def list_users():
    return json.jsonify(controllers.list_users())

@app.route('/list/users/<uid>', methods=['GET'])
@requires_auth
def list_user(uid):
    return json.jsonify(controllers.list_user(uid))

@app.route('/list/devices', methods=['GET'])
@requires_auth
def list_devices():
    return json.jsonify(controllers.list_devices())

@app.route('/list/devices/<did>', methods=['GET'])
@requires_auth
def list_device(did):
    return json.jsonify(controllers.list_device(did))

@app.route('/insert/<what>', methods=['POST'])
@requires_auth
def insert(what):
    try:
        p = request.get_json()
    except BadRequest:
        return badreq()
    if what == 'user':
        return json.jsonify(controllers.user(p))
    elif what == 'device':
        return json.jsonify(controllers.device(p))
    elif what == 'relation':
        return json.jsonify(controllers.relation(p))
    else:
        return badreq()

@app.route('/', methods=['POST', 'GET'])
def index():
    return 'v1.0 20160311\n' + helpers.stamp()

@app.route('/test', methods=['POST'])
def test():
    j = json.loads(request.form.get('request'))['nameValuePairs']
    print type(j)
    print j
    return j
