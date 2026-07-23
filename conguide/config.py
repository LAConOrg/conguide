#!/usr/bin/env python

# Copyright (c) 2014-2017, Paul Selkirk
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted, provided that the
# above copyright notice and this permission notice appear in all
# copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
# AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
# DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
# PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

""" Global variables and config file parsing. """

# default config file
CFG = 'conguide.cfg'

# default output dir
OUTDIR = '.'
# TODO: If there is exactly one .cfg file in the working directory, use
# that by default.

# global variables
debug = False
quiet = False
cfgfile = CFG

# bios.py variables
boldnames = {}

# Boilerplate xhtml file header, with 4 %s bits:
# - title, for <head>
# - extra styles (only used in grid.py)
# - title again, for <body>
# - timestamp of the input csv file
html_header = \
'<?xml version="1.0" encoding="UTF-8"?>\n\
<!DOCTYPE html\n\
     PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"\n\
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n\
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n\
<head>\n\
<title>%s</title>\n\
<meta http-equiv="content-type" content="text/html;charset=utf-8" />\n\
<style type="text/css">\n\
div.center {text-align:center}\n\
%s\
</style>\n\
</head>\n\
<body>\n\
<div class="center">\n\
<h1>%s</h1>\n\
<p>Generated: %s</p>\n\
</div>\n'
source_date = ''

import configparser

cfg: configparser.ConfigParser | None = None

def readConfig(fn) -> configparser.ConfigParser:
    global cfg
    if not cfg:
        cfg = configparser.ConfigParser(allow_no_value=True, strict=False,
                                        inline_comment_prefixes=('#',))
        cfg.optionxform = lambda optionstr: optionstr
        with open(fn, 'r', encoding='utf-8') as f:
            cfg.read_file(f)
    return cfg

def get(section, option, default = None):
    cfg = readConfig(cfgfile)
    try:
        return cfg.get(section, option)
    except configparser.NoSectionError as e:
        if default:
            return default
        raise NoSectionError(e)
    except configparser.NoOptionError as e:
        if default:
            return default
        raise NoOptionError(e)

def getboolean(section, option):
    cfg = readConfig(cfgfile)
    try:
        return cfg.getboolean(section, option)
    except configparser.NoSectionError as e:
        raise NoSectionError(e)
    except configparser.NoOptionError as e:
        raise NoOptionError(e)

def getfloat(section, option):
    cfg = readConfig(cfgfile)
    try:
        return cfg.getfloat(section, option)
    except configparser.NoSectionError as e:
        raise NoSectionError(e)
    except configparser.NoOptionError as e:
        raise NoOptionError(e)

def items(section):
    cfg = readConfig(cfgfile)
    try:
        return cfg.items(section)
    except configparser.NoSectionError as e:
        raise NoSectionError(e)

def itemdict(section):
    cfg = readConfig(cfgfile)
    try:
        dd = {}
        for key, value in cfg.items(section):
            dd[key] = value
        return dd
    except configparser.NoSectionError as e:
        raise NoSectionError(e)

def sections():
    cfg = readConfig(cfgfile)
    return cfg.sections()

def set(section, option, value):
    cfg = readConfig(cfgfile)
    try:
        cfg.set(section, option, value)
    except configparser.NoSectionError as e:
        raise NoSectionError(e)

# # exception classes, so callers don't have to know about configparser
class NoSectionError(configparser.NoSectionError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NoOptionError(configparser.NoOptionError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

