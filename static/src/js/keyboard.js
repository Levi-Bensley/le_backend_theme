odoo.define('le_backend_theme.KeyboardNavigationMixin', function (require) {
"use strict";

var core = require('web.core');
var config = require("web.config");
var session = require("web.session");

var AbstractWebClient = require('web.AbstractWebClient');

var _t = core._t;
var QWeb = core.qweb;

AbstractWebClient.include({
	_getAllUsedAccessKeys: function () {
        return _.union(this._super.apply(this, arguments), ['M', 'T']);
    },
});

});

