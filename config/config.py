#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/18 下午3:25
# @Author  : lovemefan
# @File    : config.py

import os
import logging
import yaml


class Config:
    """upgrade the config automatically while the config.ini file changed
    Example Config.get_instance().get(key, default)
    """

    def __init__(self):
        """initialize attributions of config class"""
        logging.debug("init config ...")
        self.global_config_file_path =  os.path.join(os.path.dirname(__file__), "config.yaml")
        self.logging_config_file_path = os.path.join(os.path.dirname(__file__), "logging.yaml")

    def load_global_config(self):
        """load the global config file"""
        logging.info("loading global the config ...")
        with open(file=self.global_config_file_path, mode="r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return config

    def load_logging_config(self):
        """load the logging config file"""
        logging.info("loading the logging config ...")
        with open(file=self.logging_config_file_path, mode="r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return config

