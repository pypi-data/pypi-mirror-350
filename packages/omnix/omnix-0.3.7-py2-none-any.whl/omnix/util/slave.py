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
import time
import datetime
import threading

import omni
import quorum

from . import logic
from . import config

LOOP_TIMEOUT = 120
""" The time to be used in between reading new
messages from the Omni service, this will only be
used in case there's a problem in the client
connection with the queueing service """

MESSAGE_TIMEOUT = 120
""" The amount of seconds before a message is
considered out dated and is discarded from the
queue even without processing """

RETRY_TIMEOUT = 30
""" The timeout to be used in between the retries
of the operations, as expected """


class Slave(threading.Thread):

    session_id = None
    connection = None
    channel = None

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

    def stop(self):
        pass

    def auth(self):
        if not config.REMOTE:
            return

        username = config.USERNAME
        password = config.PASSWORD
        if username == None or password == None:
            raise RuntimeError("Missing authentication information")

        self.api = logic.get_api(mode=omni.API.DIRECT_MODE)

    def connect(self, queue="default"):
        if not config.REMOTE:
            return

        while True:
            try:
                quorum.debug("Starting loop cycle in slave ...")
                self.connection = quorum.get_amqp(force=True)
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue=queue, durable=True)
                self.channel.basic_qos(prefetch_count=1)
                self.channel.basic_consume(
                    queue=queue, on_message_callback=self.callback
                )
                self.channel.start_consuming()
            except Exception as exception:
                quorum.error(
                    "Exception while executing - %s" % quorum.legacy.UNICODE(exception),
                    log_trace=True,
                )

            quorum.info("Sleeping %d seconds before consume retry" % RETRY_TIMEOUT)

            time.sleep(RETRY_TIMEOUT)

    def disconnect(self):
        if not config.REMOTE:
            return

    def callback(self, channel, method, properties, body):
        # prints a debug message about the callback call for the message, this
        # may be used latter for debugging purposes (as requested)
        quorum.debug("Received callback for message")

        # loads the contents of the body that is going to be submitted this
        # is considered the payload of the document to be submitted
        document = json.loads(body)

        # retrieves the various attributes of the document that is going to
        # be submitted, making sure that the issue date is correctly formatted
        type = document["_class"]
        object_id = document["object_id"]
        representation = document["representation"]
        issue_date = document["issue_date"]
        issue_date_d = datetime.datetime.utcfromtimestamp(issue_date)
        issue_date_s = issue_date_d.strftime("%d %b %Y %H:%M:%S")

        # verifies if the document is considered to be outdated (timeout passed)
        # in case it's returns immediately printing a message
        outdated = (
            not properties.timestamp
            or properties.timestamp < time.time() - MESSAGE_TIMEOUT
        )
        if outdated:
            channel.basic_ack(delivery_tag=method.delivery_tag)
            quorum.info(
                "Canceling/Dropping %s - %s (%s)" % (type, representation, issue_date_s)
            )
            return

        # retrieves the current time and uses it to print debug information
        # about the current document submission to at
        quorum.info("Submitting %s - %s (%s)" % (type, representation, issue_date_s))

        # resolves the method for the currently retrieved data type (class)
        # this should raise an exception in case the type is invalid
        api_method = self._resolve_method(type)

        try:
            # calls the proper method for the submission of the document
            # described by the provided object id, in case there's a problem
            # in the request an exception should be raised and handled properly
            api_method(object_id)
        except Exception as exception:
            quorum.error(
                "Exception while submitting document - %s"
                % quorum.legacy.UNICODE(exception)
            )
            retries = properties.priority or 0
            retries -= 1
            properties.priority = retries
            if retries >= 0:
                self.channel.basic_publish(
                    exchange="",
                    routing_key=config.QUEUE,
                    body=body,
                    properties=properties,
                )
                quorum.error(
                    "Re-queueing for latter consumption (%d retries pending)" % retries
                )
            else:
                quorum.error("No more retries left, the document will be discarded")
        else:
            quorum.info("Document submitted with success")

        # marks the message as acknowledged in the message queue server
        # and then prints a debug message about the action
        channel.basic_ack(delivery_tag=method.delivery_tag)
        quorum.debug("Marked as acknowledged in message queue")

    def run(self):
        self.auth()
        self.connect(queue=config.QUEUE)
        self.disconnect()

    def _resolve_method(self, type):
        if type in config.AT_SALE_TYPES:
            return self.api.submit_invoice_at
        elif type in config.AT_TRANSPORT_TYPES:
            return self.api.submit_transport_at
        else:
            raise RuntimeError("Invalid document type")


def run(count=1):
    for _index in range(count):
        slave = Slave()
        slave.start()
