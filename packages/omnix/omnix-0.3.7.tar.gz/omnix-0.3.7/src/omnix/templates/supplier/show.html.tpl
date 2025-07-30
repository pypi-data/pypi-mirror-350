{% extends "partials/layout.html.tpl" %}
{% block title %}Suppliers{% endblock %}
{% block name %}{{ supplier.representation }}{% endblock %}
{% block content %}
    <div class="quote">{{ supplier.name }}</div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">phone</td>
                <td class="left value" width="50%">{{ supplier.primary_contact_information.phone_number|default("", True) }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">email</td>
                <td class="left value" width="50%">{{ supplier.primary_contact_information.email|default("", True) }}</td>
            </tr>
        </tbody>
    </table>
{% endblock %}
