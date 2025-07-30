# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "State Change History Mixin",
    "version": "14.0.1.2.0",
    "category": "Administration",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "base",
        "ssi_decorator",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "templates/mixin_state_change_history_templates.xml",
        "views/state_change_history_views.xml",
    ],
}
