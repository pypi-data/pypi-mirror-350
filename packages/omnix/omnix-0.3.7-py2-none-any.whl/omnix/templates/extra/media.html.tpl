{% extends "partials/layout.html.tpl" %}
{% block title %}Media List{% endblock %}
{% block name %}Media List{% endblock %}
{% block content %}
    <div class="quote">
        Please provide the file containing the list of media to be imported
        to the data source, the file should be <strong>zip file
        based</strong> containing media files with their names.<br />
        Remember this is a <strong>dangerous operation</strong>.
    </div>
    <div class="separator-horizontal"></div>
    {% if error %}
        <div class="quote error">{{ error }}</div>
    {% endif %}
    <form enctype="multipart/form-data" action="{{ url_for('do_media_extras') }}" method="post" class="form tiny">
        <div class="input single">
             <a data-name="media_file" class="uploader">Select & Upload the media list file</a>
        </div>
        <span class="button" data-link="{{ url_for('list_extras') }}">Cancel</span>
        //
        <span class="button" data-submit="true">Upload</span>
    </form>
{% endblock %}
