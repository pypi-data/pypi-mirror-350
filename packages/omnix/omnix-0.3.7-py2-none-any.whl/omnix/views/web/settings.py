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
from omnix import models

from omnix.main import app
from omnix.main import flask
from omnix.main import quorum


@app.route("/settings/slack/ensure", methods=("GET",))
@quorum.ensure("base.admin")
def ensure_slack():
    next = quorum.get_field("next")
    api = _get_slack_api()
    return flask.redirect(api.oauth_authorize(state=next))


@app.route("/settings/slack/oauth", methods=("GET",))
@quorum.ensure("base.admin")
def oauth_slack():
    code = quorum.get_field("code")
    state = quorum.get_field("state")
    next = state
    api = _get_slack_api()
    access_token = api.oauth_access(code)
    settings = models.Settings.get_settings()
    settings.slack_token = access_token
    settings.slack_channel = api.channel
    settings.save()
    return flask.redirect(next or flask.url_for("index"))


def _get_slack_api(scope=None):
    import slack

    kwargs = dict()
    redirect_url = util.BASE_URL + flask.url_for("oauth_slack")
    access_token = flask.session and flask.session.get("slack.access_token", None)
    if scope:
        kwargs["scope"] = scope
    return slack.API(
        client_id=quorum.conf("SLACK_ID"),
        client_secret=quorum.conf("SLACK_SECRET"),
        redirect_url=redirect_url,
        access_token=access_token,
        **kwargs
    )
