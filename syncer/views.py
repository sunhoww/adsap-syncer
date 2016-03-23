from syncer import app, controllers, models, helpers
from flask import request, json
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

@app.route('/insert/<what>', methods=['POST'])
def insert(what):
    try:
        p = request.get_json()
    except BadRequest:
        return 'Error: I\'m sorry, Dave. I\'m afraid I can\'t do that.'
    if not controllers.authenticate(p):
        return json.jsonify({'error': 'Unauthorized access.'})
    if what == 'user':
        return json.jsonify(controllers.user(p))
    elif what == 'device':
        return json.jsonify(controllers.device(p))
    elif what == 'relation':
        return json.jsonify(controllers.relation(p))
    else:
        return json.jsonify({'error': 'Unrecognized action.'})

@app.route('/list/<what>', methods=['POST'])
def list(what):
    try:
        p = request.get_json()
    except BadRequest:
        return 'Error: I\'m sorry, Dave. I\'m afraid I can\'t do that.'
    if not controllers.authenticate(p):
        return json.jsonify({'error': 'Unauthorized access.'})
    if what == 'users':
        return json.jsonify(controllers.list_users(p))
    elif what == 'devices':
        return json.jsonify(controllers.list_devices(p))
    elif what == 'messages':
        return json.jsonify(controllers.list_messages(p))
    else:
        return json.jsonify({'error': 'Unrecognized action.'})

@app.route('/', methods=['POST', 'GET'])
def index():
    return 'v1.0 20160311\n' + helpers.stamp()

@app.route('/test', methods=['POST'])
def test():
    j = json.loads(request.form.get('request'))['nameValuePairs']
    print type(j)
    print j
    return j
