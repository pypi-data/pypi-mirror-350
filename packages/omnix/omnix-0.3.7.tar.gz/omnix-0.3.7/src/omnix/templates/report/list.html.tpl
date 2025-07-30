{% extends "partials/layout.html.tpl" %}
{% block title %}Reports{% endblock %}
{% block name %}Reports{% endblock %}
{% block content %}
    <ul>
        <li>
            <div class="name">
                <a href="{{ url_for('sales_reports') }}">Sales Report</a>
            </div>
            <div class="description">Reports of sales per month</div>
        </li>
    </ul>
{% endblock %}
