{% extends "partials/layout.html.tpl" %}
{% block title %}Inventory List{% endblock %}
{% block name %}Inventory List{% endblock %}
{% block content %}
    <div class="quote">
        Please provide the file containing the inventory list to be imported
        to the data source, the file should be <strong>CSV and multiple value
        based</strong> containing the store codes and product codes.<br />
        Remember this is a <strong>dangerous operation</strong>.
    </div>
    <div class="separator-horizontal"></div>
    {% if error %}
        <div class="quote error">{{ error }}</div>
    {% endif %}
    <form enctype="multipart/form-data" action="{{ url_for('do_inventory_extras') }}" method="post" class="form tiny">
        <div class="input single">
             <a data-name="inventory_file" class="uploader">Select & Upload the inventory list file</a>
        </div>
        <span class="button" data-link="{{ url_for('list_extras') }}">Cancel</span>
        //
        <span class="button" data-submit="true">Upload</span>
    </form>
{% endblock %}
