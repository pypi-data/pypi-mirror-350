{% extends "partials/layout.html.tpl" %}
{% block title %}Media{% endblock %}
{% block name %}Media{% endblock %}
{% block content %}
    <ul class="filter" data-infinite="true" data-original_value="Search Media">
        <div class="data-source" data-url="{{ url_for('list_media_json') }}" data-type="json" data-timeout="0"></div>
        <li class="template clear">
            <div class="name"><a href="{{ url_for('show_media', id = 0) }}%[object_id]">%[label]</a></div>
            <div class="description">%[dimensions]</div>
        </li>
        <div class="filter-no-results quote">
            No results found
        </div>
        <div class="filter-more">
            <span class="button more">Load more</span>
            <span class="button load">Loading</span>
        </div>
    </ul>
{% endblock %}
