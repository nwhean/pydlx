"""Test file for the dlx package"""
import doctest
import dlx.operations
import dlx.link

MODULES = (dlx.operations, dlx.link)
for mod in MODULES:
    doctest.testmod(dlx.operations)
