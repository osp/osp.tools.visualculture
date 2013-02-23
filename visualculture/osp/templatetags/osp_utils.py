#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

from django import template

register = template.Library()

def formatsize(size):
    """
    Take a filesize in bytes and output a more readable string
    Adapted from: http://stackoverflow.com/a/14822210/319860
    """
    size = int(size)
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size,1024)))
    p = math.pow(1024,i)
    s = round(size/p,2)
    if (s > 0):
        return '%s %s' % (s,size_name[i])
    return '0 B'

register.filter('formatsize', formatsize)
