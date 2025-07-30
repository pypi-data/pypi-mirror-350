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

import os
import setuptools

setuptools.setup(
    name="omnix",
    version="0.3.7",
    author="Hive Solutions Lda.",
    author_email="development@hive.pt",
    description="Omnix System",
    license="Apache License, Version 2.0",
    keywords="omni extensions erp",
    url="http://omnix.hive.pt",
    zip_safe=False,
    packages=[
        "omnix",
        "omnix.models",
        "omnix.test",
        "omnix.test.util",
        "omnix.util",
        "omnix.views",
        "omnix.views.api",
        "omnix.views.web",
    ],
    test_suite="omnix.test",
    package_dir={"": os.path.normpath("src")},
    package_data={
        "omnix": [
            "static/css/*.css",
            "static/images/*.png",
            "static/images/email/*.png",
            "static/js/*.js",
            "templates/*.tpl",
            "templates/customer/*.tpl",
            "templates/email/*.tpl",
            "templates/employee/*.tpl",
            "templates/entity/*.tpl",
            "templates/extra/*.tpl",
            "templates/extra/browser/*.tpl",
            "templates/media/*.tpl",
            "templates/partials/*.tpl",
            "templates/report/*.tpl",
            "templates/store/*.tpl",
            "templates/supplier/*.tpl",
        ]
    },
    install_requires=[
        "netius",
        "flask",
        "quorum",
        "pillow",
        "pymongo",
        "redis",
        "pika",
        "xlrd",
        "omni-api",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    long_description=open(os.path.join(os.path.dirname(__file__), "README.md"), "rb")
    .read()
    .decode("utf-8"),
    long_description_content_type="text/markdown",
)
