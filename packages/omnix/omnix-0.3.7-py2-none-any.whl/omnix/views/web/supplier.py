#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Omnix System
# Copyright (c) 2008-2025 Hive Solutions Lda.
#
# This file is part of Hive Omnix System.
#
# Hive Omnix System is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Omnix System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Omnix System. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2025 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

from omnix import util

from omnix.main import app
from omnix.main import flask
from omnix.main import quorum


@app.route("/suppliers", methods=("GET",))
@quorum.ensure("foundation.supplier_company.list")
def list_suppliers():
    return flask.render_template("supplier/list.html.tpl", link="suppliers")


@app.route("/suppliers.json", methods=("GET",), json=True)
@quorum.ensure("foundation.supplier_company.list")
def list_suppliers_json():
    api = util.get_api()
    object = quorum.get_object()
    return api.list_companies(**object)


@app.route("/suppliers/<int:id>", methods=("GET",))
@quorum.ensure("foundation.supplier_company.show")
def show_suppliers(id):
    api = util.get_api()
    supplier = api.get_company(id)
    return flask.render_template(
        "supplier/show.html.tpl", link="suppliers", supplier=supplier
    )
