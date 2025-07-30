{% extends "partials/layout.html.tpl" %}
{% block title %}Extras{% endblock %}
{% block name %}Extras{% endblock %}
{% block content %}
    <ul>
        {% if acl("foundation.root_entity.set_media") %}
            <li>
                <div class="name">
                    <a href="{{ url_for('media_extras') }}">Media List</a>
                </div>
                <div class="description">Upload a list of media to be used in entities</div>
            </li>
        {% endif %}
        {% if acl("inventory.transactional_merchandise.update") %}
            <li>
                <div class="name">
                    <a href="{{ url_for('images_extras') }}">Images List</a>
                </div>
                <div class="description">Upload a list of images to be used in inventory</div>
            </li>
        {% endif %}
        {% if acl("foundation.root_entity.update") %}
            <li>
                <div class="name">
                    <a href="{{ url_for('metadata_extras') }}">Metadata List</a>
                </div>
                <div class="description">Upload a list of metadata information about entities</div>
            </li>
        {% endif %}
        {% if acl("inventory.transactional_merchandise.update") %}
            <li>
                <div class="name">
                    <a href="{{ url_for('prices_extras') }}">Prices List</a>
                </div>
                <div class="description">Import list of prices to the current data source</div>
            </li>
        {% endif %}
        {% if acl("inventory.transactional_merchandise.update") %}
            <li>
                <div class="name">
                    <a href="{{ url_for('costs_extras') }}">Costs List</a>
                </div>
                <div class="description">Import list of costs to the current data source</div>
            </li>
        {% endif %}
        {% if acl((
               "inventory.stock_adjustment.create",
               "inventory.transactional_merchandise.list",
               "foundation.store.list"
           )) %}
            <li>
                <div class="name">
                    <a href="{{ url_for('inventory_extras') }}">Inventory List</a>
                </div>
                <div class="description">Import list of inventory items to the current data source</div>
            </li>
        {% endif %}
        {% if acl((
               "inventory.transfer.create",
               "inventory.transactional_merchandise.list",
               "foundation.store.list"
           )) %}
            <li>
                <div class="name">
                    <a href="{{ url_for('transfers_extras') }}">Transfers List</a>
                </div>
                <div class="description">Import list of transfers to the current data source</div>
            </li>
        {% endif %}
        {% if acl("sales.sale_order.list") %}
            <li>
                <div class="name">
                    <a href="{{ url_for('ctt_extras') }}">CTT Shipping</a>
                </div>
                <div class="description">Generate the standard shipping file for open sale orders</div>
            </li>
        {% endif %}
        {% if acl("foundation.system_company.show.self") %}
            <li>
                <div class="name">
                    <a href="{{ url_for('template_extras') }}">Template Applier</a>
                </div>
                <div class="description">Apply an image template to a base image</div>
            </li>
        {% endif %}
        {% if acl("foundation.root_entity.show_media") %}
            <li>
                <div class="name">
                    <a href="{{ url_for('browser_extras') }}">Media Browser</a>
                </div>
                <div class="description">Browse throught media of each entity</div>
            </li>
        {% endif %}
    </ul>
{% endblock %}
