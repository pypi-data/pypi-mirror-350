{% extends "partials/layout.html.tpl" %}
{% block title %}Transfers List{% endblock %}
{% block name %}Transfers List{% endblock %}
{% block content %}
    <div class="quote">
        Please provide the file containing the transfers list to be imported
        to the data source, the file should be <strong>CSV and multiple value
        based</strong> containing the store codes and product codes.<br />
        Remember this is a <strong>dangerous operation</strong>.
    </div>
    <div class="separator-horizontal"></div>
    {% if error %}
        <div class="quote error">{{ error }}</div>
    {% endif %}
    <form enctype="multipart/form-data" action="{{ url_for('do_transfers_extras') }}" method="post" class="form tiny">
        <div class="input">
            <div class="drop-field" data-original_value="Origin" data-value_attribute="object_id">
                <input type="hidden" class="hidden-field" name="origin" />
                <div class="data-source" data-url="{{ url_for('list_stores_json') }}" data-type="json"></div>
            </div>
        </div>
        <div class="input single">
             <a data-name="transfers_file" class="uploader">Select & Upload the transfers list file</a>
        </div>
        <span class="button" data-link="{{ url_for('list_extras') }}">Cancel</span>
        //
        <span class="button" data-submit="true">Upload</span>
    </form>
{% endblock %}
