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

import calendar
import datetime
import unittest

import omnix


class BusinessTest(unittest.TestCase):

    def test_get_comparison_day(self):
        timestamp = calendar.timegm(
            datetime.datetime(year=2018, month=3, day=1, hour=4).utctimetuple()
        )
        current = calendar.timegm(
            datetime.datetime(year=2018, month=2, day=28, hour=4).utctimetuple()
        )
        previous = calendar.timegm(
            datetime.datetime(year=2017, month=2, day=28, hour=4).utctimetuple()
        )
        current_v, previous_v = omnix.calc_comparison(
            unit="day", offset=-1, timestamp=timestamp
        )

        self.assertEqual(current_v["date"], current)
        self.assertEqual(current_v["span"], 28)
        self.assertEqual(current_v["unit"], "day")
        self.assertEqual(current_v["has_global"], True)

        self.assertEqual(previous_v["date"], previous)
        self.assertEqual(previous_v["span"], 28)
        self.assertEqual(previous_v["unit"], "day")
        self.assertEqual(previous_v["has_global"], True)

        timestamp = calendar.timegm(
            datetime.datetime(year=2018, month=3, day=1, hour=4).utctimetuple()
        )
        current = calendar.timegm(
            datetime.datetime(year=2018, month=3, day=1, hour=4).utctimetuple()
        )
        previous = calendar.timegm(
            datetime.datetime(year=2017, month=3, day=1, hour=4).utctimetuple()
        )
        current_v, previous_v = omnix.calc_comparison(
            unit="day", offset=0, timestamp=timestamp
        )

        self.assertEqual(current_v["date"], current)
        self.assertEqual(current_v["span"], 1)
        self.assertEqual(current_v["unit"], "day")
        self.assertEqual(current_v["has_global"], True)

        self.assertEqual(previous_v["date"], previous)
        self.assertEqual(previous_v["span"], 1)
        self.assertEqual(previous_v["unit"], "day")
        self.assertEqual(previous_v["has_global"], True)

    def test_get_comparison_day_leap(self):
        timestamp = calendar.timegm(
            datetime.datetime(year=2020, month=3, day=1, hour=4).utctimetuple()
        )
        current = calendar.timegm(
            datetime.datetime(year=2020, month=2, day=29, hour=4).utctimetuple()
        )
        previous = calendar.timegm(
            datetime.datetime(year=2019, month=2, day=28, hour=4).utctimetuple()
        )
        current_v, previous_v = omnix.calc_comparison(
            unit="day", offset=-1, timestamp=timestamp
        )

        self.assertEqual(current_v["date"], current)
        self.assertEqual(current_v["span"], 29)
        self.assertEqual(current_v["unit"], "day")
        self.assertEqual(current_v["has_global"], True)

        self.assertEqual(previous_v["date"], previous)
        self.assertEqual(previous_v["span"], 28)
        self.assertEqual(previous_v["unit"], "day")
        self.assertEqual(previous_v["has_global"], True)

    def test_get_comparison_month(self):
        timestamp = calendar.timegm(
            datetime.datetime(year=2018, month=3, day=1, hour=4).utctimetuple()
        )
        current = calendar.timegm(
            datetime.datetime(year=2018, month=2, day=28, hour=4).utctimetuple()
        )
        previous = calendar.timegm(
            datetime.datetime(year=2017, month=2, day=28, hour=4).utctimetuple()
        )
        current_v, previous_v = omnix.calc_comparison(
            unit="month", offset=-1, timestamp=timestamp
        )

        self.assertEqual(current_v["date"], current)
        self.assertEqual(current_v["span"], 2)
        self.assertEqual(current_v["unit"], "month")
        self.assertEqual(current_v["has_global"], True)

        self.assertEqual(previous_v["date"], previous)
        self.assertEqual(previous_v["span"], 2)
        self.assertEqual(previous_v["unit"], "month")
        self.assertEqual(previous_v["has_global"], True)

        timestamp = calendar.timegm(
            datetime.datetime(year=2018, month=3, day=1, hour=4).utctimetuple()
        )
        current = calendar.timegm(
            datetime.datetime(year=2018, month=3, day=1, hour=4).utctimetuple()
        )
        previous = calendar.timegm(
            datetime.datetime(year=2017, month=3, day=1, hour=4).utctimetuple()
        )
        current_v, previous_v = omnix.calc_comparison(
            unit="month", offset=0, timestamp=timestamp
        )

        self.assertEqual(current_v["date"], current)
        self.assertEqual(current_v["span"], 3)
        self.assertEqual(current_v["unit"], "month")
        self.assertEqual(current_v["has_global"], True)

        self.assertEqual(previous_v["date"], previous)
        self.assertEqual(previous_v["span"], 3)
        self.assertEqual(previous_v["unit"], "month")
        self.assertEqual(previous_v["has_global"], True)

        timestamp = calendar.timegm(
            datetime.datetime(year=2018, month=3, day=1, hour=4).utctimetuple()
        )
        current = calendar.timegm(
            datetime.datetime(year=2018, month=2, day=25, hour=4).utctimetuple()
        )
        previous = calendar.timegm(
            datetime.datetime(year=2017, month=2, day=25, hour=4).utctimetuple()
        )
        current_v, previous_v = omnix.calc_comparison(
            unit="month", offset=-4, timestamp=timestamp
        )

        self.assertEqual(current_v["date"], current)
        self.assertEqual(current_v["span"], 2)
        self.assertEqual(current_v["unit"], "month")
        self.assertEqual(current_v["has_global"], True)

        self.assertEqual(previous_v["date"], previous)
        self.assertEqual(previous_v["span"], 2)
        self.assertEqual(previous_v["unit"], "month")
        self.assertEqual(previous_v["has_global"], True)

        timestamp = calendar.timegm(
            datetime.datetime(year=2018, month=4, day=1, hour=4).utctimetuple()
        )
        current = calendar.timegm(
            datetime.datetime(year=2018, month=3, day=31, hour=4).utctimetuple()
        )
        previous = calendar.timegm(
            datetime.datetime(year=2017, month=3, day=31, hour=4).utctimetuple()
        )
        current_v, previous_v = omnix.calc_comparison(
            unit="month", offset=-1, timestamp=timestamp
        )

        self.assertEqual(current_v["date"], current)
        self.assertEqual(current_v["span"], 3)
        self.assertEqual(current_v["unit"], "month")
        self.assertEqual(current_v["has_global"], True)

        self.assertEqual(previous_v["date"], previous)
        self.assertEqual(previous_v["span"], 3)
        self.assertEqual(previous_v["unit"], "month")
        self.assertEqual(previous_v["has_global"], True)

        timestamp = calendar.timegm(
            datetime.datetime(year=2018, month=1, day=2, hour=4).utctimetuple()
        )
        current = calendar.timegm(
            datetime.datetime(year=2018, month=1, day=1, hour=4).utctimetuple()
        )
        previous = calendar.timegm(
            datetime.datetime(year=2017, month=1, day=1, hour=4).utctimetuple()
        )
        current_v, previous_v = omnix.calc_comparison(
            unit="month", offset=-1, timestamp=timestamp
        )

        self.assertEqual(current_v["date"], current)
        self.assertEqual(current_v["span"], 1)
        self.assertEqual(current_v["unit"], "month")
        self.assertEqual(current_v["has_global"], True)

        self.assertEqual(previous_v["date"], previous)
        self.assertEqual(previous_v["span"], 1)
        self.assertEqual(previous_v["unit"], "month")
        self.assertEqual(previous_v["has_global"], True)

        timestamp = calendar.timegm(
            datetime.datetime(year=2018, month=2, day=1, hour=4).utctimetuple()
        )
        current = calendar.timegm(
            datetime.datetime(year=2018, month=1, day=31, hour=4).utctimetuple()
        )
        previous = calendar.timegm(
            datetime.datetime(year=2017, month=1, day=31, hour=4).utctimetuple()
        )
        current_v, previous_v = omnix.calc_comparison(
            unit="month", offset=-1, timestamp=timestamp
        )

        self.assertEqual(current_v["date"], current)
        self.assertEqual(current_v["span"], 1)
        self.assertEqual(current_v["unit"], "month")
        self.assertEqual(current_v["has_global"], True)

        self.assertEqual(previous_v["date"], previous)
        self.assertEqual(previous_v["span"], 1)
        self.assertEqual(previous_v["unit"], "month")
        self.assertEqual(previous_v["has_global"], True)

        timestamp = calendar.timegm(
            datetime.datetime(year=2018, month=2, day=2, hour=4).utctimetuple()
        )
        current = calendar.timegm(
            datetime.datetime(year=2018, month=1, day=31, hour=4).utctimetuple()
        )
        previous = calendar.timegm(
            datetime.datetime(year=2017, month=1, day=31, hour=4).utctimetuple()
        )
        current_v, previous_v = omnix.calc_comparison(
            unit="month", offset=-2, timestamp=timestamp
        )

        self.assertEqual(current_v["date"], current)
        self.assertEqual(current_v["span"], 1)
        self.assertEqual(current_v["unit"], "month")
        self.assertEqual(current_v["has_global"], True)

        self.assertEqual(previous_v["date"], previous)
        self.assertEqual(previous_v["span"], 1)
        self.assertEqual(previous_v["unit"], "month")
        self.assertEqual(previous_v["has_global"], True)

        timestamp = calendar.timegm(
            datetime.datetime(year=2018, month=1, day=2, hour=4).utctimetuple()
        )
        current = calendar.timegm(
            datetime.datetime(year=2017, month=12, day=31, hour=4).utctimetuple()
        )
        previous = calendar.timegm(
            datetime.datetime(year=2016, month=12, day=31, hour=4).utctimetuple()
        )
        current_v, previous_v = omnix.calc_comparison(
            unit="month", offset=-2, timestamp=timestamp
        )

        self.assertEqual(current_v["date"], current)
        self.assertEqual(current_v["span"], 12)
        self.assertEqual(current_v["unit"], "month")
        self.assertEqual(current_v["has_global"], True)

        self.assertEqual(previous_v["date"], previous)
        self.assertEqual(previous_v["span"], 12)
        self.assertEqual(previous_v["unit"], "month")
        self.assertEqual(previous_v["has_global"], True)

    def test_get_comparison_month_leap(self):
        timestamp = calendar.timegm(
            datetime.datetime(year=2020, month=3, day=1, hour=4).utctimetuple()
        )
        current = calendar.timegm(
            datetime.datetime(year=2020, month=2, day=29, hour=4).utctimetuple()
        )
        previous = calendar.timegm(
            datetime.datetime(year=2019, month=2, day=28, hour=4).utctimetuple()
        )
        current_v, previous_v = omnix.calc_comparison(
            unit="month", offset=-1, timestamp=timestamp
        )

        self.assertEqual(current_v["date"], current)
        self.assertEqual(current_v["span"], 2)
        self.assertEqual(current_v["unit"], "month")
        self.assertEqual(current_v["has_global"], True)

        self.assertEqual(previous_v["date"], previous)
        self.assertEqual(previous_v["span"], 2)
        self.assertEqual(previous_v["unit"], "month")
        self.assertEqual(previous_v["has_global"], True)
