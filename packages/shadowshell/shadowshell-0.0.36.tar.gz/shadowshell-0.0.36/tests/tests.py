#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tests

@author: shadow shell
"""

from shadowshell import *

class Test(TestTemplate):
    
    def test0(self):
        LoggerFactory().get_logger().info("Run test0")
        return

def hello_world(content):
    LoggerFactory().get_logger().info(f"Hello {content}")

Test().test()
ShadowShell().hello()
# hello()
# shadowshell()

testserver()

# invoke_with_tmpl(hello_world, "World")