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

import json

from omnix import util

from omnix.main import app
from omnix.main import flask
from omnix.main import quorum


@app.route("/entities", methods=("GET",))
@quorum.ensure("foundation.root_entity.list")
def list_entities():
    return flask.render_template("entity/list.html.tpl", link="entities")


@app.route("/entities.json", methods=("GET",), json=True)
@quorum.ensure("foundation.root_entity.list")
def list_entities_json():
    api = util.get_api()
    object = quorum.get_object()
    return api.list_entities(**object)


@app.route("/entities/<int:id>", methods=("GET",))
@quorum.ensure("foundation.root_entity.show")
def show_entities(id):
    api = util.get_api()
    entity = api.get_entity(id)
    metadata = entity.get("metadata", None)
    entity["metadata_s"] = _metadata_s(metadata)
    return flask.render_template(
        "entity/show.html.tpl", link="entities", sub_link="info", entity=entity
    )


@app.route("/entities/<int:id>/edit", methods=("GET",))
@quorum.ensure("foundation.root_entity.update")
def edit_entities(id):
    api = util.get_api()
    entity = api.get_entity(id)
    metadata = entity.get("metadata", None)
    entity["metadata_s"] = _metadata_s(metadata)
    return flask.render_template(
        "entity/edit.html.tpl",
        link="entities",
        sub_link="edit",
        entity=entity,
        errors=dict(),
    )


@app.route("/entities/<int:id>/update", methods=("POST",))
@quorum.ensure("foundation.root_entity.update")
def update_entities(id):
    models = util.get_models()
    api = util.get_api()
    object = quorum.get_object()
    for name, value in object.items():
        object[name] = None if value == "" else value
    entity = models.Entity.new(model=object, build=False, fill=False)
    api.update_entity(id, payload=dict(root_entity=entity.model))
    return flask.redirect(flask.url_for("show_entities", id=id))


def _metadata_s(metadata):
    return (
        json.dumps(
            metadata,
            ensure_ascii=False,
            indent=4,
            separators=(",", " : "),
            sort_keys=True,
        )
        if not metadata == None
        else None
    )
