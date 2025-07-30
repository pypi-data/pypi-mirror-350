{% extends "partials/layout.html.tpl" %}
{% block title %}Customers{% endblock %}
{% block name %}{{ customer.representation }}{% endblock %}
{% block content %}
    <div class="quote">{{ customer.name }}</div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">email</td>
                <td class="left value" width="50%">{{ customer.primary_contact_information.email }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">birthday</td>
                <td class="left value" width="50%">{{ customer.birthday }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">gender</td>
                <td class="left value" width="50%">{{ customer.gender }}</td>
            </tr>
        </tbody>
    </table>
{% endblock %}
