{% extends "partials/layout_report.html.tpl" %}
{% block title %}Sales Report{% endblock %}
{% block name %}Sales Report{% endblock %}
{% block description %}Actualizado a 09/01/2013 19:34{% endblock %}
{% block content %}
    <table class="table table-full table-report">
        <thead>
            <tr>
                <th class="center label" data-width="60">Rank</th>
                <th class="left label" data-width="200">Seller</th>
                <th class="left label" style="width:10000px;">Store</th>
                <th class="right label" data-width="180">Sales</th>
                <th class="right label" data-width="180">Commision</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="center">4º</td>
                <td class="left"><a href="#">Alberto F.</a></td>
                <td class="left">Sede</td>
                <td class="right"><a href="#">120.00 €</a></td>
                <td class="right">12.00 €</td>
            </tr>
            <tr>
                <td class="center">4º</td>
                <td class="left"><a href="#">Alberto F.</a></td>
                <td class="left">Sede</td>
                <td class="right"><a href="#">120.00 €</a></td>
                <td class="right">12.00 €</td>
            </tr>
            <tr>
                <td class="center">4º</td>
                <td class="left"><a href="#">Alberto F.</a></td>
                <td class="left">Sede</td>
                <td class="right"><a href="#">120.00 €</a></td>
                <td class="right">12.00 €</td>
            </tr>
            <tr>
                <td class="center">4º</td>
                <td class="left"><a href="#">Alberto F.</a></td>
                <td class="left">Sede</td>
                <td class="right"><a href="#">120.00 €</a></td>
                <td class="right">12.00 €</td>
            </tr>
        </tbody>
    </table>
    <table class="table-full">
        <tbody>
            <tr>
                <td>
                    <div class="links">
                        <a href="#">previous</a> // <a href="#">next</a>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
{% endblock %}
