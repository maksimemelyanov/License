from pyramid.security import Allow
from pyramid.security import Everyone
from pyramid.security import Authenticated

class HelloFactory(object):
    def __init__(self, request):
        self.__acl__ = [
            (Allow, Authenticated, 'view')]


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    #config.add_route('company', '/')
    config.add_route('company', '/companies')
    config.add_route('compadd', '/add', factory=HelloFactory)
    config.add_route('parse', '/xlsparse', factory=HelloFactory)
    config.add_route('adding', '/addlicense', factory=HelloFactory)
    config.add_route('deleting', '/delete')
    config.add_route('login', '/login')
    config.add_route('logged', '/logged')
    config.add_route('logouted', '/logout')