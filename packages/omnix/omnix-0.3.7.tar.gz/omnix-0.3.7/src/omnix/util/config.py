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

LOCAL_PREFIX = "omni_adm/"
""" The web prefix to be used when trying to access administration
related resources from a local perspective """

REMOTE_PREFIX = "adm/"
""" The web prefix to be used when trying to access administration
related resources from a remote perspective """

LOCAL_URL = "http://localhost:8080/mvc/"
""" The base URL to be used to compose the various
complete URL values for the various operations, this is
the local version of it used mostly for debugging """

REMOTE_URL = "https://omni.stage.hive.pt/"
""" The base URL to be used to compose the various
complete URL values for the various operations, this is
the remove version used in production environments """

REDIRECT_URL = "http://localhost:8181/oauth"
""" The redirect base URL to be used as the base value
for the construction of the base URL instances """

CLIENT_ID = "2a4dd8f8f649472dba4dfbbefdf7d623"
""" The id of the Omni client to be used, this value
is not considered to be secret and may be freely used """

CLIENT_SECRET = "b3ae4af4454945479592792ad970f8d7"
""" The secret key value to be used to access the
Omni API as the client, this value should not be shared
with every single person (keep private) """

FIRST_DAY = 1
""" The constant value that defines the first day of a month
this is obvious and should be used as a constant for readability """

SCOPE = (
    "base",
    "base.user",
    "base.admin",
    "foundation.media.list",
    "foundation.media.show",
    "foundation.media.update",
    "foundation.media.delete",
    "foundation.store.list",
    "foundation.store.show",
    "foundation.employee.list",
    "foundation.employee.show",
    "foundation.employee.show.self",
    "foundation.root_entity.list",
    "foundation.root_entity.show",
    "foundation.root_entity.update",
    "foundation.root_entity.show_media",
    "foundation.root_entity.set_media",
    "foundation.root_entity.clear_media",
    "foundation.supplier_company.list",
    "foundation.supplier_company.show",
    "foundation.system_company.show.self",
    "customers.customer_person.list",
    "customers.customer_person.show",
    "sales.customer_return.list",
    "sales.customer_return.list.self",
    "sales.sale_order.list",
    "sales.sale_transaction.list",
    "sales.sale_transaction.list.self",
    "documents.signed_document.list",
    "documents.signed_document.submit_invoice_at",
    "analytics.sale_snapshot.list",
    "analytics.employee_snapshot.list",
    "inventory.stock_adjustment.create",
    "inventory.transfer.create",
    "inventory.transactional_merchandise.list",
    "inventory.transactional_merchandise.update",
)
""" The list of permissions to be used to create the
scope string for the OAuth value """

DOCUMENT_INTERNAL = 1
""" The internal document type value, for documents that represent
internal actions of the system company """

DOCUMENT_INBOUND = 2
""" The outbound document type value, for documents that represent
actions coming from external entities to the system company """

DOCUMENT_OUTBOUND = 3
""" The outbound document type value, for documents that represent
actions going from the system company to external entities """

AT_SUBMIT_DOCUMENTS = (DOCUMENT_INTERNAL, DOCUMENT_OUTBOUND)
""" The multiple document types that are considered to be valid
for AT submission """

AT_SALE_TYPES = ("MoneySaleSlip", "Invoice", "CreditNote", "DebitNote")
""" The list containing the complete set of types that
are considered to be of type sale """

AT_TRANSPORT_TYPES = ("TransportationSlip", "ExpeditionSlip")
""" The list containing the complete set of types that
are considered to be of type transport """

AT_SUBMIT_TYPES = AT_SALE_TYPES + AT_TRANSPORT_TYPES
""" The set of valid types for submission to AT, note
that this range of values should be changed with care """

AT_SALE_DIGEST_TYPES = ("FS", "FT", "NC", "ND")
""" The list containing the complete set of digest types that
are considered to be of type sale """

AT_TRANSPORT_DIGEST_TYPES = ("GT", "GR")
""" The list containing the complete set of digest types that
are considered to be of type transport """

AT_SUBMIT_DIGEST_TYPES = AT_SALE_DIGEST_TYPES + AT_TRANSPORT_DIGEST_TYPES
""" The set of valid digest types for submission to AT, note
that this range of values should be changed with care """

REMOTE = quorum.conf("REMOTE", False, cast=bool)
REMOTE = quorum.conf("OMNIX_REMOTE", REMOTE, cast=bool)
BASE_URL = quorum.conf("BASE_URL", "http://localhost:8181")
REDIRECT_URL = quorum.conf("REDIRECT_URL", REDIRECT_URL)
CLIENT_ID = quorum.conf("OMNIX_CLIENT_ID", CLIENT_ID)
CLIENT_SECRET = quorum.conf("OMNIX_CLIENT_SECRET", CLIENT_SECRET)
SENDER_EMAIL = quorum.conf("SENDER_EMAIL", "Omnix <no-reply@omnix.com>")
USERNAME = quorum.conf("OMNIX_USERNAME", None)
PASSWORD = quorum.conf("OMNIX_PASSWORD", None)
SCHEDULE = quorum.conf("OMNIX_SCHEDULE", True, cast=bool)
COMMISSION_RATE = quorum.conf("OMNIX_COMMISSION_RATE", 0.01, cast=float)
COMMISSION_DAY = quorum.conf("OMNIX_COMMISSION_DAY", 26, cast=int)
IMAGE_RESIZE = quorum.conf("OMNIX_IMAGE_RESIZE", "crop")
LOCALE = quorum.conf("OMNIX_LOCALE", "en_us")
QUEUE = quorum.conf("OMNIX_QUEUE", "omnix")
RECORD_CHUNK = quorum.conf("OMNIX_RECORD_CHUNK", 256, cast=int)
BIRTHDAY_TEMPLATE = quorum.conf(
    "OMNIX_BIRTHDAY_TEMPLATE", "email/birthday.%s.html.tpl" % LOCALE
)

OMNI_URL = REMOTE_URL if REMOTE else LOCAL_URL
PREFIX = REMOTE_PREFIX if REMOTE else LOCAL_PREFIX

OMNI_URL = quorum.conf("OMNI_URL", OMNI_URL)
PREFIX = quorum.conf("OMNI_PREFIX", PREFIX)
