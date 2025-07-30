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

import csv

import quorum


def csv_file(
    file, callback, header=False, delimiter=",", strict=False, encoding="utf-8"
):
    _file_name, mime_type, data = file
    is_csv = mime_type in ("text/csv", "application/vnd.ms-excel")
    if not is_csv and strict:
        raise quorum.OperationalError("Invalid MIME type '%s'" % mime_type)
    data = data.decode(encoding)
    buffer = quorum.legacy.StringIO(data)
    return csv_import(buffer, callback, header=header, delimiter=delimiter)


def csv_import(
    buffer, callback, header=False, delimiter=",", quoting=False, encoding="utf-8"
):
    is_unicode = quorum.legacy.PYTHON_3
    if is_unicode:
        data = buffer.read()
        data = data.decode(encoding)
        buffer = quorum.legacy.StringIO(data)
    csv_reader = csv.reader(
        buffer,
        delimiter=delimiter,
        quoting=csv.QUOTE_MINIMAL if quoting else csv.QUOTE_NONE,
    )
    if header:
        _header = next(csv_reader)
    else:
        _header = []
    for line in csv_reader:
        if not is_unicode:
            line = [value.decode(encoding) for value in line]
        callback(line, header=_header)


def csv_value(name, line, header):
    values = zip(line, header)
    return values[name]
