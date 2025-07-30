{% extends "email/layout.pt_pt.html.tpl" %}
{% block title %}Relatório de Atividade{% endblock %}
{% block content %}
    <p>
        Este email contêm informações sobre as suas últimas operações feitas
        no sistema Omni. Este relatório deve conter a descrições para o conjunto
        completo de operações associadas ao corrente período.
    </p>
    {{ h2("Resumo") }}
    <p>
        <strong>Período:</strong>
        <span>{{ target }}</span>
    </p>
    <p>
        <strong>Vendas Líquidas:</strong>
        <span>{{ "%.2f" % sales_total }} €</span>
    </p>
    <p>
        <strong>Vendas & Devoluções:</strong>
        <span>{{ sales_count }} / {{ returns_count }}</span>
    </p>
    <p>
        <strong>Comissões:</strong>
        <span>{{ "%.2f" % (sales_total * commission_rate) }} €</span>
    </p>
    {{ h2("Vendas & Devoluções") }}
    <p>
        <table cellspacing="0" width="100%">
            <thead>
                <tr>
                    <th>Data</th>
                    <th>Operação</th>
                    <th>Comissão</th>
                    <th>Valor</th>
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
    {{ h2("Estamos Sempre Consigo") }}
    <p>
        Algum problema? A nossa equipa de apoio está disponível para o ajudar.
        Envie-nos um email para {{ link("mailto:ajuda@omnix.com", "ajuda@omnix.com", False) }}.
    </p>
{% endblock %}
