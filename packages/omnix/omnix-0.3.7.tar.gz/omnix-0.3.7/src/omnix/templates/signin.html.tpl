{% extends "partials/layout_simple.html.tpl" %}
{% block title %}Login{% endblock %}
{% block name %}Welcome To Omnix{% endblock %}
{% block content %}
    <div class="quote">
        Omnix is a simple web application for minimal control of an omni instance.<br />
        To be able to access the system please use you <strong>frontdoor account</strong>.
    </div>
    <div class="button login" data-link="{{ url_for('do_login', next = next) }}"></div>
{% endblock %}
