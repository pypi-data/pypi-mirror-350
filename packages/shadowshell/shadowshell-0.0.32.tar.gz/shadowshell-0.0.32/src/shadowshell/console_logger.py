#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ConsoleLogger

author: shadow shell
"""

from shadowshell.logger import Logger

class ConsoleLogger(Logger):

    def debug(self, content):
        self.__log(content)
        
    def info(self, content):
        self.__log(content)

    def warn(self, content):
        self.__log(content)
    
    def error(self, content):
        self.__log(content)

    def __log(self, content):
        print("%s" % (content))
