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


@app.route("/employees", methods=("GET",))
@quorum.ensure("foundation.employee.list")
def list_employees():
    return flask.render_template("employee/list.html.tpl", link="employees")


@app.route("/employees.json", methods=("GET",), json=True)
@quorum.ensure("foundation.employee.list")
def list_employees_json():
    api = util.get_api()
    object = quorum.get_object()
    return api.list_employees(**object)


@app.route("/employees/self", methods=("GET",))
@quorum.ensure("foundation.employee.show.self")
def show_employee():
    api = util.get_api()
    employee = api.self_employee()
    return flask.render_template(
        "employee/show.html.tpl",
        link="employees",
        sub_link="info",
        is_self=True,
        employee=employee,
    )


@app.route("/employees/self/sales", methods=("GET",))
@quorum.ensure(("sales.sale_transaction.list.self", "sales.customer_return.list.self"))
def sales_employee():
    year = quorum.get_field("year", None, cast=int)
    month = quorum.get_field("month", None, cast=int)

    api = util.get_api()
    employee = api.self_employee()

    (
        operations,
        target,
        sales_total,
        sales,
        returns,
        previous_month,
        previous_year,
        next_month,
        next_year,
        has_next,
    ) = util.get_sales(year=year, month=month)

    return flask.render_template(
        "employee/sales.html.tpl",
        link="employees",
        sub_link="sales",
        is_self=True,
        employee=employee,
        operations=operations,
        commission_rate=util.COMMISSION_RATE,
        title=target,
        sales_total=sales_total,
        sales_count=len(sales),
        returns_count=len(returns),
        previous=(previous_month, previous_year),
        next=(next_month, next_year),
        has_next=has_next,
    )


@app.route("/employees/self/mail", methods=("GET",))
@quorum.ensure("foundation.employee.show.self")
def mail_employee():
    year = quorum.get_field("year", None, cast=int)
    month = quorum.get_field("month", None, cast=int)

    util.mail_activity(year=year, month=month)

    return show_employee()


@app.route("/employees/<int:id>", methods=("GET",))
@quorum.ensure("foundation.employee.show")
def show_employees(id):
    api = util.get_api()
    employee = api.get_employee(id)
    return flask.render_template(
        "employee/show.html.tpl", link="employees", sub_link="info", employee=employee
    )


@app.route("/employees/<int:id>/sales", methods=("GET",))
@quorum.ensure(("sales.sale_transaction.list", "sales.customer_return.list"))
def sales_employees(id):
    year = quorum.get_field("year", None, cast=int)
    month = quorum.get_field("month", None, cast=int)

    api = util.get_api()
    employee = api.get_employee(id)

    (
        operations,
        target_s,
        sales_total,
        sales_s,
        returns_s,
        previous_month,
        previous_year,
        next_month,
        next_year,
        has_next,
    ) = util.get_sales(id=id, year=year, month=month)

    return flask.render_template(
        "employee/sales.html.tpl",
        link="employees",
        sub_link="sales",
        is_self=False,
        employee=employee,
        operations=operations,
        commission_rate=util.COMMISSION_RATE,
        title=target_s,
        sales_total=sales_total,
        sales_count=len(sales_s),
        returns_count=len(returns_s),
        previous=(previous_month, previous_year),
        next=(next_month, next_year),
        has_next=has_next,
    )


@app.route("/employees/<int:id>/mail", methods=("GET",))
@quorum.ensure("foundation.employee.show")
def mail_employees(id):
    year = quorum.get_field("year", None, cast=int)
    month = quorum.get_field("month", None, cast=int)

    util.mail_activity(id=id, year=year, month=month)

    return show_employees(id)
