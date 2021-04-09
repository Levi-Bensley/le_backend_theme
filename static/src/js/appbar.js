odoo.define('le_backend_theme.AppBar', function (require) {
    "use strict";
    
    var core = require('web.core');
    var config = require("web.config");
    
    var Widget = require('web.Widget');
    
    var _t = core._t;
    var QWeb = core.qweb;
    
    var AppsBar = Widget.extend({
        events: _.extend({}, Widget.prototype.events, {
            'click .nav-link': '_onAppsMenuItemClicked',
        }),
        template: "le_backend_theme.AppBarMenu",
        init: function (parent, menu) {
            this._super.apply(this, arguments);
            this._apps = _.map(menu.children, function (app) {
                return {
                    actionID: parseInt(app.action.split(',')[1]),
                    web_icon_data: app.web_icon_data,
                    menuID: app.id,
                    name: app.name,
                    xmlID: app.xmlid,
                };
            });
        },
        getApps: function () {
            return this._apps;
        },
        _openApp: function (app) {
            this.trigger_up('app_clicked', {
                action_id: app.actionID,
                menu_id: app.menuID,
            });
        },
        _onAppsMenuItemClicked: function (ev) {
            var $target = $(ev.currentTarget);
            var actionID = $target.data('action-id');
            var menuID = $target.data('menu-id');
            var app = _.findWhere(this._apps, {
                actionID: actionID,
                menuID: menuID 
            });
            this._openApp(app);
            ev.preventDefault();
            $target.blur();
        },
    });
    
    return AppsBar;
    
    });