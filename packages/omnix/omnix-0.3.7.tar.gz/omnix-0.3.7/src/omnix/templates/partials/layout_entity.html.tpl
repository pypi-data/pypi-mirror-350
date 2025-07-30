{% extends "partials/layout.html.tpl" %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        {% if sub_link == "info" %}
            <a href="{{ url_for('show_entities', id = entity.object_id) }}" class="active">info</a>
        {% else %}
            <a href="{{ url_for('show_entities', id = entity.object_id) }}">info</a>
        {% endif %}
        //
        {% if sub_link == "edit" %}
            <a href="{{ url_for('edit_entities', id = entity.object_id) }}" class="active">edit</a>
        {% else %}
            <a href="{{ url_for('edit_entities', id = entity.object_id) }}">edit</a>
        {% endif %}
    </div>
{% endblock %}
