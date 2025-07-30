// Hive Omnix System
// Copyright (c) 2008-2025 Hive Solutions Lda.
//
// This file is part of Hive Omnix System.
//
// Hive Omnix System is free software: you can redistribute it and/or modify
// it under the terms of the Apache License as published by the Apache
// Foundation, either version 2.0 of the License, or (at your option) any
// later version.
//
// Hive Omnix System is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// Apache License for more details.
//
// You should have received a copy of the Apache License along with
// Hive Omnix System. If not, see <http://www.apache.org/licenses/>.

// __author__    = João Magalhães <joamag@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision$
// __date__      = $LastChangedDate$
// __copyright__ = Copyright (c) 2008-2025 Hive Solutions Lda.
// __license__   = Apache License, Version 2.0

(function(jQuery) {
    jQuery.fn.uapply = function(options) {
        // sets the jquery matched object
        var matchedObject = this;

        // retrieves the reference to the media preview object
        // so that the proper plugin is registered
        var mediaPreview = jQuery(".media-preview", matchedObject);
        mediaPreview.umediapreview();

        // returns the current context to the caller method so that
        // it may be used for chained operations
        return this;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.umediapreview = function(options) {
        var matchedObject = this;
        var objectId = jQuery(".text-field[name=object_id]", matchedObject);
        var previewPanel = jQuery(".preview-panel", matchedObject);

        previewPanel.hide();

        var update = function(element) {
            var form = element.parents("form");
            var previewPanel = jQuery(".preview-panel", element);
            var mediaTarget = jQuery(".media-target", previewPanel);
            var operationsTarget = jQuery(".operations-target", previewPanel);
            var buttonAdd = jQuery(".button-add", operationsTarget);
            var buttonClear = jQuery(".button-clear", operationsTarget);
            var objectId = jQuery(".text-field[name=object_id]", element);
            var classInput = jQuery("input[name=class]", element);
            var representationInput = jQuery("input[name=representation]",
                element);
            var url = form.attr("action");
            var mediaUrl = form.attr("data-media");
            var newUrlAdd = buttonAdd.attr("data-reference");
            var newUrlClear = buttonClear.attr("data-reference");
            var value = objectId.uxvalue();
            previewPanel.hide();
            mediaTarget.empty();
            if (!value) {
                return;
            }
            jQuery.ajax({
                url: url,
                type: "post",
                data: {
                    object_id: value
                },
                success: function(data) {
                    var media = data.media;
                    for (var index = 0; index < media.length; index++) {
                        var item = media[index];
                        var itemUrl = mediaUrl + String(item.object_id);
                        var imageContainer = jQuery("<div class=\"image-container\"></div>");
                        var imageLink = jQuery("<a href=\"" + itemUrl + "\"></a>");
                        var image = jQuery("<img src=\"" + item.image_url + "\" />");
                        var title = jQuery("<h2>" + item.label + "</h2>");
                        var subTitle = jQuery("<h3>" + (item.dimensions || "unset") + "</h3>");
                        imageLink.append(image);
                        imageLink.append(title);
                        imageLink.append(subTitle);
                        imageContainer.append(imageLink);
                        mediaTarget.append(imageContainer);
                        imageContainer.uxapply();
                    }
                    buttonAdd.attr("data-link", newUrlAdd + value);
                    buttonClear.attr("data-link", newUrlClear + value);
                    classInput.val(data._class);
                    representationInput.val(data.representation);
                    previewPanel.show();
                }
            });
        };

        objectId.bind("value_change", function() {
            var element = jQuery(this);
            var mediaPreview = element.parents(".media-preview");
            update(mediaPreview);
        });

        matchedObject.each(function(index, element) {
            var _element = jQuery(this);
            update(_element);
        });

        return this;
    };
})(jQuery);

jQuery(document).ready(function() {
    var _body = jQuery("body");
    _body.bind("applied", function(event, base) {
        base.uapply();
    });
});
