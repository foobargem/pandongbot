#-*- coding:utf-8 -*-
import base64
import hashlib
import hmac
import requests
import json
import logging
from django.utils import timezone

LOG = logging.getLogger("pandongbot")


class PandongBot():

    def __init__(self, conf={}):
        self.access_token = conf['access_token']
        self.channel_secret = conf['channel_secret']

    def validate_signature(self, request):
        hash = hmac.new(self.channel_secret.encode('utf-8'),
                        str(request.body),
                        hashlib.sha256).digest()
        signature = base64.b64encode(hash)
        return signature == request.META.get('HTTP_X_LINE_SIGNATURE')

    def reply_message(self, reply_token, messages):
        url = "https://api.line.me/v2/bot/message/reply"
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer %s" % self.access_token,
        }
        data = {
            'replyToken': reply_token,
            'messages': messages,
        }
        res = requests.post(url=url, headers=headers, data=json.dumps(data))
        return res

    def help_message(self):
        usage = '''사용법: @팬동봇 명령
명령어:
  * 큐티 {청소년|고학년|저학년|어린이} - 오늘의 매일성경 링크를 알려줍니다. 기본은 장년 매일성경입니다.
'''
        return {
            'type': "text",
            'text': usage,
        }

    def qt_message(self, type=None):
        base_url = "http://www.su.or.kr/03bible/daily/qtView.do"
        if type == "청소년":
            qt_type = "QT2"
        elif type == "고학년":
            base_url = "http://www.su.or.kr/03bible/daily/qt3View.do"
            qt_type = "QT3"
        elif type == "저학년":
            base_url = "http://www.su.or.kr/03bible/daily/qt3View.do"
            qt_type = "QT4"
        elif type == "어린이":
            base_url = "http://www.su.or.kr/03bible/daily/qt3View.do"
            qt_type = "QT7"
        else:
            qt_type = "QT1"

        now = timezone.localtime(timezone.now())
        qt_link = "{base_url}?qtType={qt_type}&year={year}&month={month}&day={day}".format(
                      base_url=base_url, qt_type=qt_type,
                      year=now.year, month=now.month, day=now.day)
        LOG.debug(qt_link)

        return {
            'type': "text",
            'text': "%s" % qt_link,
        }
