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

import datetime

from omnix import util

from omnix.main import app
from omnix.main import flask
from omnix.main import quorum


@app.route("/stores", methods=("GET",))
@quorum.ensure("foundation.store.list")
def list_stores():
    return flask.render_template("store/list.html.tpl", link="stores")


@app.route("/stores.json", methods=("GET",), json=True)
@quorum.ensure("foundation.store.list")
def list_stores_json():
    api = util.get_api()
    object = quorum.get_object()
    return api.list_stores(**object)


@app.route("/stores/<id>", methods=("GET",))
@quorum.ensure("foundation.store.show")
def show_stores(id):
    api = util.get_api()
    id = int(id)
    is_global = id == -1
    store = _global() if is_global else api.get_store(id)
    return flask.render_template(
        "store/show.html.tpl", link="stores", sub_link="info", store=store
    )


@app.route("/stores/<id>/sales", methods=("GET",))
@quorum.ensure(("foundation.store.show", "analytics.sale_snapshot.list"))
def sales_stores(id):
    api = util.get_api()

    id = int(id)
    is_global = id == -1

    now = datetime.datetime.utcnow()
    current_day = datetime.datetime(now.year, now.month, now.day)

    store = _global() if is_global else api.get_store(id)

    contents = api.stats_sales(
        unit="day", store_id=None if is_global else id, has_global=True
    )
    stats = contents[str(id)]
    current = dict(
        net_price_vat=stats["net_price_vat"][-1],
        net_number_sales=stats["net_number_sales"][-1],
        date=current_day,
    )

    days = []

    count = len(stats["net_price_vat"]) - 1
    count_r = range(count)
    count_r = list(count_r)
    count_r.reverse()
    _current_day = current_day
    for index in count_r:
        _current_day -= datetime.timedelta(1)
        day = dict(
            net_price_vat=stats["net_price_vat"][index],
            net_number_sales=stats["net_number_sales"][index],
            date=_current_day,
        )
        days.append(day)

    previous_s = days[0] if days else dict()
    current["amount_delta"] = current["net_price_vat"] - previous_s.get(
        "net_price_vat", 0
    )
    current["number_delta"] = current["net_number_sales"] - previous_s.get(
        "net_number_sales", 0
    )

    if current["amount_delta"] == 0:
        current["amount_direction"] = "equal"
    elif current["amount_delta"] > 0:
        current["amount_direction"] = "up"
    else:
        current["amount_direction"] = "down"

    if current["number_delta"] == 0:
        current["number_direction"] = "equal"
    elif current["number_delta"] > 0:
        current["number_direction"] = "up"
    else:
        current["number_direction"] = "down"

    return flask.render_template(
        "store/sales.html.tpl",
        link="stores",
        sub_link="sales",
        store=store,
        stats=stats,
        current=current,
        days=days,
    )


def _global():
    return dict(object_id=-1, name="Global", primary_contact_information=dict())
