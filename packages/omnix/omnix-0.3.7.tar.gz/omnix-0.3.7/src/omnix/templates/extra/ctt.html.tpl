{% extends "partials/layout.html.tpl" %}
{% block title %}CTT Shipping{% endblock %}
{% block name %}CTT Shipping{% endblock %}
{% block content %}
    <div class="quote">
        The current operation will generate a file containing all the reserved
        (to be shipped) orders using the currently <strong>standard CTT (Correios) format</strong>,
        only ship to customer order will be selected.
    </div>
    <div class="quote">
        The resulting file will be encoded using the standard <strong>Windows-1252</strong>.<br/>
        <strong>This operation may take some time</strong>, please be patient.
    </div>
    <div class="separator-horizontal"></div>
    {% if error %}
        <div class="quote error">{{ error }}</div>
    {% endif %}
    <form action="{{ url_for('do_ctt_extras') }}" method="post" class="form tiny">
        <span class="button" data-link="{{ url_for('list_extras') }}">Cancel</span>
        //
        <span class="button" data-submit="true">Generate</span>
    </form>
{% endblock %}
