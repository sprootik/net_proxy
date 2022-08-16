#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import configparser
import logging.handlers
from flask import Flask, request, jsonify, make_response
from gevent.pywsgi import WSGIServer
from gevent import monkey
from flask_basicauth import BasicAuth
from flask_expects_json import expects_json
from jsonschema import ValidationError
from netmiko import ConnectHandler
# modules
from net_proxy_modules import json_schema

file_dir = os.path.dirname(os.path.abspath(__file__))

settings = configparser.ConfigParser()
settings.read(file_dir + '/cfg/settings.cfg')
# for asynchronous
monkey.patch_all()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
# logs
FORMAT = "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
logger = logging.getLogger('http_net_proxy')
if settings.getboolean("logs", "debug") is False:
    log_level = logging.INFO
else:
    log_level = logging.DEBUG
logging.basicConfig(format=FORMAT, filename=file_dir + '/logs/net_proxy.log',
                    level=log_level)
handler = logging.handlers.RotatingFileHandler(
    file_dir + '/logs/net_proxy.log',
    maxBytes=50 * 1024,
    backupCount=3)

# auth
app.config['BASIC_AUTH_USERNAME'] = settings.get("net-proxy", "username")
app.config['BASIC_AUTH_PASSWORD'] = settings.get("net-proxy", "password")
basic_auth = BasicAuth(app)
app.config['BASIC_AUTH_FORCE'] = True


@app.route('/net_send', methods=['POST'])
@expects_json(json_schema.schema_net)
def net_send():
    data = request.get_json(force=True)
    host = data['host']
    port = data['port']
    username = data['username']
    password = data['password']
    device_type = data['devtype']
    commands = data['commmands']
    net_parameters = {
        'device_type': device_type,
        'ip': host,
        'username': username,
        'password': password,
        'port': port,
        'auth_timeout': 3,
        'timeout': 5,
    }
    try:
        connection = ConnectHandler(**net_parameters)
        output = []
        for line in commands:
            out = connection.send_command(line)
            output.append(out)
    except Exception as e:
        return jsonify({'error': str(e)}), 200
    else:
        return jsonify(result=output), 200
    finally:
        if 'connection' in locals():
            connection.disconnect()


@app.route('/net_change', methods=['POST'])
@expects_json(json_schema.schema_net)
def net_change():
    data = request.get_json(force=True)
    host = data['host']
    port = data['port']
    username = data['username']
    password = data['password']
    device_type = data['devtype']
    commands = data['commmands']
    net_parameters = {
        'device_type': device_type,
        'ip': host,
        'username': username,
        'password': password,
        'port': port,
        'auth_timeout': 3,
        'timeout': 5,
    }
    try:
        connection = ConnectHandler(**net_parameters)
        output = connection.send_config_set(commands)
    except Exception as e:
        return jsonify({'error': str(e)}), 200
    else:
        return jsonify(result=output), 200
    finally:
        if 'connection' in locals():
            connection.disconnect()


@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({'error': original_error.message}), 200)
    # handle other "Bad Request"-errors
    return error


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=4445)  # Flask for dev
    http_proxy = WSGIServer((settings.get(
        "net-proxy", "ip"), int(settings.get("net-proxy", "port"))), app, log=logger)
    try:
        logging.warning('the server is running')
        http_proxy.serve_forever()
    except KeyboardInterrupt:
        logging.warning('server stopped')
        http_proxy.stop()
