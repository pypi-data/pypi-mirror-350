{% extends "partials/layout.html.tpl" %}
{% block title %}Metadata List{% endblock %}
{% block name %}Metadata List{% endblock %}
{% block content %}
    <div class="quote">
        Please provide the file containing the list of metadata to be imported
        to the data source, the file should be <strong>CSV file
        based</strong> containing object id and metdata.<br />
        Remember this is a <strong>dangerous operation</strong>.
    </div>
    <div class="separator-horizontal"></div>
    {% if error %}
        <div class="quote error">{{ error }}</div>
    {% endif %}
    <form enctype="multipart/form-data" action="{{ url_for('do_metadata_extras') }}" method="post" class="form tiny">
        <div class="input">
            <div class="option">
                <span class="float-left">Custom metadata ?</span>
                <input class="float-right" type="checkbox" name="custom" />
                <div class="clear"></div>
            </div>
            <div class="option">
                <span class="float-left">Use "," instead of ";" for separator ?</span>
                <input class="float-right" type="checkbox" name="comma" />
                <div class="clear"></div>
            </div>
        </div>
        <div class="input single">
             <a data-name="metadata_file" class="uploader">Select & Upload the metadata list file</a>
        </div>
        <span class="button" data-link="{{ url_for('list_extras') }}">Cancel</span>
        //
        <span class="button" data-submit="true">Upload</span>
    </form>
{% endblock %}
