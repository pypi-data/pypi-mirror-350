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

__copyright__ = "Copyright (c) 2008-2025 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

from . import business
from . import config
from . import ctt
from . import format
from . import image
from . import logic
from . import scheduling
from . import slave
from . import supervisor

from .business import (
    slack_sales,
    slack_previous,
    slack_week,
    mail_birthday_all,
    mail_activity_all,
    mail_birthday,
    mail_activity,
    get_date,
    get_top,
    get_sales,
    get_comparison,
    sum_results,
    calc_comparison,
    calc_extra,
    calc_results,
)
from .ctt import encode_ctt
from .format import csv_file, csv_import, csv_value
from .config import (
    LOCAL_PREFIX,
    REMOTE_PREFIX,
    LOCAL_URL,
    REMOTE_URL,
    REDIRECT_URL,
    CLIENT_ID,
    CLIENT_SECRET,
    FIRST_DAY,
    SCOPE,
    DOCUMENT_INTERNAL,
    DOCUMENT_INBOUND,
    DOCUMENT_OUTBOUND,
    AT_SUBMIT_DOCUMENTS,
    AT_SALE_TYPES,
    AT_TRANSPORT_TYPES,
    AT_SUBMIT_TYPES,
    AT_SALE_DIGEST_TYPES,
    AT_TRANSPORT_DIGEST_TYPES,
    AT_SUBMIT_DIGEST_TYPES,
    REMOTE,
    BASE_URL,
    SENDER_EMAIL,
    USERNAME,
    PASSWORD,
    SCHEDULE,
    COMMISSION_RATE,
    COMMISSION_DAY,
    IMAGE_RESIZE,
    LOCALE,
    QUEUE,
    RECORD_CHUNK,
    BIRTHDAY_TEMPLATE,
    OMNI_URL,
    PREFIX,
)
from .image import mask_image
from .logic import (
    get_models,
    get_api,
    ensure_api,
    on_auth,
    start_session,
    reset_session,
    get_tokens,
)

from .scheduling import load as load_scheduling
from .slave import run as run_slave
from .supervisor import run as run_supervisor
