odoo.define('le_backend_theme.ListRenderer', function(require) {
    "use strict";

    var ListRenderer = require('web.ListRenderer');
    var config = require('web.config');
    var field_utils = require('web.field_utils');

    var FIELD_CLASSES = {
        float: 'o_list_number',
        integer: 'o_list_number',
        monetary: 'o_list_number',
        text: 'o_list_text',
    };

    var OLR = ListRenderer.include({
        _renderHeaderCell: function (node) {
            var name = node.attrs.name;
            var order = this.state.orderedBy;
            var isNodeSorted = order[0] && order[0].name === name;
            var field = this.state.fields[name];
            var $th = $('<th>');
            if (!field) {
                return $th;
            }
            var description;
            if (node.attrs.widget) {
                description = this.state.fieldsInfo.list[name].Widget.prototype.description;
            }
            if (description === undefined) {
                description = node.attrs.string || field.string;
            }
            $th.text(description)
                .data('name', name)
                .toggleClass('o-sort-down', isNodeSorted ? !order[0].asc : false)
                .toggleClass('o-sort-up', isNodeSorted ? order[0].asc : false)
                .addClass(field.sortable && 'o_column_sortable')
                .addClass(name);
    
            if (isNodeSorted) {
                $th.attr('aria-sort', order[0].asc ? 'ascending' : 'descending');
            }
    
            if (field.type === 'float' || field.type === 'integer' || field.type === 'monetary') {
                $th.addClass('o_list_number_th');
            }
    
            if (config.debug) {
                var fieldDescr = {
                    field: field,
                    name: name,
                    string: description || name,
                    record: this.state,
                    attrs: node.attrs,
                };
                this._addFieldTooltip(fieldDescr, $th);
            }
            return $th;
        },

        _renderBodyCell: function (record, node, colIndex, options) {
            var tdClassName = 'o_data_cell';
            if (node.tag === 'button') {
                tdClassName += ' o_list_button';
            } else if (node.tag === 'field') {
                var typeClass = FIELD_CLASSES[this.state.fields[node.attrs.name].type];
                if (typeClass) {
                    tdClassName += (' ' + typeClass);
                }
                if (node.attrs.widget) {
                    tdClassName += (' o_' + node.attrs.widget + '_cell');
                }
                tdClassName+= (' ' + node.attrs.name)
            }
            var $td = $('<td>', { class: tdClassName });
    
            // We register modifiers on the <td> element so that it gets the correct
            // modifiers classes (for styling)
            var modifiers = this._registerModifiers(node, record, $td, _.pick(options, 'mode'));
            // If the invisible modifiers is true, the <td> element is left empty.
            // Indeed, if the modifiers was to change the whole cell would be
            // rerendered anyway.
            if (modifiers.invisible && !(options && options.renderInvisible)) {
                return $td;
            }
    
            if (node.tag === 'button') {
                return $td.append(this._renderButton(record, node));
            } else if (node.tag === 'widget') {
                return $td.append(this._renderWidget(record, node));
            }
            if (node.attrs.widget || (options && options.renderWidgets)) {
                var $el = this._renderFieldWidget(node, record, _.pick(options, 'mode'));
                this._handleAttributes($el, node);
                return $td.append($el);
            }
            var name = node.attrs.name;
            var field = this.state.fields[name];
            var value = record.data[name];
            var formattedValue = field_utils.format[field.type](value, field, {
                data: record.data,
                escape: true,
                isPassword: 'password' in node.attrs,
                digits: node.attrs.digits ? JSON.parse(node.attrs.digits) : undefined,
            });
            this._handleAttributes($td, node);
            return $td.html(formattedValue);
        },
    })
})