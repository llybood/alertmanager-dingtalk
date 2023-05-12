#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/12 13:58
# @Author  : llybood

from dingtalkchatbot.chatbot import DingtalkChatbot


class Dingtalk: 

    def __init__(
        self, 
        url=None,
        secret=None,
        at_mobiles=None,
        is_at_all=None,
        msg=None,
        ):

        self.url = url
        self.secret = secret
        self.at_mobiles = at_mobiles
        self.is_at_all = is_at_all
        self.msg = msg

    def send(self):
       if self.secret:
           xiaoding = DingtalkChatbot(self.url, secret=self.secret)
       else:
           xiaoding = DingtalkChatbot(self.url)
       if self.is_at_all:
           return xiaoding.send_markdown(title="dingtalk-alert", text=self.msg, is_at_all=True)
       elif self.at_mobiles:
           return xiaoding.send_markdown(title="dingtalk-alert", text=self.msg, at_mobiles=self.at_mobiles)
       else:
           return xiaoding.send_markdown(title="dingtalk-alert", text=self.msg)
