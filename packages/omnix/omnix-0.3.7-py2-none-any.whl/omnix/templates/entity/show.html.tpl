{% extends "partials/layout_entity.html.tpl" %}
{% block title %}Entity{% endblock %}
{% block name %}{{ entity.object_id }}{% endblock %}
{% block content %}
    <div class="quote">{{ entity.object_id }}</div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">created</td>
                <td class="left value" width="50%">{{ entity.create_date }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">modified</td>
                <td class="left value" width="50%">{{ entity.modify_date }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">class</td>
                <td class="left value" width="50%">{{ entity._class }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">status</td>
                <td class="left value" width="50%">{{ entity.status }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">representation</td>
                <td class="left value" width="50%">{{ entity.representation|default("N/A", True) }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">description</td>
                <td class="left value" width="50%">{{ entity.description|default("N/A", True) }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">metadata</td>
                <td class="left value" width="50%">{{ entity.metadata_s|default("N/A", True)|nl_to_br|sp_to_nbsp }}</td>
            </tr>
        </tbody>
    </table>
{% endblock %}
