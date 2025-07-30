{% extends "partials/layout_employee.html.tpl" %}
{% block title %}Employees{% endblock %}
{% block name %}{{ employee.short_name }}{% endblock %}
{% block content %}
    <div class="quote">{{ title }}</div>
    <div class="separator-horizontal"></div>
    <table class="table table-resume three">
        <tbody>
            <tr>
                <td>
                    <span class="label">Net Sales</span><br />
                    <span class="value">{{ "%.2f" % sales_total }} €</span>
                </td>
                <td>
                    <span class="label">Sales & Returns</span><br />
                    <span class="value">{{ sales_count }} / {{ returns_count }}</span>
                </td>
                <td>
                    <span class="label">Commissions</span><br />
                    <span class="value">{{ "%.2f" % (sales_total * commission_rate) }} €</span>
                </td>
            </tr>
        </tbody>
    </table>
    <table class="table table-list">
        <thead>
            <tr>
                <th class="left label" width="25%">Date</th>
                <th class="left label" width="30%">Operation</th>
                <th class="right label" width="15%">Commission</th>
                <th class="right label" width="30%">Op. Value</th>
            </tr>
        </thead>
        <tbody>
            {% for operation in operations %}
                <tr>
                    <td class="left">{{ operation.date_f }}</td>
                    {% if operation._class == "SaleTransaction" %}
                        <td class="left">
                            <a href="{{ session['omnix.base_url'] }}sam/sales/{{ operation.object_id }}">{{ operation.identifier }}</a>
                        </td>
                    {% else %}
                        <td class="left">
                            <a href="{{ session['omnix.base_url'] }}sam/returns/{{ operation.object_id }}">{{ operation.identifier }}</a>
                        </td>
                    {% endif %}
                    {% if operation._class == "SaleTransaction" %}
                        <td class="right">{{ "%.2f" % (operation.price.value * commission_rate) }} €</td>
                        <td class="right">{{ "%.2f" % operation.price.value }} / {{ "%.2f" % operation.price_vat }} €</td>
                    {% else %}
                        <td class="right red">{{ "%.2f" % (operation.price.value * commission_rate * -1) }} €</td>
                        <td class="right red">{{ "%.2f" % (operation.price.value * -1) }} / {{ "%.2f" % (operation.price_vat * -1) }} €</td>
                    {% endif %}
                </tr>
            {% endfor %}
        </tbody>
    </table>
    <table>
        <tbody>
            <tr>
                <td>
                    <div class="links">
                        {% if is_self %}
                            <a href="{{ url_for('sales_employee', month = previous[0], year = previous[1]) }}">previous</a>
                            //
                            {% if has_next %}
                                <a href="{{ url_for('sales_employee', month = next[0], year = next[1]) }}">next</a>
                            {% else %}
                                <span>next</span>
                            {% endif %}
                        {% else %}
                            <a href="{{ url_for('sales_employees', id = employee.object_id, month = previous[0], year = previous[1]) }}">previous</a>
                            //
                            {% if has_next %}
                                <a href="{{ url_for('sales_employees', id = employee.object_id, month = next[0], year = next[1]) }}">next</a>
                            {% else %}
                                <span>next</span>
                            {% endif %}
                        {% endif %}
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
{% endblock %}
