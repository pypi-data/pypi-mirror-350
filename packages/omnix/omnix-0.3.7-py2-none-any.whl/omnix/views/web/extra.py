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
import imghdr
import shutil
import zipfile
import tempfile
import mimetypes

from omnix import util

from omnix.main import app
from omnix.main import flask
from omnix.main import quorum


@app.route("/extras", methods=("GET",))
@quorum.ensure("base.user")
def list_extras():
    return flask.render_template("extra/list.html.tpl", link="extras")


@app.route("/extras/media", methods=("GET",))
@quorum.ensure("foundation.root_entity.set_media")
def media_extras():
    return flask.render_template("extra/media.html.tpl", link="extras")


@app.route("/extras/media", methods=("POST",))
@quorum.ensure("inventory.transactional_merchandise.update")
def do_media_extras():
    # retrieves the reference to the (Omni) API object that
    # is going to be used for the operations of updating of
    # the merchandise in bulk (multiple operations at a time)
    api = util.get_api()

    # tries to retrieve the media file from the current
    # form in case it's not available renders the current
    # template with an error message
    media_file = quorum.get_field("media_file", None)
    if media_file == None or not media_file.filename:
        return flask.render_template(
            "extra/media.html.tpl", link="extras", error="No file defined"
        )

    # creates a temporary file path for the storage of the file
    # and then saves it into that directory, closing the same
    # file afterwards, as it has been properly saved
    fd, file_path = tempfile.mkstemp()
    try:
        media_file.save(file_path)
    finally:
        media_file.close()

    try:
        # creates a new temporary directory that is going to be used
        # in the extraction of the media zip file
        temp_path = tempfile.mkdtemp()
        try:
            # creates the zip file reference with the current file path
            # and then extracts the complete set of contents to the "target"
            # temporary path closing the zip file afterwards
            zip = zipfile.ZipFile(file_path)
            try:
                zip.extractall(temp_path)
            finally:
                zip.close()

            # iterates over the complete set of names in the temporary path
            # to try to upload the media to the target data source, note that
            # only the media files are considered and the base name of them
            # are going to be validation for existence in the data source
            for name in os.listdir(temp_path):
                # splits the file name into base name and extension and validates
                # the extension, so that only media files are considered
                base, extension = os.path.splitext(name)
                if not extension.lower() in (".png", ".jpg", ".jpeg"):
                    quorum.info("Skipping, '%s' not a valid media file" % name)
                    continue

                # splits the base value of the file name so that it's possible to
                # extract the proper position of the image if that's required
                base_s = base.rsplit("_", 1)
                if len(base_s) > 1:
                    position = int(base_s[1])
                else:
                    position = 1

                # tries to "cast" the base file name value as an integer and in case
                # it's possible assumes that this value is the object identifier
                try:
                    object_id = int(base_s[0])
                except Exception:
                    object_id = None

                # in case no object id was retrieved from the base file name value
                # a secondary strategy is used, so that the merchandise database
                # is searched using the base string value as the company product code
                if not object_id:
                    # creates the keyword arguments map so that the the merchandise
                    # with the provided company product code is retrieved
                    kwargs = {
                        "start_record": 0,
                        "number_records": 1,
                        "filters[]": ["company_product_code:equals:%s" % base_s[0]],
                    }

                    # runs the list merchandise operation in order to try to find a
                    # merchandise entity for the requested (unique) product code in
                    # case there's at least one merchandise its object id is used
                    try:
                        merchandise = api.list_merchandise(**kwargs)
                    except Exception:
                        merchandise = []
                    if merchandise:
                        object_id = merchandise[0]["object_id"]

                # in case no object id was retrieved must skip the current loop
                # with a proper information message (as expected)
                if not object_id:
                    quorum.info(
                        "Skipping, could not resolve Object ID id for '%s'" % base
                    )
                    continue

                # prints a logging message about the upload of media file that
                # is going to be performed for the current entity
                quorum.debug(
                    "Adding media file for entity '%d' in position '%d'"
                    % (object_id, position)
                )

                # creates the target temporary media path from the temporary directory
                # path and then "read" the complete set of contents from it closing the
                # file afterwards (no more reading allowed)
                media_path = os.path.join(temp_path, name)
                media_file = open(media_path, "rb")
                try:
                    contents = media_file.read()
                finally:
                    media_file.close()

                # tries to guess the proper image type for the image located at the
                # provided path and the uses this value to construct the mime type
                image_type = imghdr.what(media_path)
                mime_type = "image/" + image_type if image_type else "image/unknown"

                # sets/updates the media for the associated root entity using the
                # data extracted from the file and the information in its name
                api.set_media_entity(
                    object_id,
                    contents,
                    position=position,
                    mime_type=mime_type,
                    engine="fs",
                    thumbnails=True,
                )
        finally:
            # removes the temporary path as it's no longer going to be
            # required for the operation (errors are ignored)
            shutil.rmtree(temp_path, ignore_errors=True)
    finally:
        # closes the temporary file descriptor and removes the temporary
        # file (avoiding any memory leaks)
        os.close(fd)
        os.remove(file_path)

    # redirects the user back to the media list page with a success
    # message indicating that everything went as expected
    return flask.redirect(
        flask.url_for("media_extras", message="Media file processed with success")
    )


@app.route("/extras/images", methods=("GET",))
@quorum.ensure("inventory.transactional_merchandise.update")
def images_extras():
    return flask.render_template("extra/images.html.tpl", link="extras")


@app.route("/extras/images", methods=("POST",))
@quorum.ensure("inventory.transactional_merchandise.update")
def do_images_extras():
    # retrieves the reference to the (Omni) API object that
    # is going to be used for the operations of updating of
    # the merchandise in bulk (multiple operations at a time)
    api = util.get_api()

    # tries to retrieve the images file from the current
    # form in case it's not available renders the current
    # template with an error message
    images_file = quorum.get_field("images_file", None)
    if images_file == None or not images_file.filename:
        return flask.render_template(
            "extra/images.html.tpl", link="extras", error="No file defined"
        )

    # creates a temporary file path for the storage of the file
    # and then saves it into that directory, closing the same
    # file afterwards, as it has been properly saved
    fd, file_path = tempfile.mkstemp()
    try:
        images_file.save(file_path)
    finally:
        images_file.close()

    try:
        # creates a new temporary directory that is going to be used
        # in the extraction of the images zip file
        temp_path = tempfile.mkdtemp()
        try:
            # creates the zip file reference with the current file path
            # and then extracts the complete set of contents to the "target"
            # temporary path closing the zip file afterwards
            zip = zipfile.ZipFile(file_path)
            try:
                zip.extractall(temp_path)
            finally:
                zip.close()

            # iterates over the complete set of names in the temporary path
            # to try to upload the image to the target data source, note that
            # only the image files are considered and the base name of them
            # are going to be validation for existence in the data source
            for name in os.listdir(temp_path):
                # splits the file name into base name and extension and validates
                # the extension, so that only image files are considered
                base, extension = os.path.splitext(name)
                if not extension.lower() in (".png", ".jpg", ".jpeg"):
                    quorum.info("Skipping, '%s' not a valid image file" % name)
                    continue

                # creates the keyword arguments map so that the the merchandise
                # with the provided company product code is retrieved
                kwargs = {
                    "start_record": 0,
                    "number_records": 1,
                    "filters[]": ["company_product_code:equals:%s" % base],
                }

                # creates the URL for the merchandise retrieval and runs the get
                # operation with the provided filter so that the target merchandise
                # is retrieved for object id validation
                merchandise = api.list_merchandise(**kwargs)

                # verifies that at least one entity was retrieved in case nothing
                # is found skips the current loop with a not found error
                if not merchandise:
                    quorum.info("Skipping, '%s' not found in data source" % base)
                    continue

                # prints a logging message about the upload of image file that
                # is going to be performed for the current merchandise
                quorum.debug("Changing image file for merchandise '%s'" % base)

                # retrieves the first entity from the resulting list and then retrieves
                # the object identifier from it to be used in the update operation
                entity = merchandise[0]
                object_id = entity["object_id"]

                # creates the target temporary image path from the temporary directory
                # path and then "read" the complete set of contents from it closing the
                # file afterwards (no more reading allowed)
                image_path = os.path.join(temp_path, name)
                image_file = open(image_path, "rb")
                try:
                    contents = image_file.read()
                finally:
                    image_file.close()

                # creates the image (file) tuple with both the name of the file and the
                # contents if it (multipart standard)
                image_tuple = (name, contents)

                # creates the multipart data map with both the object id and the image
                # file parameters that are going to be used in the encoding
                data_m = {
                    "object_id": object_id,
                    "transactional_merchandise[_parameters][image_file]": image_tuple,
                }

                # uses the "resolved" items structure in the operation to
                # the Omni API so that the images for them get updated
                api.update_merchandise(object_id, data_m)
        finally:
            # removes the temporary path as it's no longer going to be
            # required for the operation (errors are ignored)
            shutil.rmtree(temp_path, ignore_errors=True)
    finally:
        # closes the temporary file descriptor and removes the temporary
        # file (avoiding any memory leaks)
        os.close(fd)
        os.remove(file_path)

    # redirects the user back to the images list page with a success
    # message indicating that everything went as expected
    return flask.redirect(
        flask.url_for("images_extras", message="Images file processed with success")
    )


@app.route("/extras/metadata", methods=("GET",))
@quorum.ensure("foundation.root_entity.update")
def metadata_extras():
    return flask.render_template("extra/metadata.html.tpl", link="extras")


@app.route("/extras/metadata", methods=("POST",))
@quorum.ensure("foundation.root_entity.update")
def do_metadata_extras():
    # retrieves the reference to the API object that is going
    # to be used for the updating of prices operation
    api = util.get_api()

    # tries to retrieve the metadata file from the current
    # form in case it's not available renders the current
    # template with an error message
    metadata_file = quorum.get_field("metadata_file", None)
    if metadata_file == None or not metadata_file.filename:
        return flask.render_template(
            "extra/metadata.html.tpl", link="extras", error="No file defined"
        )

    # retrieves the value of the custom field that control if
    # the importing will be performed using a dynamic approach
    # meaning that no static values will be retrieved and instead
    # the header will be used for dynamic retrieval
    custom = quorum.get_field("custom", False, cast=bool)

    # check if the CSV file to uploaded is separated by the comma
    # character or if instead it used the semicolon
    comma = quorum.get_field("comma", False, cast=bool)

    # creates a temporary file path for the storage of the file
    # and then saves it into that directory
    fd, file_path = tempfile.mkstemp()
    metadata_file.save(file_path)

    # creates the file object that is going to be used in the
    # reading of the CSV file (underlying object)
    file = open(file_path, "rb")
    try:
        data = file.read()
    finally:
        file.close()

    # constructs the bytes based buffer object from the data that
    # has just been loaded from the file
    buffer = quorum.legacy.BytesIO(data)

    def callback(line, header=None):
        # in case the custom metadata mode is enabled then a special work
        # model is set where all of the columns are going to be used dynamically
        # for the update of the metadata map of the object
        if custom:
            # creates a zip of tuples with the header to line value association
            # and uses them to build a proper dictionary
            zipped = zip(header, line)
            update = dict(zipped)

            # iterates over the complete set of items in the map of values
            # and updates the update map with the sanitized value
            for name, value in update.items():
                update[name] = value.strip()

            # tries to retrieve the base identifier of the entity
            # this value is going to be used as the basis for identification
            base = update.pop("code", None)
            base = update.pop("company_product_code", base)
            base = update.pop("object_id", base)
            base = update.pop("base", base)

            # tries to retrieve some of the base entity values
            # if their found they are properly popped out
            name = update.pop("name", None)
            description = update.pop("description", None)
            upc = update.pop("upc", None)
            ean = update.pop("ean", None)

        # otherwise this is a "normal" update and the "typical" metadata
        # fields are the one to be updated
        else:
            # unpacks the current "metadata" line into its components as
            # expected by the specification
            (
                base,
                name,
                _retail_price,
                compare_price,
                discount,
                characteristics,
                material,
                category,
                collection,
                brand,
                season,
                gender,
                description,
                order,
                discountable,
                orderable,
                sku_field,
                upc,
                ean,
            ) = line[:19]

            # verifies if the initials part of the CSV line exists and
            # if that's the case processes it properly
            if len(line) >= 22:
                initials, initials_min, initials_max = line[19:22]
            else:
                initials, initials_min, initials_max = "", "", ""

            # normalizes the various values that have been extracted from the line
            # so they are properly represented for importing
            name = name or None
            compare_price = (compare_price and compare_price.strip()) or None
            discount = (discount and discount.strip()) or None
            characteristics = [
                value.strip() for value in characteristics.split(";") if value.strip()
            ]
            material = [value.strip() for value in material.split(";") if value.strip()]
            category = [value.strip() for value in category.split(";") if value.strip()]
            collection = [
                value.strip() for value in collection.split(";") if value.strip()
            ]
            brand = brand or None
            season = season or None
            gender = gender or None
            description = description or None
            order = (order and order.strip()) or None
            discountable = discountable or None
            orderable = orderable or None
            sku_field = sku_field or None
            upc = upc or None
            ean = ean or None
            initials = initials or None
            initials_min = initials_min or None
            initials_max = initials_max or None

            # verifies and strips the various possible string values so that they
            # represent a valid not trailed value
            if name:
                name = name.strip()
            if compare_price:
                compare_price = float(compare_price)
            if brand:
                brand = brand.strip()
            if season:
                season = season.strip()
            if gender:
                gender = gender.strip()
            if description:
                description = description.strip()
            if order:
                order = int(order)
            if discountable:
                discountable = discountable == "1"
            if orderable:
                orderable = orderable == "1"
            if sku_field:
                sku_field = sku_field.strip()
            if discount:
                discount = float(discount)
            if upc:
                upc = upc.strip()
            if ean:
                ean = ean.strip()
            if initials:
                initials = initials == "1"
            if initials_min:
                initials_min = int(initials_min)
            if initials_max:
                initials_max = int(initials_max)

            # creates the map that is going to hold the complete set of features
            # and populates the features according to their existence
            features = dict()
            if initials:
                features["initials"] = dict(min=initials_min, max=initials_max)

            # creates the update dictionary that is going to be used in the updating
            # of the "product" metadata (this is considered to be a delta dictionary)
            update = dict(
                compare_price=compare_price,
                discount=discount,
                characteristics=characteristics,
                features=features,
                material=material,
                category=category,
                collection=collection,
                brand=brand,
                season=season,
                gender=gender,
                order=order,
                discountable=discountable,
                orderable=orderable,
                sku_field=sku_field,
            )

        # tries to "cast" the base value as an integer and in case
        # it's possible assumes that this value is the object identifier
        try:
            object_id = int(base)
        except Exception:
            object_id = None

        # in case no object id was retrieved from the base name value
        # a secondary strategy is used, so that the merchandise database
        # is searched using the base string value as the company product code
        if not object_id:
            # creates the keyword arguments map so that the the merchandise
            # with the provided company product code is retrieved
            kwargs = {
                "start_record": 0,
                "number_records": 1,
                "filters[]": ["company_product_code:equals:%s" % base],
            }

            # runs the list merchandise operation in order to try to find a
            # merchandise entity for the requested (unique) product code in
            # case there's at least one merchandise its object id is used
            try:
                merchandise = api.list_merchandise(**kwargs)
            except Exception:
                merchandise = []
            if merchandise:
                object_id = merchandise[0]["object_id"]

        # in case no object id was retrieved must skip the current loop
        # with a proper information message (as expected)
        if not object_id:
            quorum.info("Skipping, could not resolve Object ID for '%s'" % base)
            return

        # prints a logging message about the updating of the metadata for
        # the entity with the current object id
        quorum.debug("Setting metadata for entity '%d'" % object_id)

        # retrieves the reference to the entity so that it's possible to
        # retrieve the currently defined metadata for it (to be updated)
        entity = api.get_entity(object_id)
        metadata = entity.get("metadata", {}) or {}

        # updates the metadata dictionary with the new values that are going
        # to be used for the updating of the entity, note that the previous
        # metadata values are leveraged and not overwritten with this strategy
        metadata.update(update)

        # creates the model structure to be updated and then runs the
        # proper execution of the metadata import
        model = dict(metadata=metadata)
        if name:
            model["name"] = name
        if description:
            model["description"] = description
        if upc:
            model["upc"] = upc
        if ean:
            model["ean"] = ean
        api.update_entity(object_id, payload=dict(root_entity=model))

    try:
        # start the CSV import operation that is going to import the
        # various lines of the CSV in the buffer and for each of them
        # call the function passed as callback
        util.csv_import(
            buffer, callback, header=True, delimiter="," if comma else ";", quoting=True
        )
    finally:
        # closes the temporary file descriptor and removes the temporary
        # file (avoiding any memory leaks)
        os.close(fd)
        os.remove(file_path)

    # redirects the user back to the metadata list page with a success
    # message indicating that everything went ok
    return flask.redirect(
        flask.url_for("metadata_extras", message="Metadata file processed with success")
    )


@app.route("/extras/prices", methods=("GET",))
@quorum.ensure("inventory.transactional_merchandise.update")
def prices_extras():
    return flask.render_template("extra/prices.html.tpl", link="extras")


@app.route("/extras/prices", methods=("POST",))
@quorum.ensure("inventory.transactional_merchandise.update")
def do_prices_extras():
    # retrieves the reference to the API object that is going
    # to be used for the updating of prices operation
    api = util.get_api()

    # tries to retrieve the prices file from the current
    # form in case it's not available renders the current
    # template with an error message
    prices_file = quorum.get_field("prices_file", None)
    if prices_file == None or not prices_file.filename:
        return flask.render_template(
            "extra/prices.html.tpl", link="extras", error="No file defined"
        )

    # creates a temporary file path for the storage of the file
    # and then saves it into that directory
    fd, file_path = tempfile.mkstemp()
    prices_file.save(file_path)

    try:
        # parses the temporary file containing the spreadsheet according
        # to the provided set of keys (to create the correct structures)
        items = quorum.xlsx_to_map(
            file_path,
            keys=("company_product_code", "retail_price"),
            types=(quorum.legacy.UNICODE, None),
        )
    finally:
        # closes the temporary file descriptor and removes the temporary
        # file (avoiding any memory leaks)
        os.close(fd)
        os.remove(file_path)

    # iterates over the complete set of items to make sure that they
    # all comply with the expected structure
    for index, item in enumerate(items):
        quorum.verify(
            item["company_product_code"],
            message="No key for value at index %d, please verify" % index,
        )
        quorum.verify(
            not item["retail_price"] in (None, ""),
            message="No retail price for code '%s', please verify"
            % item["company_product_code"],
        )

    # uses the "resolved" items structure in the put operation to
    # the Omni API so that the prices for them get updated
    api.prices_merchandise(items)

    # redirects the user back to the prices list page with a success
    # message indicating that everything went ok
    return flask.redirect(
        flask.url_for("prices_extras", message="Prices file processed with success")
    )


@app.route("/extras/costs", methods=("GET",))
@quorum.ensure("inventory.transactional_merchandise.update")
def costs_extras():
    return flask.render_template("extra/costs.html.tpl", link="extras")


@app.route("/extras/costs", methods=("POST",))
@quorum.ensure("inventory.transactional_merchandise.update")
def do_costs_extras():
    # retrieves the reference to the API object that is going
    # to be used for the updating of costs operation
    api = util.get_api()

    # tries to retrieve the costs file from the current
    # form in case it's not available renders the current
    # template with an error message
    costs_file = quorum.get_field("costs_file", None)
    if costs_file == None or not costs_file.filename:
        return flask.render_template(
            "extra/costs.html.tpl", link="extras", error="No file defined"
        )

    # creates a temporary file path for the storage of the file
    # and then saves it into that directory
    fd, file_path = tempfile.mkstemp()
    costs_file.save(file_path)

    try:
        # parses the temporary file containing the spreadsheet according
        # to the provided set of keys (to create the correct structures)
        items = quorum.xlsx_to_map(
            file_path,
            keys=("company_product_code", "cost"),
            types=(quorum.legacy.UNICODE, None),
        )
    finally:
        # closes the temporary file descriptor and removes the temporary
        # file (avoiding any memory leaks)
        os.close(fd)
        os.remove(file_path)

    # iterates over the complete set of items to make sure that they
    # all comply with the expected structure
    for index, item in enumerate(items):
        quorum.verify(
            item["company_product_code"],
            message="No key for value at index %d, please verify" % index,
        )
        quorum.verify(
            not item["cost"] in (None, ""),
            message="No cost value for code '%s', please verify"
            % item["company_product_code"],
        )

    # uses the "resolved" items structure in the put operation to
    # the Omni API so that the costs for them get updated
    api.costs_merchandise(items)

    # redirects the user back to the costs list page with a success
    # message indicating that everything went ok
    return flask.redirect(
        flask.url_for("costs_extras", message="Costs file processed with success")
    )


@app.route("/extras/inventory", methods=("GET",))
@quorum.ensure(
    (
        "inventory.stock_adjustment.create",
        "inventory.transactional_merchandise.list",
        "foundation.store.list",
    )
)
def inventory_extras():
    return flask.render_template("extra/inventory.html.tpl", link="extras")


@app.route("/extras/inventory", methods=("POST",))
@quorum.ensure(
    (
        "inventory.stock_adjustment.create",
        "inventory.transactional_merchandise.list",
        "foundation.store.list",
    )
)
def do_inventory_extras():
    # retrieves the reference to the API object that is going
    # to be used for the updating of prices operation
    api = util.get_api()

    # tries to retrieve the inventory file from the current
    # form in case it's not available renders the current
    # template with an error message
    inventory_file = quorum.get_field("inventory_file", None)
    if inventory_file == None or not inventory_file.filename:
        return flask.render_template(
            "extra/inventory.html.tpl", link="extras", error="No file defined"
        )

    # creates a temporary file path for the storage of the file
    # and then saves it into that directory
    fd, file_path = tempfile.mkstemp()
    inventory_file.save(file_path)

    # creates the file object that is going to be used in the
    # reading of the CSV file (underlying object)
    file = open(file_path, "rb")
    try:
        data = file.read()
    finally:
        file.close()

    # constructs the bytes based buffer object from the data that
    # has just been loaded from the file
    buffer = quorum.legacy.BytesIO(data)

    # creates the maps that are going to be used to cache the
    # resolution processes for both the stores and the merchandise
    stores_map = dict()
    merchandise_map = dict()

    # creates the map that is going to hold the complete state
    # to be used in the process of the various adjustments (context)
    state = dict()

    def get_adjustment():
        return state.get("adjustment", None)

    def new_adjustment(target_id):
        flush_adjustment()
        adjustment = dict(
            adjustment_target=dict(object_id=target_id), stock_adjustment_lines=[]
        )
        state["adjustment"] = adjustment
        return adjustment

    def flush_adjustment():
        adjustment = get_adjustment()
        state["adjustment"] = None
        if not adjustment:
            return
        payload = dict(stock_adjustment=adjustment)
        stock_adjustment = api.create_stock_adjustment(payload)
        store_id = adjustment["adjustment_target"]["object_id"]
        stock_adjustment_id = stock_adjustment["object_id"]
        quorum.debug(
            "Created stock adjustment '%d' for store '%d'"
            % (stock_adjustment_id, store_id)
        )
        return stock_adjustment

    def add_adjustment_line(merchandise_id, quantity=-1):
        adjustment = get_adjustment()
        if not adjustment:
            raise quorum.OperationalError("No adjustment in context")
        lines = adjustment["stock_adjustment_lines"]
        line = dict(
            stock_on_hand_delta=quantity, merchandise=dict(object_id=merchandise_id)
        )
        lines.append(line)

    def get_store_id(store_code):
        object_id = stores_map.get(store_code, None)
        if object_id:
            return object_id

        kwargs = {
            "start_record": 0,
            "number_records": 1,
            "filters[]": ["store_code:equals:%s" % store_code],
        }

        try:
            stores = api.list_stores(**kwargs)
        except Exception:
            stores = []
        if stores:
            object_id = stores[0]["object_id"]

        stores_map[store_code] = object_id
        return object_id

    def get_merchandise_id(company_product_code):
        # tries to retrieve the object id of the merchandise from the
        # cache and in case it succeeds returns it immediately
        object_id = merchandise_map.get(company_product_code, None)
        if object_id:
            return object_id

        # creates the map containing the (filter) keyword arguments that
        # are going to be send to the list merchandise operation
        kwargs = {
            "start_record": 0,
            "number_records": 1,
            "filters[]": ["company_product_code:equals:%s" % company_product_code],
        }

        # runs the list merchandise operation in order to try to find a
        # merchandise entity for the requested (unique) product code in
        # case there's at least one merchandise its object id is used
        try:
            merchandise = api.list_merchandise(**kwargs)
        except Exception:
            merchandise = []
        if merchandise:
            object_id = merchandise[0]["object_id"]

        # updates the (cache) map for the merchandise with the reference
        # new object id to company product code reference and then returns
        # the object id of the merchandise to the caller method
        merchandise_map[company_product_code] = object_id
        return object_id

    def callback(line, header=None):
        code, quantity, _date, _time = line[:4]

        code = code.strip()
        quantity = quantity.strip()
        quantity = int(quantity)
        quantity = quantity * -1

        is_store = len(code) < 4
        if is_store:
            store_id = get_store_id(code)
        else:
            merchandise_id = get_merchandise_id(code)

        if is_store:
            if store_id:
                new_adjustment(store_id)
            else:
                flush_adjustment()
        elif merchandise_id:
            try:
                add_adjustment_line(merchandise_id, quantity=quantity)
            except Exception:
                pass

    try:
        # start the CSV import operation that is going to import the
        # various lines of the CSV in the buffer and for each of them
        # call the function passed as callback
        util.csv_import(buffer, callback, delimiter=";")
        flush_adjustment()
    finally:
        # closes the temporary file descriptor and removes the temporary
        # file (avoiding any memory leaks)
        os.close(fd)
        os.remove(file_path)

    # redirects the user back to the inventory list page with a success
    # message indicating that everything went ok
    return flask.redirect(
        flask.url_for(
            "inventory_extras", message="Inventory file processed with success"
        )
    )


@app.route("/extras/transfers", methods=("GET",))
@quorum.ensure(
    (
        "inventory.transfer.create",
        "inventory.transactional_merchandise.list",
        "foundation.store.list",
    )
)
def transfers_extras():
    return flask.render_template("extra/transfers.html.tpl", link="extras")


@app.route("/extras/transfers", methods=("POST",))
@quorum.ensure(
    (
        "inventory.transfer.create",
        "inventory.transactional_merchandise.list",
        "foundation.store.list",
    )
)
def do_transfers_extras():
    # retrieves the reference to the API object that is going
    # to be used for the updating of prices operation
    api = util.get_api()

    # tries to retrieve the origin value from the provided set
    # of fields and in case it's not defined re-renders the template
    origin = quorum.get_field("origin", None, cast=int)
    if not origin:
        return flask.render_template(
            "extra/transfers.html.tpl", link="extras", error="No origin defined"
        )

    # tries to retrieve the transfers file from the current
    # form in case it's not available renders the current
    # template with an error message
    transfers_file = quorum.get_field("transfers_file", None)
    if transfers_file == None or not transfers_file.filename:
        return flask.render_template(
            "extra/transfers.html.tpl", link="extras", error="No file defined"
        )

    # creates a temporary file path for the storage of the file
    # and then saves it into that directory
    fd, file_path = tempfile.mkstemp()
    transfers_file.save(file_path)

    # creates the file object that is going to be used in the
    # reading of the CSV file (underlying object)
    file = open(file_path, "rb")
    try:
        data = file.read()
    finally:
        file.close()

    # constructs the bytes based buffer object from the data that
    # has just been loaded from the file
    buffer = quorum.legacy.BytesIO(data)

    # creates the maps that are going to be used to cache the
    # resolution processes for both the stores and the merchandise
    stores_map = dict()
    merchandise_map = dict()

    # creates the map that is going to hold the complete state
    # to be used in the process of the various transfers (context)
    state = dict()

    def get_transfer():
        return state.get("transfer", None)

    def new_transfer(target_id, workflow_state=6):
        flush_transfer()
        transfer = dict(
            origin=dict(object_id=origin),
            destination=dict(object_id=target_id),
            transfer_lines=[],
            _parameters=dict(target_workflow_state=workflow_state),
        )
        state["transfer"] = transfer
        return transfer

    def flush_transfer():
        transfer = get_transfer()
        state["transfer"] = None
        if not transfer:
            return
        payload = dict(transfer=transfer)
        transfer = api.create_transfer(payload)
        transfer_id = transfer["object_id"]
        quorum.debug("Created stock transfer '%d'" % transfer_id)
        return transfer

    def add_transfer_line(merchandise_id, quantity=1):
        transfer = get_transfer()
        if not transfer:
            raise quorum.OperationalError("No transfer in context")
        lines = transfer["transfer_lines"]
        line = dict(quantity=quantity, merchandise=dict(object_id=merchandise_id))
        lines.append(line)

    def get_store_id(store_code):
        object_id = stores_map.get(store_code, None)
        if object_id:
            return object_id

        kwargs = {
            "start_record": 0,
            "number_records": 1,
            "filters[]": ["store_code:equals:%s" % store_code],
        }

        try:
            stores = api.list_stores(**kwargs)
        except Exception:
            stores = []
        if stores:
            object_id = stores[0]["object_id"]

        stores_map[store_code] = object_id
        return object_id

    def get_merchandise_id(company_product_code):
        # tries to retrieve the object id of the merchandise from the
        # cache and in case it succeeds returns it immediately
        object_id = merchandise_map.get(company_product_code, None)
        if object_id:
            return object_id

        # creates the map containing the (filter) keyword arguments that
        # are going to be send to the list merchandise operation
        kwargs = {
            "start_record": 0,
            "number_records": 1,
            "filters[]": ["company_product_code:equals:%s" % company_product_code],
        }

        # runs the list merchandise operation in order to try to find a
        # merchandise entity for the requested (unique) product code in
        # case there's at least one merchandise its object id is used
        try:
            merchandise = api.list_merchandise(**kwargs)
        except Exception:
            merchandise = []
        if merchandise:
            object_id = merchandise[0]["object_id"]

        # updates the (cache) map for the merchandise with the reference
        # new object id to company product code reference and then returns
        # the object id of the merchandise to the caller method
        merchandise_map[company_product_code] = object_id
        return object_id

    def callback(line, header=None):
        code, quantity, _date, _time = line[:4]

        code = code.strip()
        quantity = quantity.strip()
        quantity = int(quantity)

        is_store = len(code) < 4
        if is_store:
            store_id = get_store_id(code)
        else:
            merchandise_id = get_merchandise_id(code)

        if is_store:
            if store_id:
                new_transfer(store_id)
            else:
                flush_transfer()
        elif merchandise_id:
            try:
                add_transfer_line(merchandise_id, quantity=quantity)
            except Exception:
                pass

    try:
        # start the CSV import operation that is going to import the
        # various lines of the CSV in the buffer and for each of them
        # call the function passed as callback
        util.csv_import(buffer, callback, delimiter=";")
        flush_transfer()
    finally:
        # closes the temporary file descriptor and removes the temporary
        # file (avoiding any memory leaks)
        os.close(fd)
        os.remove(file_path)

    # redirects the user back to the transfers list page with a success
    # message indicating that everything went ok
    return flask.redirect(
        flask.url_for(
            "transfers_extras", message="Transfers file processed with success"
        )
    )


@app.route("/extras/ctt", methods=("GET",))
@quorum.ensure("sales.sale_order.list")
def ctt_extras():
    return flask.render_template("extra/ctt.html.tpl", link="extras")


@app.route("/extras/ctt", methods=("POST",))
@quorum.ensure("sales.sale_order.list")
def do_ctt_extras():
    api = util.get_api()
    sale_orders = api.list_sale_orders(
        **{
            "start_record": 0,
            "number_records": -1,
            "eager[]": [
                "customer",
                "customer.primary_contact_information",
                "shipping_address",
            ],
            "filters[]": ["workflow_state:equals:5", "shipping_type:equals:2"],
        }
    )

    out_data = util.encode_ctt(sale_orders, encoding="Cp1252")

    return flask.Response(out_data, mimetype="binary/octet-stream")


@app.route("/extras/template", methods=("GET",))
@quorum.ensure("base.user")
def template_extras():
    return flask.render_template("extra/template.html.tpl", link="extras")


@app.route("/extras/template", methods=("POST",))
@quorum.ensure("foundation.system_company.show.self")
def do_template_extras():
    object = quorum.get_object()
    mask_name = object.get("mask_name", None)
    format = object.get("format", "png")
    base_file = object.get("base_file", None)
    base_data = base_file.read()

    mask_name = "mask_" + mask_name if mask_name else "mask"
    mask_name = mask_name.lower()
    mask_name = mask_name.replace(" ", "_")

    api = util.get_api()
    try:
        mask_data = api.public_media_system_company(label=mask_name)
    except Exception:
        mask_data = None
    if not mask_data:
        raise quorum.OperationalError("No mask defined")

    out_data = util.mask_image(base_data, mask_data, format=format)
    mimetype = mimetypes.guess_type("_." + format)[0]

    return flask.Response(out_data, mimetype=mimetype or "application/octet-stream")


@app.route("/extras/mask", methods=("POST",))
@quorum.ensure("foundation.root_entity.set_media")
def do_mask_extras():
    object = quorum.get_object()
    mask_name = object.get("mask_name", None)
    mask_file = object.get("mask_file", None)

    mask_name = "mask_" + mask_name if mask_name else "mask"
    mask_name = mask_name.lower()
    mask_name = mask_name.replace(" ", "_")

    api = util.get_api()
    system_company = api.self_system_company()

    data = mask_file.read()
    mime_type = mask_file.content_type
    api.set_media_entity(
        system_company["object_id"],
        mask_name,
        data=data,
        mime_type=mime_type,
        visibility=2,
    )

    return flask.redirect(
        flask.url_for("template_extras", message="Mask file uploaded with success")
    )


@app.route("/extras/browser", methods=("GET",))
@quorum.ensure("foundation.root_entity.show_media")
def browser_extras():
    object_id = quorum.get_field("id", None, cast=int)
    return flask.render_template(
        "extra/browser.html.tpl", link="extras", object_id=object_id
    )


@app.route("/extras/browser", methods=("POST",), json=True)
@quorum.ensure("foundation.root_entity.show_media")
def do_browser():
    object_id = quorum.get_field("object_id", None, cast=int)
    api = util.get_api()
    entity = api.get_entity(object_id)
    media = api.info_media_entity(object_id)
    media_info = []
    for item in media:
        mitem = dict(
            object_id=item["object_id"],
            label=item["label"],
            position=item["position"],
            dimensions=item["dimensions"],
            image_url=api.get_media_url(item["secret"]),
        )
        media_info.append(mitem)
    media_info.sort(key=_media_sorter)
    entity["media"] = media_info
    return entity


@app.route("/extras/browser/new_media/<int:id>", methods=("GET",))
@quorum.ensure("foundation.root_entity.set_media")
def new_media_browser(id):
    return flask.render_template(
        "extra/browser/new_media.html.tpl",
        link="extras",
        object_id=id,
        media=dict(),
        errors=dict(),
    )


@app.route("/extras/browser/new_media/<int:id>", methods=("POST",))
@quorum.ensure("foundation.root_entity.set_media")
def create_media_browser(id):
    api = util.get_api()
    engine = quorum.get_field("engine", None) or None
    position = quorum.get_field("position", None, cast=int)
    label = quorum.get_field("label", None) or None
    visibility = quorum.get_field("visibility", None, cast=int)
    description = quorum.get_field("description", None) or None
    thumbnails = quorum.get_field("thumbnails", False, cast=bool)
    media_file = quorum.get_field("media_file", None)
    image_type = mimetypes.guess_type(media_file.filename)[0]
    mime_type = image_type if image_type else "image/unknown"
    try:
        data = media_file.stream.read()
    finally:
        media_file.close()
    api.set_media_entity(
        id,
        data,
        engine=engine,
        position=position,
        label=label,
        mime_type=mime_type,
        visibility=visibility,
        description=description,
        thumbnails=thumbnails,
    )
    return flask.redirect(flask.url_for("browser_extras", id=id))


@app.route("/extras/browser/clear_media/<int:id>", methods=("GET",))
@quorum.ensure("foundation.root_entity.clear_media")
def clear_media_browser(id):
    api = util.get_api()
    api.clear_media_entity(id)
    return flask.redirect(flask.url_for("browser_extras", id=id))


def _media_sorter(item):
    return (item["label"] or "", item["position"] or 0, item["dimensions"] or "")
