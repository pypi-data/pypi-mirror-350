{% extends "partials/layout.html.tpl" %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        {% if sub_link == "info" %}
            <a href="{{ url_for('show_stores', id = store.object_id) }}" class="active">info</a>
        {% else %}
            <a href="{{ url_for('show_stores', id = store.object_id) }}">info</a>
        {% endif %}
        //
        {% if sub_link == "sales" %}
            <a href="{{ url_for('sales_stores', id = store.object_id) }}" class="active">sales</a>
        {% else %}
            <a href="{{ url_for('sales_stores', id = store.object_id) }}">sales</a>
        {% endif %}
    </div>
{% endblock %}
