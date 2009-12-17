# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenObject Library
#    Copyright (C) 2009 Tiny (<http://tiny.be>). Christophe Simonis 
#                  All Rights Reserved
#    Copyright (C) 2009 Syleam (<http://syleam.fr>). Christophe Chauvet 
#                  All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import xmlrpclib
from socket import error as socket_error

# TODO abastract the use of the context

class Object(object):
    def __init__(self, connection, model):
        self._connection = connection
        self._model = model
        self._url = "http://%s:%d/xmlrpc/object" % (connection.server, connection.port)
        self._sock = xmlrpclib.ServerProxy(self._url)

    def __getattr__(self, name):
        def proxy(*args, **kwargs):
            try:
                return self._sock.execute(self._connection.dbname, self._connection.userid, self._connection.password, self._model, name, *args, **kwargs)
            except socket_error, se:
                raise Exception('Unable to connect to http://%s:%d: %s' % (server, port, se.args[1]))
            except xmlrpclib.Fault, err:
                raise Exception('%s: %s' % (err.faultCode.encode('utf-8'), err.faultString.encode('utf-8')))
        return proxy

    def select(self, domain = None, fields=None):
        ids = self.search(domain or [])
        return self.read(ids, fields or [])

    def __str__(self,):
        return '%s [%s]' % (self._url, self._model)

class Wizard(object):
    def __init__(self, connection, name):
        self._connection = connection
        self._name = name
        self._sock = xmlrpclib.ServerProxy("http://%s:%d/xmlrpc/wizard" % (connection.server, connection.port))
        self._id = self._sock.create(self._connection.dbname, self._connection.userid, self._connection.password, self._name)

    def __getattr__(self, state):
        def proxy(**kwargs):
            return self._sock.execute(self._connection.dbname, self._connection.userid, self._connection.password, self._id, kwargs, state)
        return proxy

def demo():
    db = Database()
    print repr(db.list())

    cnx = Connection(dbname="demo", login="admin", password="admin")
    modules = Object(cnx, "ir.module.module")

    ids = modules.search([('state', '=', 'installed')])
    for p in modules.read(ids, ['name']):
        print p['name']

if __name__ == '__main__':
    demo()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: