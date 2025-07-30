{% extends "email/layout.en_us.html.tpl" %}
{% block title %}Activity Report{% endblock %}
{% block content %}
    <p>
        This email contains information about the latest created operations
        in the Omni system. This report should contain descriptions for the
        complete set of operations that are associated with the current period.
    </p>
    {{ h2("Overview") }}
    <p>
        <strong>Period:</strong>
        <span>{{ target }}</span>
    </p>
    <p>
        <strong>Net Sales:</strong>
        <span>{{ "%.2f" % sales_total }} €</span>
    </p>
    <p>
        <strong>Sales & Returns:</strong>
        <span>{{ sales_count }} / {{ returns_count }}</span>
    </p>
    <p>
        <strong>Commissions:</strong>
        <span>{{ "%.2f" % (sales_total * commission_rate) }} €</span>
    </p>
    {{ h2("Sales & Returns") }}
    <p>
        <table cellspacing="0" width="100%">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Operation</th>
                    <th>Commission</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                {% for operation in operations %}
                    <tr>
                        <td>{{ operation.date_f }}</td>
                        {% if operation._class == "SaleTransaction" %}
                            <td >
                                {% if settings.links %}
                                    <a href="{{ omnix_base_url }}sam/sales/{{ operation.object_id }}">{{ operation.identifier }}</a>
                                {% else %}
                                    <span>{{ operation.identifier }}</span>
                                {% endif %}
                            </td>
                        {% else %}
                            <td>
                                {% if settings.links %}
                                    <a href="{{ omnix_base_url }}sam/returns/{{ operation.object_id }}">{{ operation.identifier }}</a>
                                {% else %}
                                    <span>{{ operation.identifier }}</span>
                                {% endif %}
                            </td>
                        {% endif %}
                        {% if operation._class == "SaleTransaction" %}
                            <td>{{ "%.2f" % (operation.price.value * commission_rate) }} €</td>
                            <td>{{ "%.2f" % operation.price.value }} / {{ "%.2f" % operation.price_vat }} €</td>
                        {% else %}
                            <td>{{ "%.2f" % (operation.price.value * commission_rate * -1) }} €</td>
                            <td>{{ "%.2f" % (operation.price.value * -1) }} / {{ "%.2f" % (operation.price_vat * -1) }} €</td>
                        {% endif %}
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </p>
    {{ h2("We've Got You Covered") }}
    <p>
        Have any problems? Our support team is available at the drop of a hat.
        Send us an email, day or night, on {{ link("mailto:help@omnix.com", "help@omnix.com", False) }}.
    </p>
{% endblock %}
