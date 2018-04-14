# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import logging
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .bots import PandongBot

LOG = logging.getLogger('pandongbot')


def index(request):
    return HttpResponse(__name__)


@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        bot = PandongBot(settings.LINEBOT['pandongbot'])
        if not (bot.validate_signature(request)):
            LOG.error("invalid signature")
            return HttpResponse("invalid signature", status=406)

        data = json.loads(request.body)
        for event in data['events']:
            if event['message']['type'] == "text":
                msg_text = event['message']['text']

            if msg_text.startswith("@팬동봇"):
                msg_tokens = msg_text.split()

            reply_messages = []
            try:
                cmd = msg_tokens[1]
            except IndexError as e:
                cmd = "help"

            try:
                cmd_arg = msg_tokens[2]
            except IndexError as e:
                cmd_arg = None

            LOG.debug("cmd: %s %s" % (cmd, cmd_arg, ))

            if cmd.lower() == "큐티":
                reply_messages.append(bot.qt_message(type=cmd_arg))
            else:
                reply_messages.append(bot.help_message())

            result = bot.reply_message(event['replyToken'], reply_messages)
            LOG.debug("invoke reply api: %s" % result.__dict__)

    return HttpResponse("OK")
