from syncer import app, controllers, helpers
from flask import request, json, Response, render_template
from functools import wraps
from werkzeug.exceptions import BadRequest
from config import app_logfile
from time import asctime

@app.before_request
def before_request():
    f = open(app_logfile, 'a')
    line = """
        <div>
            <h3 style=\"background-color:lightgreen; padding:5px;\">
                """ + asctime() + ' ' + """<span style=\"font-size:.8em; font-weight:normal;\">""" + request.method + ' ' + request.path + ' ' + request.remote_addr + """</span>
            </h3>
            <pre style=\"background-color:lightgray; margin:20px; padding:5px;\">""" + str(request.headers) + """</pre>
            <pre style=\"background-color:lightgray; margin:20px; padding:5px;\">""" + request.data + """</pre>
        </div>"""
    f.write(line)
    f.close()

@app.after_request
def after_request(r):
    f = open(app_logfile, 'a')
    line = """
        <div>
            <h3 style=\"background-color:lightblue; padding:5px;\">
                """ + asctime() + ' ' + """<span style=\"font-size:.8em; font-weight:normal;\">""" + str(r.status_code) + """</span>
            </h3>
            <pre style=\"background-color:lightgray; margin:20px; padding:5px;\">""" + str(r.headers) + """</pre>
            <pre style=\"background-color:lightgray; margin:20px; padding:5px;\">""" + r.data + """</pre>
        </div>"""
    f.write(line)
    f.close()
    return r

@app.route('/login', methods=['POST'])
def login():
    try:
        p = request.get_json(force=True)
    except BadRequest:
        return helpers.bad_request()
    if not controllers.is_correct_login_format(p):
        return helpers.incorrect_format()
    if not controllers.is_user(p):
        return helpers.unauthorized()
    return json.jsonify(controllers.get_conf(p))

@app.route('/message', methods=['POST'])
def message():
    try:
        p = request.get_json()
    except BadRequest:
        return helpers.bad_request()
    if not controllers.is_correct_login_format(p):
        return helpers.incorrect_format()
    if not controllers.is_user(p):
        return helpers.unauthorized()
    return json.jsonify(controllers.add_record(p))

@app.route('/', methods=['POST', 'GET'])
def index():
    return 'v1.0 20160311\n' + helpers.stamp()

@app.route('/test', methods=['POST'])
def test():
    j = json.loads(request.form.get('request'))['nameValuePairs']
    print type(j)
    print j
    return j

# admin

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    js = json.dumps({'error': 'Do or do not. There is no try. Yes.'})
    resp = Response(js, status=401, mimetype='application/json')
    resp.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/users', methods=['GET', 'POST'])
@app.route('/users/<uid>', methods=['GET', 'PUT', 'DELETE'])
@requires_auth
def users(uid=None):
    if request.method == 'GET':
        return controllers.list_items(uid)
    if request.method == 'POST':
        return controllers.insert_item()
    if request.method == 'PUT':
        return controllers.update_item(uid)
    if request.method == 'DELETE':
        return controllers.remove_item(uid)

@app.route('/devices', methods=['GET', 'POST'])
@app.route('/devices/<did>', methods=['GET', 'PUT', 'DELETE'])
@requires_auth
def devices(did=None):
    if request.method == 'GET':
        return controllers.list_items(did)
    if request.method == 'POST':
        return controllers.insert_item()
    if request.method == 'PUT':
        return controllers.update_item(did)
    if request.method == 'DELETE':
        return controllers.remove_item(did)
