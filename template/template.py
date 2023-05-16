#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/12 10:58
# @Author  : llybood

import shutil
from os import path

from utils.utils import utc_to_local
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import BytecodeCache


class TemplateCache(BytecodeCache):

    def __init__(self, directory):
        self.directory = directory

    def load_bytecode(self, bucket):
        filename = path.join(self.directory, bucket.key)
        if path.exists(filename):
            with open(filename, 'rb') as f:
                bucket.load_bytecode(f)

    def dump_bytecode(self, bucket):
        filename = path.join(self.directory, bucket.key)
        with open(filename, 'wb') as f:
            bucket.write_bytecode(f)

    def clear(self):
        shutil.rmtree(self.directory)


class MessageTemplate():


    def __init__(self, directory):
        file_loader = FileSystemLoader(directory)
        self.env = Environment(loader=file_loader, bytecode_cache=TemplateCache('/tmp'))
        self.env.filters["utc_to_local"] = utc_to_local

    def get_template(self):
        template = self.env.get_template("template.tmpl")
        return template
