#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/12 15:08
# @Author  : llybood

import os
import logging
import yaml


sanic_log = logging.getLogger("sanic.root")

class Config:
    """Load global configuration files and log configuration files"""

    def __init__(self):
        self.global_config_file_path =  os.path.join(os.path.dirname(__file__), "config.yaml")
        self.logging_config_file_path = os.path.join(os.path.dirname(__file__), "logging.yaml")

    def load_global_config(self):
        sanic_log.info(f"loading global config {self.global_config_file_path}")
        with open(file=self.global_config_file_path, mode="r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return config

    def load_logging_config(self):
        sanic_log.info(f"loading logging config {self.logging_config_file_path}")
        with open(file=self.logging_config_file_path, mode="r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return config
