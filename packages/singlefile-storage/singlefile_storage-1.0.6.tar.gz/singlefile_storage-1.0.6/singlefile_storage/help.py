#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: qicongsheng
def get_name():
    return 'singlefile-storage'


def get_version():
    return '1.0.6'


def get_source_url():
    return 'https://github.com/qicongsheng/%s' % get_name()


def print_version():
    print('%s %s\r\nMt5 http proxy for python.' % (get_name(), get_version()))
