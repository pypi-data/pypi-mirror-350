{% extends "partials/layout.html.tpl" %}
{% block title %}About{% endblock %}
{% block name %}About{% endblock %}
{% block content %}
    <div class="quote">
        The complete project was developed by the <a href="http://hive.pt">Hive Solutions</a><br />
        development team using only spare time.
    </div>
    <div class="separator-horizontal"></div>
    <div class="quote">
        Omnix is currently licensed under the much permissive<br />
        <strong>Apache License, Version 2.0</strong>
        and the<br/>
        current repository is hosted at <a href="https://github.com/hivesolutions/omnix">GitHub</a>.
    </div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">session id</td>
                <td class="left value" width="50%">{{ session_id }}</td>
            </tr>
        </tbody>
    </table>
{% endblock %}
