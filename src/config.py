import os

__author__ = "jc"

DEBUG = False
ADMINS = frozenset([
    os.environ.get('ADMIN_EMAIL')
])
