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

import omni
import quorum

from . import logic
from . import config
from . import business


def load():
    if not config.SCHEDULE:
        return
    quorum.debug("Loading scheduling tasks ...")
    load_slack()
    load_mail()


def load_slack():
    if not config.REMOTE:
        return
    sales_time = quorum.daily_work(sales_slack, offset=14400)
    previous_time = quorum.daily_work(previous_slack, offset=18000)
    week_time = quorum.weekly_work(week_slack, weekday=0, offset=14400)
    sales_date = datetime.datetime.utcfromtimestamp(sales_time)
    previous_date = datetime.datetime.utcfromtimestamp(previous_time)
    week_date = datetime.datetime.utcfromtimestamp(week_time)
    quorum.debug("Scheduled initial daily sales slack task for %s" % sales_date)
    quorum.debug(
        "Scheduled initial daily previous (sales) slack task for %s" % previous_date
    )
    quorum.debug(
        "Scheduled initial weekly previous week (sales) slack task for %s" % week_date
    )


def load_mail():
    if not config.REMOTE:
        return
    day_time = quorum.daily_work(birthday_mail, offset=14400)
    week_time = quorum.weekly_work(activity_mail, weekday=4, offset=14400)
    month_time = quorum.monthly_work(activity_previous, monthday=26, offset=14400)
    day_date = datetime.datetime.utcfromtimestamp(day_time)
    week_date = datetime.datetime.utcfromtimestamp(week_time)
    month_date = datetime.datetime.utcfromtimestamp(month_time)
    quorum.debug("Scheduled initial daily birthday mail task for %s" % day_date)
    quorum.debug("Scheduled initial weekly activity mail task for %s" % week_date)
    quorum.debug("Scheduled initial monthly activity previous task for %s" % month_date)


def sales_slack(offset=1):
    api = logic.get_api(mode=omni.API.DIRECT_MODE)
    business.slack_sales(api=api, offset=offset)


def previous_slack(offset=0):
    api = logic.get_api(mode=omni.API.DIRECT_MODE)
    business.slack_previous(api=api, offset=offset)


def week_slack(offset=0, span=7):
    api = logic.get_api(mode=omni.API.DIRECT_MODE)
    business.slack_week(api=api, offset=offset, span=span)


def birthday_mail(month=None, day=None):
    api = logic.get_api(mode=omni.API.DIRECT_MODE)
    business.mail_birthday_all(api=api, month=month, day=day, links=False)
    quorum.debug("Finished sending birthday emails")


def activity_mail(year=None, month=None):
    api = logic.get_api(mode=omni.API.DIRECT_MODE)
    business.mail_activity_all(
        api=api, year=year, month=month, validate=True, links=False
    )
    quorum.debug("Finished sending activity emails")


def activity_previous():
    now = datetime.datetime.utcnow()
    pre_year, pre_month = (
        (now.year - 1, 12) if now.month == 1 else (now.year, now.month - 1)
    )
    activity_mail(year=pre_year, month=pre_month)
