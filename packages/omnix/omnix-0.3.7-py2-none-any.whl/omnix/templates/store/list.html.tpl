{% extends "partials/layout.html.tpl" %}
{% block title %}Stores{% endblock %}
{% block name %}Stores{% endblock %}
{% block content %}
    <ul class="filter" data-infinite="true" data-original_value="Search Stores">
        <div class="data-source" data-url="{{ url_for('list_stores_json') }}" data-type="json" data-timeout="0"></div>
        <li class="template clear">
            <div class="name"><a href="{{ url_for('show_stores', id = 0) }}%[object_id]">%[representation]</a></div>
            <div class="description">%[primary_contact_information.email]</div>
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
