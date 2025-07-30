{% extends "partials/layout_employee.html.tpl" %}
{% block title %}Employees{% endblock %}
{% block name %}{{ employee.short_name }}{% endblock %}
{% block content %}
    <div class="quote">{{ employee.representation }}</div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">phone</td>
                <td class="left value" width="50%">{{ employee.primary_contact_information.phone_number|default("", True) }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">email</td>
                <td class="left value" width="50%">{{ employee.primary_contact_information.email|default("", True) }}</td>
            </tr>
        </tbody>
    </table>
{% endblock %}
