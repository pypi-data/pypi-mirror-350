{% extends "partials/layout_media.html.tpl" %}
{% block title %}Media{% endblock %}
{% block name %}{{ media.object_id }}{% endblock %}
{% block content %}
    <form enctype="multipart/form-data" action="{{ url_for('update_media', id = media.object_id) }}"
          method="post" class="form">
        <div class="label">
            <label>Engine</label>
        </div>
        <div class="input">
            <div class="drop-field drop-field-select" value="{{ media.engine|default('db', True) }}"
                 data-error="{{ errors.engine }}"  data-disabled="1">
            </div>
        </div>
        <div class="label">
            <label>Position</label>
        </div>
        <div class="input">
            <input class="text-field" name="position" placeholder="eg: 1, 2, 3, etc." value="{{ media.position }}"
                   data-error="{{ errors.position }}" />
        </div>
        <div class="label">
            <label>Label</label>
        </div>
        <div class="input">
            <input class="text-field" name="label" placeholder="eg: main_header" value="{{ media.label }}"
                   data-error="{{ errors.label }}" />
        </div>
        <div class="label">
            <label>Visibility</label>
        </div>
        <div class="input">
            <div class="drop-field drop-field-select" data-error="{{ errors.engine }}">
                <input name="visibility" type="hidden" class="hidden-field"
                       value="{{ media.visibility|default('3', True) }}" />
                <ul class="data-source" data-type="local">
                    <li>
                        <span name="name">Public</span>
                        <span name="value">1</span>
                    </li>
                    <li>
                        <span name="name">Global</span>
                        <span name="value">2</span>
                    </li>
                    <li>
                        <span name="name">Constrained</span>
                        <span name="value">3</span>
                    </li>
                    <li>
                        <span name="name">Private</span>
                        <span name="value">4</span>
                    </li>
                </ul>
            </div>
        </div>
        <div class="label">
            <label>Description</label>
        </div>
        <div class="input">
            <textarea class="text-area" name="description" placeholder="eg: some words about the media"
                      data-error="{{ errors.description }}">{{ media.description|default("", True) }}</textarea>
        </div>
        <div class="input single">
             <a data-name="media_file" class="uploader">Select & Upload the media file</a>
        </div>
        <span class="button" data-link="{{ url_for('show_media', id = media.object_id) }}">Cancel</span>
        //
        <span class="button" data-submit="true">Update</span>
    </form>
{% endblock %}
