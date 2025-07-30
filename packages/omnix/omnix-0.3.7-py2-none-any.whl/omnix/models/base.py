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

import quorum


class Base(quorum.Model):

    id = dict(type=int, index=True, increment=True, immutable=True)

    enabled = dict(type=bool, index=True)

    def pre_create(self):
        quorum.Model.pre_create(self)

        self.enabled = True

    def enable(self):
        store = self._get_store()
        store.update({"_id": self._id}, {"$set": {"enabled": True}})

    def disable(self):
        store = self._get_store()
        store.update({"_id": self._id}, {"$set": {"enabled": False}})
