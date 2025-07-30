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
import traceback

from omnix import util

from omnix.main import app
from omnix.main import flask
from omnix.main import quorum


@app.route("/", methods=("GET",))
@app.route("/index", methods=("GET",))
@quorum.ensure("base")
def index():
    return flask.render_template("index.html.tpl", link="home")


@app.route("/signin", methods=("GET",))
def signin():
    next = quorum.get_field("next", None)
    return flask.render_template("signin.html.tpl", next=next)


@app.route("/signin", methods=("POST",))
def login():
    next = quorum.get_field("next", None)
    url = util.ensure_api(state=next)
    if url:
        return flask.redirect(url)
    return flask.redirect(next or flask.url_for("index"))


@app.route("/signin_do", methods=("GET",))
def do_login():
    next = quorum.get_field("next", None)
    url = util.ensure_api(state=next)
    if url:
        return flask.redirect(url)
    return flask.redirect(next or flask.url_for("index"))


@app.route("/logout", methods=("GET",))
def logout():
    next = quorum.get_field("next", None)
    util.reset_session()
    return flask.redirect(next or flask.url_for("index"))


@app.route("/about", methods=("GET",))
@quorum.ensure("base")
def about():
    access_token = flask.session.get("omnix.access_token", None)
    session_id = flask.session.get("omnix.session_id", None)

    return flask.render_template(
        "about.html.tpl", link="about", access_token=access_token, session_id=session_id
    )


@app.route("/reset", methods=("GET",))
def reset():
    util.reset_session()

    return flask.redirect(flask.url_for("index"))


@app.route("/flush_slack", methods=("GET",))
@app.route("/flush_slack_sales", methods=("GET",))
@quorum.ensure("base.admin")
def flush_slack_sales():
    channel = quorum.get_field("channel", None)
    offset = quorum.get_field("offset", 0, cast=int)

    util.slack_sales(channel=channel, offset=offset)

    return flask.redirect(flask.url_for("index", message="Slack events have been sent"))


@app.route("/flush_slack_previous", methods=("GET",))
@quorum.ensure("base.admin")
def flush_slack_previous():
    channel = quorum.get_field("channel", None)
    offset = quorum.get_field("offset", 0, cast=int)

    util.slack_previous(channel=channel, offset=offset)

    return flask.redirect(flask.url_for("index", message="Slack events have been sent"))


@app.route("/flush_slack_week", methods=("GET",))
@quorum.ensure("base.admin")
def flush_slack_week():
    channel = quorum.get_field("channel", None)
    offset = quorum.get_field("offset", 0, cast=int)
    span = quorum.get_field("span", 7, cast=int)

    util.slack_week(channel=channel, offset=offset, span=span)

    return flask.redirect(flask.url_for("index", message="Slack events have been sent"))


@app.route("/flush_birthday", methods=("GET",))
@quorum.ensure("base.admin")
def flush_birthday():
    month = quorum.get_field("month", None, cast=int)
    day = quorum.get_field("day", None, cast=int)

    util.mail_birthday_all(month=month, day=day, links=False)

    return flask.redirect(
        flask.url_for("index", message="Birthday emails have been sent")
    )


@app.route("/flush_activity", methods=("GET",))
@quorum.ensure("base.admin")
def flush_activity():
    util.mail_activity_all(validate=True, links=False)

    return flask.redirect(
        flask.url_for("index", message="Activity emails have been sent")
    )


@app.route("/flush_at", methods=("GET",))
@quorum.ensure("base.admin")
def flush_at():
    # creates a values map structure to retrieve the complete
    # set of inbound documents that have not yet been submitted
    # to at for the flush operation
    kwargs = {
        "filter_string": "",
        "start_record": 0,
        "number_records": 1000,
        "sort": "issue_date:ascending",
        "filters[]": [
            "issue_date:greater:1356998400",
            "submitted_at:equals:2",
            "document_type:equals:3",
        ],
    }
    api = util.get_api()
    documents = api.list_signed_documents(**kwargs)

    # filters the result set retrieved so that only the valid at
    # "submittable" documents are present in the sequence
    valid_documents = [
        value for value in documents if value["_class"] in util.AT_SUBMIT_TYPES
    ]

    # "calculates" the total set of valid documents present in the
    # valid documents and starts the index counter
    total = len(valid_documents)
    index = 1

    # iterates over the complete set of valid documents to be sent
    # (submitted) to at and processes the submission
    for document in valid_documents:
        type = document["_class"]
        object_id = document["object_id"]
        representation = document["representation"]
        issue_date = document["issue_date"]
        issue_date_d = datetime.datetime.utcfromtimestamp(issue_date)
        issue_date_s = issue_date_d.strftime("%d %b %Y %H:%M:%S")

        # retrieves the current time and uses it to print debug information
        # about the current document submission to at
        quorum.info(
            "Submitting %s - %s (%s) [%d/%d]"
            % (type, representation, issue_date_s, index, total)
        )

        try:
            # starts the submission process for the invoice, taking into
            # account that the document id to be submitted is the one that
            # has been extracted from the (signed) document structure
            api.submit_invoice_at(object_id)
        except Exception as exception:
            quorum.error(
                "Exception while submitting document - %s"
                % quorum.legacy.UNICODE(exception)
            )
        else:
            quorum.info("Document submitted with success")

        # increments the index counter, because one more document
        # as been processed (submitted or failed)
        index += 1

    return flask.redirect(
        flask.url_for("index", message="Signed documents have been sent to AT")
    )


@app.route("/oauth", methods=("GET",))
def oauth():
    # retrieves the reference to the current API object, so that
    # it may be used for the retrieval of the access token from
    # the currently received code value
    api = util.get_api()

    # retrieves the code value provided that is going to be used
    # to redeem the access token and the state value that is going
    # to be used as the next value for redirection (if defined)
    code = quorum.get_field("code", None)
    state = quorum.get_field("state", None)

    # tries to retrieve the error field an in case it exists raises
    # an error indicating the OAuth based problem
    error = quorum.get_field("error", None)
    error_description = quorum.get_field("error_description", None)
    if error:
        raise RuntimeError("%s - %s" % (error, error_description))

    # creates the access token URL for the API usage and sends the
    # appropriate attributes for the retrieval of the access token,
    # then stores it in the current session
    access_token = api.oauth_access(code)
    flask.session["omnix.access_token"] = access_token

    # ensures that a correct session value exists in session, creating
    # a new session in case that's required, this ensures that the acl
    # exists for the current user that is logging in
    api.oauth_session()

    return flask.redirect(state or flask.url_for("index"))


@app.route("/top", methods=("GET",))
@quorum.ensure("base.admin")
def top():
    year = quorum.get_field("year", None, cast=int)
    month = quorum.get_field("month", None, cast=int)

    (
        top_employees,
        target_s,
        previous_month,
        previous_year,
        next_month,
        next_year,
        has_next,
    ) = util.get_top(year=year, month=month)

    return flask.render_template(
        "top.html.tpl",
        link="top",
        title=target_s,
        top_employees=top_employees,
        previous=(previous_month, previous_year),
        next=(next_month, next_year),
        has_next=has_next,
    )


@app.errorhandler(404)
def handler_404(error):
    return flask.Response(
        flask.render_template("error.html.tpl", error="404 - Page not found"),
        status=404,
    )


@app.errorhandler(413)
def handler_413(error):
    return flask.Response(
        flask.render_template("error.html.tpl", error="412 - Precondition failed"),
        status=413,
    )


@app.errorhandler(Exception)
def handler_exception(error):
    formatted = traceback.format_exc()
    lines = formatted.splitlines() if quorum.is_devel() else []

    return flask.Response(
        flask.render_template("error.html.tpl", error=str(error), traceback=lines),
        status=500,
    )
