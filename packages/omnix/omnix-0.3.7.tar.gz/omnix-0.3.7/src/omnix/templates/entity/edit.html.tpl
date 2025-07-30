{% extends "partials/layout_entity.html.tpl" %}
{% block title %}Entity{% endblock %}
{% block name %}{{ entity.object_id }}{% endblock %}
{% block content %}
    <form action="{{ url_for('update_entities', id = entity.object_id) }}" method="post" class="form">
        <div class="label">
            <label>Description</label>
        </div>
        <div class="input">
            <textarea class="text-area" name="description" placeholder="eg: some words about the entity"
                      data-error="{{ errors.description }}">{{ entity.description|default("", True) }}</textarea>
        </div>
        <div class="label">
            <label>Metadata</label>
        </div>
        <div class="input">
            <textarea class="text-area text-json" name="metadata" placeholder="eg: JSON conformant string"
                      spellcheck="false" data-error="{{ errors.metadata }}">{{ entity.metadata_s|default("", True) }}</textarea>
        </div>
        <span class="button" data-link="{{ url_for('show_entities', id = entity.object_id) }}">Cancel</span>
        //
        <span class="button" data-submit="true">Update</span>
    </form>
{% endblock %}
