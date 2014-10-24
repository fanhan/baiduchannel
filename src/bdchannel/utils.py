#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests


class EnumDict(dict):

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError, k:
            raise AttributeError, k

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError, k


class ChannelException(Exception):

    def __init__(self, code, msg):
        self.error_code = code
        self.error_msg = msg
        self.error = msg

    def __str__(self):
        return "%s: %s" % (self.error_code, self.error_msg)


def get_access_token(api_key, api_secret):
    """
    Get access token
    """
    url = 'https://openapi.baidu.com/oauth/2.0/token'
    r = requests.post(url, data={
        'grant_type': 'client_credentials',
        'client_id': api_key,
        'client_secret': api_secret,
    })
    return EnumDict(json.loads(r.text))


