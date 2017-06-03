__author__ = 'jc'


class StoreException(Exception):
    def __init__(self, message):
        self.message = message


class StoreNotFoundException(StoreException):
    pass

