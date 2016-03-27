# adsap-syncer

backend for getting sms configs and logging message for a few gps tracker units.

1. refer to `runsync.py --help` for more info
2. put db variables and admin key in `config.py`
3. run `runsync.py`

use `repop.py` to import some sample users and devices.

## current endpoints

endpoint | usage
---------|------
*/login* | *POST* to get config
*/message* | *POST* log messages
*/users* | *GET* all, *POST* new
*/users/:id* | *GET* one, *PUT* to update, *DELETE* one
*/devices* | *GET* all, *POST* new
*/devices/:id* | *GET* one, *PUT* to update, *DELETE* one

## attributions

- http://flask.pocoo.org/docs/0.10/
- http://blog.miguelgrinberg.com/post/flask-migrate-alembic-database-migration-wrapper-for-flask
- http://garage.pimentech.net/libcommonPython_src_python_libcommon_javastringhashcode/
