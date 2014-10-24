#!/usr/bin/env python
# -*- coding: utf-8 -*-

import md5
import time
try:
    import json
except:
    import simplejson as json
import uuid
import requests
import operator

from utils import EnumDict, ChannelException, get_access_token

CHANNEL_URL = 'https://channel.api.duapp.com/rest/2.0/channel/%s'

PUSH_TYPE = EnumDict()
PUSH_TYPE.USER = 1
PUSH_TYPE.TAG = 2
PUSH_TYPE.ALL = 3


class Channel(object):
    """
    Channel
    ======
    需要两个参数: api_key、 api_secret
    """
    access_token = None
    expires = time.time()

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def refresh_access_token(self):
        access_token = get_access_token(self.api_key, self.api_secret)
        self.expires = access_token.expires_in + time.time()
        self.access_token = access_token.access_token

    def _request(self, channel_id='channel', params={}):
        if time.time() + 3600 > self.expires:
            self.refresh_access_token()
        url = CHANNEL_URL % channel_id

        params.update({
            'access_token': self.access_token,
        })

        r = requests.post(url, data=params)
        if r.status_code != requests.codes.ok:
            raise ChannelException(r.status_code, r.text)
        return EnumDict(json.loads(r.text))

    def query_bindlist(self, user_id, device_type=0, start=0, limit=10,
                       channel_id='channel'):
        """
        查询设备、应用、用户与百度Channel的绑定关系
        """
        params = {
            'user_id': user_id,
            'start': start,
            'limit': limit,
            'method': 'query_bindlist',
            'device_type': device_type,
        }
        return self._request(params=params)

    def push_msg(self, msgs, user_id=None, tag=None, channel_id=None,
                 device_type=3, message_type=0):
        """
        推送消息
        """
        params = {}

        if tag:
            push_type = PUSH_TYPE.TAG
            params.update(tag=tag)
        elif not tag and user_id:
            push_type = PUSH_TYPE.USER
            params.update(user_id=user_id)
        else:
            push_type = PUSH_TYPE.ALL

        msgs = msgs if isinstance(msgs, (list, tuple)) else [msgs]
        params.update(
            push_type=push_type,
            messages=json.dumps(msgs),
            msg_keys=json.dumps([uuid.uuid4().hex for x in msgs]),
            device_type=device_type,
            message_type=message_type,
            method='push_msg',
        )
        return self._request(channel_id=channel_id, params=params)

    def init_app_ioscert(self, name, description, release_cert, dev_cert):
        """
        上传iOS apns证书
        """
        params = {
            'name': name,
            'description': description,
            'release_cert': release_cert,
            'dev_cert': dev_cert,
            'method': 'init_app_ioscert',
        }
        return self._request(params=params)

    def update_app_ioscert(self, name=None, description=None,
                           release_cert=None, dev_cert=None):
        """
        更新iOS设备的推送证书相关内容
        """
        params = {
            'name': name,
            'description': description,
            'release_cert': release_cert,
            'dev_cert': dev_cert,
            'method': 'update_app_ioscert',
        }
        return self._request(params=params)

    def delete_app_ioscert(self):
        """
        删除iOS设备的推送证书
        """
        return self._request(params={'method': 'delete_app_ioscert'})

    def query_app_ioscert(self):
        """
        查询该App server对应的iOS证书。
        """
        return self._request(params={'method': 'query_app_ioscert'})

    def verify_bind(self, user_id, device_type=None):
        """
        判断设备、应用、用户与Channel的绑定关系是否存在
        """
        params = {
            'method': 'verify_bind',
            'user_id': user_id,
            'device_type': device_type,
        }
        return self._request(params=params)

    def fetch_msg(self, user_id, start=0, limit=10):
        """
        查询离线消息
        """
        params = {
            'method': 'fetch_msg',
            'user_id': user_id,
            'start': start,
            'limit': limit,
        }
        return self._request(params=params)

    def fetch_msgcount(self, user_id):
        """
        查询离线消息的个数
        """
        params = {
            'method': 'fetch_msgcount',
            'user_id':user_id,
        }
        return self._request(params=params)

    def delete_msg(self, user_id, msg_ids):
        """
        删除离线消息
        """
        msg_ids = msg_ids if isinstance(msg_ids, (list, tuple)) else [msg_ids]
        params = {
            'method': 'delete_msg',
            'msg_ids': json.dumps(msg_ids),
            'user_id': user_id,
        }
        return self._request(params=params)


    def set_tag(self, tag, user_id=None):
        """
        服务器端设置用户标签
        """
        params = {
            'method': 'set_tag',
            'user_id': user_id,
            'tag': tag,
        }
        return self._request(params=params)

    def fetch_tag(self, tag=None, start=0, limit=10):
        """
        App Server查询应用标签
        """
        params = {
            'method': 'fetch_tag',
            'tag': tag,
            'start': start,
            'limit': limit,
        }
        return self._request(params=params)

    def delete_tag(self, tag, user_id=None):
        """
        服务端删除用户标签
        """
        params = {
            'method': 'delete_tag',
            'tag': tag,
            'user_id': user_id,
        }
        return self._request(params=params)

    def query_user_tags(self, user_id):
        """
        App Server查询用户所属的标签列表
        """
        params = {
            'method': 'query_user_tags',
            'user_id': user_id,
        }
        return self._request(params=params)

    def query_device_type(self):
        """
        根据channel_id查询设备类型
        """
        params = {
            'method': 'query_device_type',
        }
        return self._request(params=params)


