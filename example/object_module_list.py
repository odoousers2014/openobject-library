#!/usr/bin/env python
# --*- coding: utf-8 -*-
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

"""
This script enable a connection on the OpenERP Server and return the list of
module whom are installed.
"""

import sys
sys.path.append('../')

from oobjlib.connection import Connection
from oobjlib.component import Object
from oobjlib.common import GetParser

parser = GetParser('Module List', '0.1')
opts, args = parser.parse_args()

try:
    cnx = Connection(
        server=opts.server, 
        dbname=opts.dbname, 
        login=opts.user, 
        password=opts.passwd, 
        port=opts.port)
except Exception, e:
    print '%s' % str(e)
    exit(1)

modules = Object(cnx, "ir.module.module")
print '--[Connection Object]---------------------'
print '%s' % str(modules)

ids = modules.search([('state', '=', 'installed')])
print '--[Module list]---------------------------'
for p in modules.read(ids, ['name']):
    print '* %s' % p['name']

print '--[End]-----------------------------------'
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
