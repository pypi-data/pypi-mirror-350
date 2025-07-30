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

import time
import calendar
import datetime

import flask
import quorum

from . import logic
from . import config

BIRTHDAY_SUBJECT = dict(en_us="Happy Birthday", pt_pt="Feliz Aniversário")

ACTIVITY_SUBJECT = dict(
    en_us="Omni activity report for %s as of %s",
    pt_pt="Relatório de atividade Omni para %s em %s",
)


@quorum.ensure_context
def slack_sales(api=None, channel=None, all=False, offset=0):
    from omnix import models

    # tries to retrieve the reference to the API object
    # and if it fails returns immediately (soft fail)
    api = api or logic.get_api()
    settings = models.Settings.get_settings()
    slack_api = settings.get_slack_api()
    if not slack_api:
        return

    # retrieves the current time and updates it with the delta
    # converting then the value to a string
    current = datetime.datetime.utcfromtimestamp(time.time())
    delta = datetime.timedelta(days=offset)
    target = current - delta
    date_s = target.strftime("%d of %B")

    # calculates both the day and the month (time) reference values
    # to be used in the calculus of the comparison values, notice
    # that the day is positioned at the offset value in the month
    # and the month one is positioned at the beginning of the month
    # considered to be of reference (previous n months calculus)
    day_ref = target
    month_ref = target - datetime.timedelta(days=target.day)
    day_ref_t = calendar.timegm(day_ref.utctimetuple())
    month_ref_t = calendar.timegm(month_ref.utctimetuple())

    # retrieves the complete set of sales according to the
    # default value and then sorts the received object identifiers
    # according to their names and in case the
    contents = api.stats_sales(
        date=time.time() - offset * 86400, unit="day", span=1, has_global=True
    )
    object_ids = quorum.legacy.keys(contents)
    object_ids.sort()
    if not all:
        object_ids = ["-1"]

    # retrieves the comparison values from both the day level and
    # the month level, so that it's possible to compare both the
    # current month and the current year against the previous ones
    day_comparison = get_comparison(api=api, unit="day", timestamp=day_ref_t)
    month_comparison = get_comparison(api=api, unit="month", timestamp=month_ref_t)

    # in case the month in calculus is the first one then an empty
    # result is going to be forced as this is the case for the
    # first month of the year (only day comparison is relevant)
    if target.month == 1:
        month_comparison = empty_results(month_comparison)

    # increments the month values (year to date) that currently contain
    # only the completed month values with the values for the on-going
    # month (day comparison) this should provide the complete year to
    # date set of values (previous months plus current month values)
    month_comparison = sum_results(month_comparison, day_comparison)

    # starts both the best (sales) value and the numeric value
    # for this same best value, these values should start with
    # the lower possible values (to be overriden)
    best_value, value = None, -1.0

    # iterates over the complete set of "stores" to try to find
    # the one to be considered the best selling one and creates
    # the best value string for it
    for object_id, values in quorum.legacy.iteritems(contents):
        store_name = values["name"]
        store_net_price_vat = values["net_price_vat"][-1]
        if not store_net_price_vat > value:
            continue
        if object_id == "-1":
            continue
        value = store_net_price_vat
        best_value = "<%s|%s>" % (
            flask.url_for("sales_stores", id=object_id, _external=True),
            store_name,
        )

    # iterates over the complete set of object identifiers for which
    # a message is meant to be displayed and sends it using Slack API
    for object_id in object_ids:
        values = contents[object_id]
        name = values["name"]
        name = name.capitalize()
        text = "Sales report for %s" % date_s
        values = dict(
            number_entries=values["number_entries"][-1],
            net_price_vat=values["net_price_vat"][-1],
            net_average_sale=values["net_price_vat"][-1]
            / (values["net_number_sales"][-1] or 1.0),
            net_number_sales=values["net_number_sales"][-1],
        )
        slack_api.post_message_chat(
            channel or settings.slack_channel or "general",
            None,
            attachments=[
                dict(
                    fallback=text,
                    color="#36a64f",
                    title=text,
                    title_link=flask.url_for(
                        "sales_stores", id=object_id, _external=True
                    ),
                    test=text,
                    mrkdwn_in=["text", "pretext", "fields"],
                    fields=[
                        dict(
                            title="Store Name",
                            value="<%s|%s>"
                            % (
                                flask.url_for(
                                    "sales_stores", id=object_id, _external=True
                                ),
                                name,
                            ),
                            short=True,
                        ),
                        dict(title="Best Store", value=best_value, short=True),
                        dict(
                            title="Number Entries",
                            value="%d x" % values["number_entries"],
                            short=True,
                        ),
                        dict(
                            title="Number Sales",
                            value="%d x" % values["net_number_sales"],
                            short=True,
                        ),
                        dict(
                            title="Average Sale",
                            value="%.2f EUR" % values["net_average_sale"],
                            short=True,
                        ),
                        dict(
                            title="Total Sales",
                            value="*%.2f EUR*" % values["net_price_vat"],
                            short=True,
                            mrkdwn=True,
                        ),
                    ],
                )
            ],
        )

        reports = (
            dict(
                text="Month to date report for %s" % date_s, comparison=day_comparison
            ),
            dict(
                text="Year to date report for %s" % date_s, comparison=month_comparison
            ),
        )

        for report in reports:
            text, comparison = report["text"], report["comparison"]
            slack_api.post_message_chat(
                channel or settings.slack_channel or "general",
                None,
                attachments=[
                    dict(
                        fallback=text,
                        color="#36a64f",
                        title=text,
                        title_link=flask.url_for(
                            "sales_stores", id=object_id, _external=True
                        ),
                        test=text,
                        mrkdwn_in=["text", "pretext", "fields"],
                        fields=[
                            dict(
                                title="Store Name",
                                value="<%s|%s>"
                                % (
                                    flask.url_for(
                                        "sales_stores", id=object_id, _external=True
                                    ),
                                    name,
                                ),
                                short=True,
                            ),
                            dict(
                                title="Number Entries",
                                value="%d x / %+d x (%+.2f %%)"
                                % (
                                    comparison[object_id]["number_entries"]["current"],
                                    comparison[object_id]["number_entries"]["diff"],
                                    comparison[object_id]["number_entries"][
                                        "percentage"
                                    ],
                                ),
                                short=True,
                            ),
                            dict(
                                title="Number Sales",
                                value="%d x / %+d x (%+.2f %%)"
                                % (
                                    comparison[object_id]["net_number_sales"][
                                        "current"
                                    ],
                                    comparison[object_id]["net_number_sales"]["diff"],
                                    comparison[object_id]["net_number_sales"][
                                        "percentage"
                                    ],
                                ),
                                short=True,
                            ),
                            dict(
                                title="Average Sale",
                                value="%.2f EUR / %+.2f EUR (%+.2f %%)"
                                % (
                                    comparison[object_id]["net_average_sale"][
                                        "current"
                                    ],
                                    comparison[object_id]["net_average_sale"]["diff"],
                                    comparison[object_id]["net_average_sale"][
                                        "percentage"
                                    ],
                                ),
                                short=True,
                            ),
                            dict(
                                title="Total Sales",
                                value="*%.2f EUR / %+.2f EUR (%+.2f %%)*"
                                % (
                                    comparison[object_id]["net_price_vat"]["current"],
                                    comparison[object_id]["net_price_vat"]["diff"],
                                    comparison[object_id]["net_price_vat"][
                                        "percentage"
                                    ],
                                ),
                                short=False,
                                mrkdwn=True,
                            ),
                        ],
                    )
                ],
            )


@quorum.ensure_context
def slack_previous(api=None, channel=None, all=False, offset=0):
    from omnix import models

    # tries to retrieve the reference to the API object
    # and if it fails returns immediately (soft fail)
    api = api or logic.get_api()
    settings = models.Settings.get_settings()
    slack_api = settings.get_slack_api()
    if not slack_api:
        return

    current = datetime.datetime.utcfromtimestamp(time.time())
    previous = datetime.datetime(
        current.year - 1,
        current.month,
        current.day,
        hour=current.hour,
        minute=current.minute,
        second=current.second,
    )
    previous_t = previous.utctimetuple()
    previous_t = calendar.timegm(previous_t)

    contents = api.stats_sales(
        date=previous_t - offset * 86400, unit="day", span=1, has_global=True
    )

    # starts both the best (sales) value and the numeric value
    # for this same best value, these values should start with
    # the lower possible values (to be overriden)
    best_value, value = None, -1.0

    # iterates over the complete set of "stores" to try to find
    # the one to be considered the best selling one and creates
    # the best value string for it
    for object_id, values in quorum.legacy.iteritems(contents):
        store_name = values["name"]
        store_net_price_vat = values["net_price_vat"][-1]
        if not store_net_price_vat > value:
            continue
        if object_id == "-1":
            continue
        value = store_net_price_vat
        best_value = "<%s|%s>" % (
            flask.url_for("sales_stores", id=object_id, _external=True),
            store_name,
        )

    # unpacks the contents of the API call and creates some of the
    # global values to be used in the Slack message creation
    values = contents["-1"]
    name = values["name"]
    name = name.capitalize()
    text = "Previous period sales for %s" % previous.strftime("%d, %B of %Y")

    values = dict(
        number_entries=values["number_entries"][-1],
        net_price_vat=values["net_price_vat"][-1],
        net_average_sale=values["net_price_vat"][-1]
        / (values["net_number_sales"][-1] or 1.0),
        net_number_sales=values["net_number_sales"][-1],
    )

    slack_api.post_message_chat(
        channel or settings.slack_channel or "general",
        None,
        attachments=[
            dict(
                fallback=text,
                color="#36a64f",
                title=text,
                title_link=flask.url_for("sales_stores", id=object_id, _external=True),
                test=text,
                mrkdwn_in=["text", "pretext", "fields"],
                fields=[
                    dict(
                        title="Store Name",
                        value="<%s|%s>"
                        % (
                            flask.url_for("sales_stores", id=object_id, _external=True),
                            name,
                        ),
                        short=True,
                    ),
                    dict(title="Best Store", value=best_value, short=True),
                    dict(
                        title="Number Entries",
                        value="%d x" % values["number_entries"],
                        short=True,
                    ),
                    dict(
                        title="Number Sales",
                        value="%d x" % values["net_number_sales"],
                        short=True,
                    ),
                    dict(
                        title="Average Sale",
                        value="%.2f EUR" % values["net_average_sale"],
                        short=True,
                    ),
                    dict(
                        title="Total Sales",
                        value="*%.2f EUR*" % values["net_price_vat"],
                        short=True,
                        mrkdwn=True,
                    ),
                ],
            )
        ],
    )


@quorum.ensure_context
def slack_week(api=None, channel=None, all=False, offset=0, span=7):
    from omnix import models

    # tries to retrieve the reference to the API object
    # and if it fails returns immediately (soft fail)
    api = api or logic.get_api()
    settings = models.Settings.get_settings()
    slack_api = settings.get_slack_api()
    if not slack_api:
        return

    current = datetime.datetime.utcfromtimestamp(time.time())
    previous = datetime.datetime(
        current.year - 1,
        current.month,
        current.day,
        hour=current.hour,
        minute=current.minute,
        second=current.second,
    )
    previous_t = previous.utctimetuple()
    previous_t = calendar.timegm(previous_t)

    contents = api.stats_sales(
        date=previous_t + (span - offset - 1) * 86400,
        unit="day",
        span=span,
        has_global=True,
    )

    values = contents["-1"]
    name = values["name"]
    name = name.capitalize()
    text = "Weekly sales for %d" % previous.year

    fields = []
    curent_t = previous_t - offset * 86400

    for amount, number_sales in zip(
        values["net_price_vat"], values["net_number_sales"]
    ):
        fields.append(
            dict(
                title="Sales for %s"
                % (datetime.datetime.utcfromtimestamp(curent_t).strftime("%d of %B")),
                value="%.2f EUR (%d x)" % (amount, number_sales),
                short=False,
                mrkdwn=True,
            )
        )
        curent_t += 86400

    slack_api.post_message_chat(
        channel or settings.slack_channel or "general",
        None,
        attachments=[
            dict(
                fallback=text,
                color="#36a64f",
                title=text,
                test=text,
                mrkdwn_in=["text", "pretext", "fields"],
                fields=fields,
            )
        ],
    )


@quorum.ensure_context
def mail_birthday_all(api=None, month=None, day=None, validate=False, links=True):
    api = api or logic.get_api()
    has_date = month and day
    if not has_date:
        current = datetime.datetime.utcnow()
        month, day = current.month, current.day
    birth_day = "%02d/%02d" % (month, day)
    employees = api.list_employees(
        object=dict(limit=-1), **{"filters[]": ["birth_day:equals:%s" % birth_day]}
    )
    for employee in employees:
        try:
            mail_birthday(api=api, id=employee["object_id"], links=links)
        except quorum.OperationalError:
            pass


@quorum.ensure_context
def mail_activity_all(api=None, year=None, month=None, validate=False, links=True):
    api = api or logic.get_api()
    employees = api.list_employees(object=dict(limit=-1))
    for employee in employees:
        try:
            mail_activity(
                api=api,
                id=employee["object_id"],
                year=year,
                month=month,
                validate=validate,
                links=links,
            )
        except quorum.OperationalError:
            pass


@quorum.ensure_context
def mail_birthday(api=None, id=None, links=True):
    api = api or logic.get_api()
    employee = api.get_employee(id) if id else api.self_employee()

    name = employee.get("full_name", None)
    working = employee.get("working", None)
    contact_information = employee.get("primary_contact_information", {})
    email = contact_information.get("email", None)

    if not name:
        raise quorum.OperationalError("No name defined")
    if not email:
        raise quorum.OperationalError("No email defined")
    if not working == 1:
        raise quorum.OperationalError("No longer working")

    quorum.debug("Sending birthday email to %s <%s>" % (name, email))
    quorum.send_mail(
        subject=BIRTHDAY_SUBJECT[config.LOCALE],
        sender=config.SENDER_EMAIL,
        receivers=["%s <%s>" % (name, email)],
        rich=config.BIRTHDAY_TEMPLATE,
        context=dict(
            settings=dict(logo=True, links=links),
            base_url=config.BASE_URL,
            omnix_base_url=config.OMNI_URL,
            commission_rate=config.COMMISSION_RATE,
        ),
    )


@quorum.ensure_context
def mail_activity(api=None, id=None, year=None, month=None, validate=False, links=True):
    api = api or logic.get_api()
    employee = api.get_employee(id) if id else api.self_employee()

    name = employee.get("full_name", None)
    working = employee.get("working", None)
    contact_information = employee.get("primary_contact_information", {})
    email = contact_information.get("email", None)

    if not name:
        raise quorum.OperationalError("No name defined")
    if not email:
        raise quorum.OperationalError("No email defined")
    if not working == 1:
        raise quorum.OperationalError("No longer working")

    now = datetime.datetime.utcnow()
    now_s = now.strftime("%B %d %Y")

    (
        operations,
        target_s,
        sales_total,
        sales_s,
        returns_s,
        _previous_month,
        _previous_year,
        _next_month,
        _next_year,
        _has_next,
    ) = get_sales(api=api, id=id, year=year, month=month)

    if validate and not operations:
        return

    quorum.debug("Sending activity email to %s <%s>" % (name, email))
    quorum.send_mail(
        subject=ACTIVITY_SUBJECT[config.LOCALE] % (target_s, now_s),
        sender=config.SENDER_EMAIL,
        receivers=["%s <%s>" % (name, email)],
        rich="email/activity.%s.html.tpl" % config.LOCALE,
        context=dict(
            settings=dict(logo=True, links=links),
            target=target_s,
            operations=operations,
            sales_total=sales_total,
            sales_count=len(sales_s),
            returns_count=len(returns_s),
            base_url=config.BASE_URL,
            omnix_base_url=config.OMNI_URL,
            commission_rate=config.COMMISSION_RATE,
        ),
    )


def get_date(year=None, month=None, pivot=config.FIRST_DAY):
    now = datetime.datetime.utcnow()
    year = year or now.year
    month = month or now.month

    has_next = int("%04d%02d" % (year, month)) < int("%04d%02d" % (now.year, now.month))

    previous_month, previous_year = (
        (month - 1, year) if not month == 1 else (12, year - 1)
    )
    next_month, next_year = (month + 1, year) if not month == 12 else (1, year + 1)

    start_month, start_year = (
        (month, year) if now.day >= pivot else (previous_month, previous_year)
    )
    if pivot == config.FIRST_DAY:
        end_month, end_year = start_month, start_year
    else:
        end_month, end_year = (
            (start_month + 1, start_year)
            if not start_month == 12
            else (1, start_year + 1)
        )

    start = datetime.datetime(year=start_year, month=start_month, day=pivot)
    end = datetime.datetime(year=end_year, month=end_month, day=pivot)

    start_t = calendar.timegm(start.utctimetuple())
    end_t = calendar.timegm(end.utctimetuple())

    target = datetime.datetime(year=end_year, month=end_month, day=1)
    target = target.strftime("%B %Y")

    return (
        target,
        month,
        year,
        start_t,
        end_t,
        previous_month,
        previous_year,
        next_month,
        next_year,
        has_next,
    )


def get_top(api=None, year=None, month=None):
    api = api or logic.get_api()

    (
        target,
        month,
        year,
        start_t,
        _end_t,
        previous_month,
        previous_year,
        next_month,
        next_year,
        has_next,
    ) = get_date(year=year, month=month)

    stats = api.stats_employee(date=start_t, unit="month", span=1, has_global=True)

    top_employees = []
    for object_id, values in stats.items():
        values = values["-1"]
        values["object_id"] = object_id
        values["amount_price_vat"] = values["amount_price_vat"][0]
        values["number_sales"] = values["number_sales"][0]
        top_employees.append(values)

    top_employees.sort(reverse=True, key=lambda value: value["amount_price_vat"])

    return (
        top_employees,
        target,
        previous_month,
        previous_year,
        next_month,
        next_year,
        has_next,
    )


def get_sales(api=None, id=None, year=None, month=None):
    api = api or logic.get_api()

    (
        target,
        month,
        year,
        start_t,
        end_t,
        previous_month,
        previous_year,
        next_month,
        next_year,
        has_next,
    ) = get_date(year=year, month=month, pivot=config.COMMISSION_DAY)

    kwargs = {
        "filter_string": "",
        "start_record": 0,
        "number_records": -1,
        "sort": "date:descending",
        "filters[]": ["date:greater:" + str(start_t), "date:lesser:" + str(end_t)],
    }
    if id:
        kwargs["filters[]"].append("primary_seller:equals:" + str(id))
    sales = api.list_sales(**kwargs) if id else api.self_sales(**kwargs)

    kwargs = {
        "filter_string": "",
        "start_record": 0,
        "number_records": -1,
        "sort": "date:descending",
        "filters[]": ["date:greater:" + str(start_t), "date:lesser:" + str(end_t)],
    }

    if id:
        kwargs["filters[]"].append("primary_return_processor:equals:" + str(id))
    returns = api.list_returns(**kwargs) if id else api.self_returns(**kwargs)

    operations = returns + sales

    sorter = lambda item: item["date"]
    operations.sort(key=sorter, reverse=True)

    sales_total = 0
    for sale in sales:
        sales_total += sale["price"]["value"]
    for _return in returns:
        sales_total -= _return["price"]["value"]

    for operation in operations:
        date = operation["date"]
        date_t = datetime.datetime.utcfromtimestamp(date)
        operation["date_f"] = date_t.strftime("%b %d, %Y")

    return (
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
    )


def get_comparison(api=None, unit="day", offset=0, timestamp=None):
    from omnix import models

    # tries to retrieve the reference to the API object
    # and if it fails returns immediately (soft fail)
    api = api or logic.get_api()
    settings = models.Settings.get_settings()
    slack_api = settings.get_slack_api()
    if not slack_api:
        return

    # retrieves both the current and the previous dictionary
    # set of arguments to be passed to the API requests
    current_args, previous_args = calc_comparison(
        unit=unit, offset=offset, timestamp=timestamp
    )

    # retrieves both the current and the previous values so that
    # they can be properly compared, notice the proper span
    current_v = api.stats_sales(**current_args)
    previous_v = api.stats_sales(**previous_args)

    # creates the dictionary that is going to store the multiple
    # comparison values in a per object identifier basis
    results = dict()

    for object_id in quorum.legacy.keys(current_v):
        current_i = current_v.get(object_id, {})
        previous_i = previous_v.get(object_id, {})

        result = dict(
            number_entries=dict(
                current=sum(current_i.get("number_entries", [])),
                previous=sum(previous_i.get("number_entries", [])),
            ),
            net_price_vat=dict(
                current=sum(current_i.get("net_price_vat", [])),
                previous=sum(previous_i.get("net_price_vat", [])),
            ),
            net_number_sales=dict(
                current=sum(current_i.get("net_number_sales", [])),
                previous=sum(previous_i.get("net_number_sales", [])),
            ),
        )

        # sets the current object identifier result in the map
        # of results (for latter usage)
        results[object_id] = result

    # runs the post-processing calculus operations on the results
    # so that the calculated attributes get correctly processed
    calc_extra(results)
    calc_results(results)

    return results


def sum_results(first, second, calc=True):
    """
    Sums the results of the first comparison dictionary
    with the second one.

    The function should return a dictionary compliant with
    the structure of the input ones.

    :type first: Dictionary
    :param first: The first comparison dictionary to be used
    for the sum operation.
    :type second: Dictionary
    :param second: The second comparison dictionary to be used
    in the sum.
    :type calc: bool
    :param calc: If the calculated attributes should be re-calculated
    after the sum has occurred.
    :rtype: Dictionary
    :return: A new dictionary containing the resulting values.
    """

    result = dict()

    for object_id in quorum.legacy.iterkeys(first):
        first_r = first[object_id]
        second_r = second.get(object_id, {})

        result_r = result.get(object_id, {})
        result[object_id] = result_r

        for key in quorum.legacy.iterkeys(first_r):
            first_m = first_r[key]
            second_m = second_r.get(key, {})

            result_m = result_r.get(key, {})
            result_r[key] = result_m

            # iterates over the complete set of keys in the first
            # map to calculate the complete set of sums
            for _key in quorum.legacy.iterkeys(first_m):
                result_m[_key] = first_m.get(_key, 0.0) + second_m.get(_key, 0.0)

    if calc:
        calc_extra(result)
        calc_results(result)

    return result


def empty_results(input, calc=True):
    """
    Generates an empty results dictionary taking as reference the
    input dictionary structure.

    The resulting dictionary should conform with the expected input
    specification.

    :type first: Dictionary
    :param first: The comparison dictionary to be used for the spec
    analysis on the generation of the empty dictionary.
    :type calc: bool
    :param calc: If the calculated attributes should be re-calculated
    after the empty operation has occurred.
    :rtype: Dictionary
    :return: A new dictionary containing an empty result set.
    """

    result = dict()

    for object_id in quorum.legacy.iterkeys(input):
        input_r = input[object_id]

        result_r = result.get(object_id, {})
        result[object_id] = result_r

        for key in quorum.legacy.iterkeys(input_r):
            input_m = input_r[key]

            result_m = result_r.get(key, {})
            result_r[key] = result_m

            for _key in quorum.legacy.iterkeys(input_m):
                result_m[_key] = 0.0

    if calc:
        calc_extra(result)
        calc_results(result)

    return result


def calc_comparison(unit="day", offset=0, timestamp=None):
    # tries to retrieve the proper timestamp value falling back
    # to the current time in case nothing is provided
    timestamp = timestamp or time.time()

    # retrieves the current time and updates it with the delta
    # converting then the value to a string
    if unit == "day":
        current = datetime.datetime.utcfromtimestamp(timestamp + offset * 86400)
    if unit == "month":
        now = datetime.datetime.utcfromtimestamp(timestamp + offset * 86400)
        current = datetime.datetime(
            now.year,
            now.month,
            now.day,
            hour=now.hour,
            minute=now.minute,
            second=now.second,
        )
    current_t = current.utctimetuple()
    current_t = calendar.timegm(current_t)

    try:
        # calculates the previous period timestamp by removing one
        # complete year from the current time
        previous = datetime.datetime(
            current.year - 1,
            current.month,
            current.day,
            hour=current.hour,
            minute=current.minute,
            second=current.second,
        )
    except ValueError:
        # in case the value error assumes that's because of a leap
        # year invalid date range and decrements the day by one
        previous = datetime.datetime(
            current.year - 1,
            current.month,
            current.day - 1,
            hour=current.hour,
            minute=current.minute,
            second=current.second,
        )
    previous_t = previous.utctimetuple()
    previous_t = calendar.timegm(previous_t)

    # tries to retrieve the proper span value according to the
    # requested unit of comparison
    if unit == "day":
        span_c, span_p = current.day, previous.day
    if unit == "month":
        span_c, span_p = current.month, previous.month

    # return a tuple containing both the current and previous values,
    # to be evaluated from the outside as expected, possible to be used
    # to pass then to a remote API request
    return dict(date=current_t, unit=unit, span=span_c, has_global=True), dict(
        date=previous_t, unit=unit, span=span_p, has_global=True
    )


def calc_extra(results):
    for result in quorum.legacy.itervalues(results):
        result["net_average_sale"] = dict(
            current=result["net_price_vat"]["current"]
            / (result["net_number_sales"]["current"] or 1.0),
            previous=result["net_price_vat"]["previous"]
            / (result["net_number_sales"]["previous"] or 1.0),
        )


def calc_results(results):
    for result in quorum.legacy.itervalues(results):
        for values in quorum.legacy.itervalues(result):
            values["diff"] = values["current"] - values["previous"]
            values["percentage"] = (
                float(values["diff"])
                / (float(values["previous"]) or float(values["diff"]) or 1.0)
                * 100.0
            )
