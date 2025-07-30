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
import json
import threading

import omni
import quorum

from . import logic
from . import config

LOOP_TIMEOUT = 120
""" The time to be used in between queueing new
messages from the Omni service """

MESSAGE_TIMEOUT = 120
""" The amount of seconds before a message is
considered out dated and is discarded from the
queue even without processing """

RETRY_TIMEOUT = 30
""" The timeout to be used in between the retries
of the operations, as expected """

MESSAGE_RETRIES = 3
""" The number of retries to be used for the message
before it's considered discarded """

NUMBER_RECORDS = config.RECORD_CHUNK
""" The maximum number of records that is going to be
retrieved and set for submission, this value influences
the performance, mostly under heavy load situations """


class Supervisor(threading.Thread):

    session_id = None
    connection = None
    channel = None
    queue = None

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

    def connect(self, queue="default", retry=True):
        if not config.REMOTE:
            return

        quorum.info("Connecting to the AMQP system")

        while True:
            try:
                self.connection = quorum.get_amqp(force=True)
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue=queue, durable=True)
                self.queue = queue
                break
            except Exception as exception:
                if not retry:
                    raise
                quorum.error(
                    "Exception while connecting - %s"
                    % quorum.legacy.UNICODE(exception),
                    log_trace=True,
                )
                quorum.info("Sleeping %d seconds before connect retry" % RETRY_TIMEOUT)
                time.sleep(RETRY_TIMEOUT)

    def disconnect(self):
        if not config.REMOTE:
            return

        quorum.info("Disconnected from the AMQP system")

        self.connection.close()

    def reconnect(self, retry=True):
        if not config.REMOTE:
            return
        if not self.connection.is_closed:
            return

        quorum.info("Re-connecting to the AMQP system")

        self.connect(queue=self.queue, retry=retry)

    def execute(self):
        # in case the current instance is not configured according to
        # the remote rules the queuing operation is ignored, and so
        # the control flow returns immediately
        if not config.REMOTE:
            return

        # creates a values map structure to retrieve the complete
        # set of inbound documents that have not yet been submitted
        # to at for the flush operation
        kwargs = {
            "session_id": self.session_id,
            "filter_string": "",
            "start_record": 0,
            "number_records": NUMBER_RECORDS,
            "sort": "issue_date:ascending",
            "filters[]": [
                "issue_date:greater:1356998400",
                "submitted_at:equals:2",
                "document_type:in:%s"
                % ";".join(str(v) for v in config.AT_SUBMIT_DOCUMENTS),
                "digest_document_type:in:%s" % ";".join(config.AT_SUBMIT_DIGEST_TYPES),
            ],
        }
        documents = self.api.list_signed_documents(**kwargs)
        valid_documents = [
            value for value in documents if value["_class"] in config.AT_SUBMIT_TYPES
        ]

        # starts the counter value to zero, so that we're able to count
        # the number of messages that have been successfully queued to
        # the remote queueing mechanism (for debugging)
        count = 0

        # prints a debug message about the number of valid documents that
        # have been found for submission to the queue
        quorum.debug(
            "Found %d (out of %d) valid documents for submission"
            % (len(valid_documents), len(documents))
        )

        # iterates over all the valid documents that have been found
        # as not submitted and creates a task for their submission
        # then adds the task to the AMQP queue to be processed
        for document in valid_documents:
            try:
                # tries to run the basic publish operation, this operation
                # may fail for a variety of reasons including errors in the
                # underlying library so a reconnection is attempted in case
                # there's an exception raised under this operation
                self.channel.basic_publish(
                    exchange="",
                    routing_key=config.QUEUE,
                    body=json.dumps(document),
                    properties=quorum.properties_amqp(
                        delivery_mode=2,
                        priority=MESSAGE_RETRIES,
                        expiration=str(MESSAGE_TIMEOUT * 1000),
                        timestamp=time.time(),
                    ),
                )
                count += 1
            except Exception as exception:
                # prints a warning message about the exception that has just occurred
                # so that it's possible to act on it
                quorum.warning(
                    "Exception in publish (will re-connect) - %s"
                    % quorum.legacy.UNICODE(exception),
                    log_trace=True,
                )

                # re-tries to connect with the AMQP channels using the currently
                # pre-defined queue system, this is a fallback of the error
                self.reconnect()

        # prints an information message about the new documents that
        # have been queued for submission by the "slaves"
        quorum.info(
            "Queued %d (out of %d) documents for submission"
            % (count, len(valid_documents))
        )

    def loop(self):
        while True:
            try:
                self.execute()
            except Exception as exception:
                # prints an error message about the exception that has just occurred
                # so that it's possible to act on it
                quorum.error(
                    "Exception while executing - %s" % quorum.legacy.UNICODE(exception),
                    log_trace=True,
                )

                # re-tries to connect with the AMQP channels using the currently
                # pre-defined queue system, this is a fallback of the error
                self.reconnect()

            try:
                if self.connection:
                    self.connection.sleep(LOOP_TIMEOUT)
                else:
                    time.sleep(LOOP_TIMEOUT)
            except Exception as exception:
                # prints a critical message about the exception that has just occurred
                # so that it's possible to act on it
                quorum.critical(
                    "Exception while sleeping - %s" % quorum.legacy.UNICODE(exception),
                    log_trace=True,
                )

                # re-tries to connect with the AMQP channels using the currently
                # pre-defined queue system, this is a fallback of the error
                self.reconnect()

    def run(self):
        self.auth()
        self.connect(queue=config.QUEUE)
        try:
            self.loop()
        finally:
            self.disconnect()


def run(count=1):
    for _index in range(count):
        supervisor = Supervisor()
        supervisor.start()
