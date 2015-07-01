#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (c) 2015 Apiary
#  License: MIT
#

try:
    # installed
    from dredd import *
except ImportError:
    # from dev/source
    import os, sys
    this_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(os.path.join(this_dir, './'))
    from dredd import *

__version__ = '0.0.1'


