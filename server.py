#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/12 14:50
# @Author  : llybood

import yaml
import logging
import os

from sanic.log import logger
from sanic import Sanic, response

from config.config import Config
from alertmanager.alertmanager import AlertManagerMessage
from dingtalk.dingtalk import Dingtalk


if not os.path.exists("logs"):
    os.makedirs("logs")

app = Sanic("alertmanager-dingtalk", log_config=Config().load_logging_config())
app.config.update(Config().load_global_config())

alert_log = logging.getLogger("custom.alert")

@app.route("/media/list", methods=["GET"])
async def get_media(request):
    return response.json(app.config.media)

@app.route("/rules/list", methods=["GET"])
async def get_rules(request):
    return response.json(app.config.rules)

# Get the channel configuration of a media
@app.route("/media/<media:str>/list", methods=["GET"])
async def get_channel(request, media):
    return response.json(app.config.media.get(media))

# Send dingtalk alarm
@app.route("/media/dingtalk/<channel:str>/send", methods=["POST"])
async def send_dingtalk_alert(request, channel):
    alerts = request.json
    alertname = alerts.get("alerts")[0].get("labels").get("alertname")
    alertnum = len(alerts.get("alerts"))
    escalation_rule = request.args.get('escalation')
    alerts_escalation_rule = None
    alertmanager = AlertManagerMessage(alerts)
    if escalation_rule is not None:
        rule = app.config.rules.get("escalation").get(escalation_rule)
        alerts_escalation_rule = alertmanager.get_alerts_escalation_rule(rule)
    if alerts_escalation_rule:
        channel = rule.get(alerts_escalation_rule).get("channel")
        alerts["escalation"] = escalation_rule
    msg = alertmanager.format_alerts_to_markdown()
    url = app.config.media.get("dingtalk").get("channels").get(channel).get("url")
    secret  = app.config.media.get("dingtalk").get("channels").get(channel).get("secret")
    at_mobiles = app.config.media.get("dingtalk").get("channels").get(channel).get("at_mobiles")
    is_at_all = app.config.media.get("dingtalk").get("channels").get(channel).get("is_at_all")
    result = Dingtalk(url=url, secret=secret, at_mobiles=at_mobiles, is_at_all=is_at_all, msg=msg).send()
    alert_log.info(f'{request.ip} {request.method} {request.url} {alertname} {alertnum} dingtalk {escalation_rule} {alerts_escalation_rule} {channel} {result}')
    return response.json(result)

if __name__ == "__main__": 
    host = app.config.server.get("listen")
    port = app.config.server.get("port")
    workers = app.config.server.get("workers")
    access_log = app.config.server.get("access_log")
    logger.info(f"alertmanager-dingtalk is start on {host}:{port}")
    app.run(host=host, port=port, workers=workers, access_log=access_log)
