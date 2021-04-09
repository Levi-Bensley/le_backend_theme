odoo.define('le_backend_theme.Chatter', function (require) {
"use strict";

var core = require('web.core');
var config = require("web.config");
var session = require("web.session");

var Chatter = require('mail.Chatter');

var _t = core._t;
var QWeb = core.qweb;

Chatter.include({
    _openComposer: function (options) {
        if (this._composer && options.isLog === this._composer.options.isLog && this._composer.$el.is(':visible')) {
            this._closeComposer(false);
        } else {
            this._super.apply(this, arguments);
        }
    }
});

});