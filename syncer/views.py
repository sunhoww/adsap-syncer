from syncer import app, controllers, models
from flask import request, json

@app.route('/login', methods=['POST'])
def login():
    try:
        p = request.get_json()
        if not controllers.is_correct_login_format(p):
            return json.jsonify({'error': 'Incorrect format.'})
        if not controllers.is_user(p):
            return json.jsonify({'error': 'Unauthorized access.'})
        return json.jsonify(controllers.get_conf(p))
    except:
        return 'Error: Resistance is futile.'

@app.route('/message', methods=['POST'])
def message():
    try:
        p = request.get_json()
        if not controllers.is_correct_login_format(p):
            return json.jsonify({'error': 'Incorrect format.'})
        if not controllers.is_user(p):
            return json.jsonify({'error': 'Unauthorized access.'})
        return json.jsonify(controllers.add_record(p))
    except:
        return 'Error: Resistance is futile.'

@app.route('/insert/<action>', methods=['POST'])
def insert(action):
    try:
        p = request.get_json()
        if not controllers.authenticate(p):
            return json.jsonify({'error': 'Unauthorized access.'})
        if action == 'user':
            return json.jsonify(controllers.user(p))
        elif action == 'device':
            return json.jsonify(controllers.device(p))
        elif action == 'relation':
            return json.jsonify(controllers.relation(p))
        else:
            return json.jsonify({'error': 'Unrecognized action.'})
    except:
        return 'Error: I\'m sorry, Dave. I\'m afraid I can\'t do that.'

@app.route('/', methods=['POST', 'GET'])
def index():
    return 'v1.0 20160311'
