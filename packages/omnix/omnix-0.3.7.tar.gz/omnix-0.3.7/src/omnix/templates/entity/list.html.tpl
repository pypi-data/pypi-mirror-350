{% extends "partials/layout.html.tpl" %}
{% block title %}Entities{% endblock %}
{% block name %}Entities{% endblock %}
{% block content %}
    <ul class="filter" data-infinite="true" data-original_value="Search Entities">
        <div class="data-source" data-url="{{ url_for('list_entities_json') }}" data-type="json" data-timeout="0"></div>
        <li class="template clear">
            <div class="name"><a href="{{ url_for('show_entities', id = 0) }}%[object_id]">%[object_id]</a></div>
            <div class="description">%[_class]</div>
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
