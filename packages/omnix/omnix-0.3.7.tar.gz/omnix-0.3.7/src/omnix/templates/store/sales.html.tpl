{% extends "partials/layout_store.html.tpl" %}
{% block title %}Stores{% endblock %}
{% block name %}{{ store.name }}{% endblock %}
{% block content %}
    <div class="quote">{{ current.date.strftime("%b %d, %Y") }}</div>
    <div class="separator-horizontal"></div>
    <table class="table table-resume">
        <tbody>
            <tr>
                <td>
                    <span class="label">Today's Sales</span><br />
                    <span class="value {{ current.number_direction }}">{{ current.net_number_sales }}</span>
                </td>
                <td>
                    <span class="label">Today's Amount</span><br />
                    <span class="value {{ current.amount_direction }}">{{ "%0.2f" % current.net_price_vat }} €</span>
                </td>
            </tr>
        </tbody>
    </table>
    <table class="table table-list">
        <thead>
            <tr>
                <th class="left label" width="50%">Previous Days</th>
                <th class="right label" width="25%">Sales</th>
                <th class="right label" width="25%">Total</th>
            </tr>
        </thead>
        <tbody>
            {% for day in days %}
                <tr>
                    <td class="left">{{ day.date.strftime("%b %d, %Y") }}</td>
                    <td class="right">{{ day.net_number_sales }}</td>
                    <td class="right">{{ "%0.2f" % day.net_price_vat }} €</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}
