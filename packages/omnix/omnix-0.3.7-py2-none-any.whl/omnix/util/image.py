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

from . import config


def mask_image(base_data, mask_data, format="png"):
    import PIL.Image

    base_file = quorum.legacy.BytesIO(base_data)
    mask_file = quorum.legacy.BytesIO(mask_data)
    out_file = quorum.legacy.BytesIO()

    base_image = PIL.Image.open(base_file)
    mask_image = PIL.Image.open(mask_file)

    target_image = PIL.Image.new("RGBA", mask_image.size, (255, 255, 255, 255))

    base_width, base_height = base_image.size
    mask_width, mask_height = mask_image.size

    base_image = base_image.convert("RGBA")

    if config.IMAGE_RESIZE == "stretch":
        base_image = base_image.resize(mask_image.size, PIL.Image.ANTIALIAS)
    elif config.IMAGE_RESIZE == "box":
        ratio_width = float(mask_width) / float(base_width)
        ratio_height = float(mask_height) / float(base_height)

        ratio = ratio_width if ratio_width < ratio_height else ratio_height
        resize_width = int(base_width * ratio)
        resize_height = int(base_height * ratio)

        base_image = base_image.resize(
            (resize_width, resize_height), PIL.Image.ANTIALIAS
        )
    elif config.IMAGE_RESIZE == "crop":
        ratio_width = float(mask_width) / float(base_width)
        ratio_height = float(mask_height) / float(base_height)

        ratio = ratio_height if ratio_width < ratio_height else ratio_width
        resize_width = int(base_width * ratio)
        resize_height = int(base_height * ratio)

        base_image = base_image.resize(
            (resize_width, resize_height), PIL.Image.ANTIALIAS
        )

        center_width = (resize_width - mask_width) / 2.0
        center_height = (resize_height - mask_height) / 2.0
        center_width = int(center_width)
        center_height = int(center_height)

        crop_box = (
            center_width,
            center_height,
            mask_width + center_width,
            mask_height + center_height,
        )
        base_image = base_image.crop(crop_box)

    base_width, base_height = base_image.size
    center_width = (mask_width - base_width) / 2.0
    center_height = (mask_height - base_height) / 2.0
    center = (int(center_width), int(center_height))

    target_image.paste(base_image, center, base_image)
    target_image.paste(mask_image, (0, 0), mask_image)
    target_image.save(out_file, format)

    out_data = out_file.getvalue()

    return out_data
