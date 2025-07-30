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

from . import base
from . import customer
from . import employee
from . import entity
from . import extra
from . import media
from . import report
from . import settings
from . import store
from . import supplier

from .base import (
    index,
    signin,
    login,
    do_login,
    logout,
    about,
    reset,
    flush_slack_sales,
    flush_slack_previous,
    flush_slack_week,
    flush_birthday,
    flush_activity,
    flush_at,
    oauth,
    top,
    handler_404,
    handler_413,
    handler_exception,
)
from .customer import list_customers, list_customers_json, show_customers
from .employee import (
    list_employees,
    list_employees_json,
    show_employee,
    sales_employee,
    mail_employee,
    show_employees,
    sales_employees,
    mail_employees,
)
from .entity import list_entities, list_entities_json, show_entities, edit_entities
from .extra import (
    list_extras,
    media_extras,
    do_media_extras,
    images_extras,
    do_images_extras,
    prices_extras,
    do_prices_extras,
    inventory_extras,
    do_inventory_extras,
    template_extras,
    do_template_extras,
    do_mask_extras,
    browser_extras,
    do_browser,
    new_media_browser,
    create_media_browser,
)
from .media import (
    list_media,
    list_media_json,
    show_media,
    edit_media,
    update_media,
    delete_media,
)
from .report import list_reports, sales_reports
from .settings import oauth_slack
from .store import list_stores, list_stores_json, show_stores, sales_stores
from .supplier import list_suppliers, list_suppliers_json, show_suppliers
