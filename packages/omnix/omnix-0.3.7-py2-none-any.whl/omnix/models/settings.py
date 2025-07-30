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

import flask
import quorum

from omnix import util

from . import base


class Settings(base.Base):

    slack_token = quorum.field(
        index="hashed",
        observations="""The OAuth token from Slack that is going
        to be used for long term Slack interaction after the OAuth
        authentication process is completed""",
    )

    slack_channel = quorum.field(index="hashed")

    extra = quorum.field(type=dict)

    @classmethod
    def get_settings(cls, *args, **kwargs):
        return cls.singleton(*args, **kwargs)

    @classmethod
    def linked_apis(cls):
        linked = dict()
        settings = cls.get_settings()
        if settings.slack_token:
            linked["slack"] = settings.slack_token
        return linked

    @classmethod
    def _plural(cls):
        return "Settings"

    def get_slack_api(self):
        try:
            import slack
        except ImportError:
            return None
        if not self.slack_token:
            return None
        redirect_url = util.BASE_URL + flask.url_for("oauth_slack")
        access_token = self.slack_token
        return slack.API(
            client_id=quorum.conf("SLACK_ID"),
            client_secret=quorum.conf("SLACK_SECRET"),
            redirect_url=redirect_url,
            access_token=access_token,
        )
