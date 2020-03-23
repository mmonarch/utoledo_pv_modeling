#!/usr/bin/python3
#
# pv_exceptions.py

class PVConfigError(Exception):
    pass

class PVIllegalArgumentError(ValueError):
    pass

class PVIOError(IOError):
    pass
