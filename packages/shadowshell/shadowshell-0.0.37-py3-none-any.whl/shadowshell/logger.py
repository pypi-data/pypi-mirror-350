#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Logger

@author: shadow shell
"""

class Logger:

    def debug(self, content):
        self.__log(content)
        
    def info(self, content):
        self.__log(content)

    def warn(self, content):
        self.__log(content)
    
    def error(self, content):
        self.__log(content)

    def __log(self, content):
        print("[LOGGER]%s" % content)
