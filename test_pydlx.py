"""Test file for the dlx package"""
import doctest
import pydlx.operations
import pydlx.link

MODULES = (pydlx.operations, pydlx.link)
for mod in MODULES:
    doctest.testmod(mod)
