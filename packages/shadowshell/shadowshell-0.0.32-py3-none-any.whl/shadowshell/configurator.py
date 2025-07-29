#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configurator
@author: shadow walker
"""

import configparser

from shadowshell import LoggerFactory

class Configurator:

    config = None;

    def __init__(self, config_file):

        self.logger = LoggerFactory().get_logger()

        # 加载配置文件
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.logger.debug("load and read config file : %s." % (config_file))
        
    def get(self, group, key):
        value = self.config.get(group, key)
        self.logger.debug("group -> %s, key -> %s, value -> %s" % (group, key, value))
        return value

        
