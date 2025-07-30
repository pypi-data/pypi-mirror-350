{% extends "partials/layout.html.tpl" %}
{% block title %}Media Browser{% endblock %}
{% block name %}Media Browser{% endblock %}
{% block content %}
    <form action="{{ url_for('do_browser') }}" method="get"
          data-media="{{ url_for('show_media', id = 0) }}">
        <div class="media-preview">
            <div class="label">
                <label>Object ID</label>
            </div>
            <div class="input">
                <input class="text-field focus" name="object_id" placeholder="eg: 123123"
                       data-type="natural" value="{{ object_id|default('', True) }}" />
            </div>
            <div class="preview-panel">
                <div class="label">
                    <label>Class</label>
                </div>
                <div class="input">
                    <input class="text-field" name="class" data-disabled="1" />
                </div>
                <div class="label">
                    <label>Representation</label>
                </div>
                <div class="input">
                    <input class="text-field" name="representation" data-disabled="1" />
                </div>
                <div class="label">
                    <label>Media</label>
                </div>
                <div class="media-target"></div>
                <div class="operations-target">
                    <span class="button button-add" data-reference="{{ url_for('new_media_browser', id = 0) }}">Add Media</span>
                    {% if acl("foundation.root_entity.clear_media") %}
                        <span>//</span>
                        <span class="button button-confirm button-clear" data-reference="{{ url_for('clear_media_browser', id = 0) }}"
                              data-message="Do you really want to clear all media values for entity ?">Clear Media</span>
                    {% endif %}
                </div>
            </div>
        </div>
    </form>
{% endblock %}
