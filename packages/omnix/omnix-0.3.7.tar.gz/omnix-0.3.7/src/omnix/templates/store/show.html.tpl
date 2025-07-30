{% extends "partials/layout_store.html.tpl" %}
{% block title %}Stores{% endblock %}
{% block name %}{{ store.name }}{% endblock %}
{% block content %}
    <div class="quote">{{ store.name }}</div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">phone</td>
                <td class="left value" width="50%">{{ store.primary_contact_information.phone_number|default("", true) }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">email</td>
                <td class="left value" width="50%">{{ store.primary_contact_information.email|default("", true) }}</td>
            </tr>
        </tbody>
    </table>
{% endblock %}
