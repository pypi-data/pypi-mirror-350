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

import flask  # @UnusedImport
import datetime

import quorum

import omnix.models

MONGO_DATABASE = "omnix"
""" The default database to be used for the connection with
the MongoDB database """

SECRET_KEY = "zhsga32ki5kvv7ymq8nolbleg248fzn1"
""" The "secret" key to be at the internal encryption
processes handled by flask (eg: sessions) """


@quorum.onrun
def onrun():
    import omnix.util

    omnix.util.run_slave(1)
    omnix.util.run_supervisor()
    omnix.util.load_scheduling()


app = quorum.load(
    name=__name__,
    secret_key=SECRET_KEY,
    mongo_database=MONGO_DATABASE,
    logger="omnix.debug",
    models=omnix.models,
    PERMANENT_SESSION_LIFETIME=datetime.timedelta(31),
    MAX_CONTENT_LENGTH=1024**3,
)

import omnix.views  # @UnusedImport

if __name__ == "__main__":
    quorum.run(server="netius")
else:
    __path__ = []
