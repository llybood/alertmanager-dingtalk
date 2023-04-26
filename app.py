#!/usr/local/python381/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/11/1 10:58
# @Author  : llybood

import asyncio
import uvloop

from config.Config import Config
from utils.logger import logger
from sanic import Sanic, response, json

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


app = Sanic(__name__)

sem = None

@app.listener('before_server_start')
def init(sanic, loop):
    global sem
    concurrency_per_worker = 4
    sem = asyncio.Semaphore(concurrency_per_worker)

@app.route("/dingtalk", methods=["GET"])
async def index(request):
    return response.text(Config.get_instance().get("global.notification.channel"))

if __name__ == '__main__': 
    logger.info("Server initlized, listenning on 0.0.0.0:8111")
    app.run(host="0.0.0.0", port=8111, workers=2, debug=False, access_log=True)
