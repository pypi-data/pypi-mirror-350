{% extends "partials/layout.html.tpl" %}
{% block title %}Employees{% endblock %}
{% block name %}Employees{% endblock %}
{% block content %}
    <ul class="filter" data-infinite="true" data-original_value="Search Employees">
        <div class="data-source" data-url="{{ url_for('list_employees_json') }}" data-type="json" data-timeout="0"></div>
        <li class="template clear">
            <div class="name"><a href="{{ url_for('show_employees', id = 0) }}%[object_id]">%[representation]</a></div>
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
