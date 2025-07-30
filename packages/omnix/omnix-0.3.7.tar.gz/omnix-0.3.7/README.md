# [Omni (x)Extensions](http://omnix.hive.pt)

Simple web application consuming the Omni API.

This application may be used as a supervisor of the Omni Platform to run tasks in an async
fashion, this way it's possible to remove async tasks from the Omni core.

## Usage

One must define a series of configuration values in order to correctly use the automated
part of the omni extension (supervisor).

| Name                        | Type   | Default | Description                                                                                                                                               |
| --------------------------- | ------ | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **OMNIX_REMOTE**            | `bool` | `False` | If the remote URL should be used as the default one (legacy).                                                                                             |
| **OMNIX_USERNAME**          | `str`  | `None`  | The username to be used for authentication on the omni service.                                                                                           |
| **OMNIX_PASSWORD**          | `str`  | `None`  | The password value used in the authentication on the omni service, notice that this value will be sent in plain text (using an SSL encrypted connection). |
| **OMNIX_CLIENT_ID**         | `str`  | `None`  | The identifier of the Omni API client to be used for authentication.                                                                                      |
| **OMNIX_CLIENT_SECRET**     | `str`  | `None`  | The secret string to be used by the Omni API client for authentication.                                                                                   |
| **OMNIX_QUEUE**             | `str`  | `omnix` | The name of AMQP queue that is going to be used.                                                                                                          |
| **OMNIX_RECORD_CHUNK**      | `int`  | `300`   | The size of record chunk to be used by the scheduler (use carefully to avoid memory issues).                                                             |
| **OMNIX_BIRTHDAY_TEMPLATE** | `str`  | `None`  | If set allows for a remote definition of the base template to be used for email sending.                                                                  |
| **REMOTE**                  | `bool` | `False` | If the remove mode should be used (production URL creation).                                                                                              |
| **OMNIX_REMOTE**            | `bool` | `False` | Same as `REMOTE`.                                                                                                                                         |
| **OMNIX_SCHEDULE**          | `bool` | `True`  | If the scheduling (background) operations of the Omnix should be enabled (defaults to `True`).                                                            |
| **REDIRECT_URL**            | `str`  | `None`  | The URL that will be used for OAuth2 based callbacks.                                                                                                     |

Additionally one must also configure the MongoDB and RabbitMQ instances to be able to execute
the proper master and slave supervisors. For that use the `MONGOHQ_URL` and `CLOUDAMQP_URL` variables.

## License

Omnix is currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

## Build Automation

[![Build Status](https://app.travis-ci.com/hivesolutions/omnix.svg?branch=master)](https://travis-ci.com/github/hivesolutions/omnix)
[![Coverage Status](https://coveralls.io/repos/hivesolutions/omnix/badge.svg?branch=master)](https://coveralls.io/r/hivesolutions/omnix?branch=master)
[![PyPi Status](https://img.shields.io/pypi/v/omnix.svg)](https://pypi.python.org/pypi/omnix)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/)
