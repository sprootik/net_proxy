#!/usr/bin/env python3
# -*- coding: utf-8 -*-


schema_net = {
    'type': 'object',
    'properties': {
        'host': {'type': 'string'},
        'port': {'type': 'number'},
        'username': {'type': 'string'},
        'password': {'type': 'string'},
        'devtype': {'type': 'string'},
        'commmands': {'type': 'array'}
    },
    'required': ['host', 'port', 'username', 'password', 'devtype']
}
