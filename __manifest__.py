# -*- coding: utf-8 -*-
{
	'name': 'Walker Rubber Backend Theme',
	'version': '0.1',
	'summary': 'Custom Backend Theme for Walker Rubber',
	'category': 'Theme/Backend',
	'author': 'Levi Bensley',
	'company': 'Walker Rubber',
	'website': 'https://www.walker-rubber.co.uk',
	'depends': ['web', 'mail', 'web_responsive'],
	'data': [
		"template/assets.xml",
		"template/web.xml",
		"views/res_users.xml",
		"views/res_config_settings_view.xml",
	],
	'qweb': [
		'static/src/xml/*.xml',
	],
	'images': [
		'static/description/icon.png'
	],
	'installable': True,
}