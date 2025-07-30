# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StateChangeHistory(models.Model):
    _name = "state_change_history"
    _description = "State Change History"
    _order = "model_id, res_id, date_change desc"

    model_id = fields.Many2one(
        string="Referenced Model",
        comodel_name="ir.model",
        ondelete="cascade",
        index=True,
        required=False,
    )
    model = fields.Char(
        related="model_id.model",
        index=True,
        store=True,
    )
    res_id = fields.Integer(
        string="Related Document ID",
        index=True,
    )
    res_reference_id = fields.Reference(
        string="Document Reference",
        compute="_compute_res_reference_id",
        store=True,
        selection="_selection_res_reference_id",
    )
    user_id = fields.Many2one(
        string="User",
        comodel_name="res.users",
        required=True,
    )
    state_from = fields.Char(
        string="State From",
        required=True,
    )
    state_to = fields.Char(
        string="State To",
        required=True,
    )
    reason = fields.Char(
        string="Reason",
        required=True,
        default="-",
    )
    date_change = fields.Datetime(
        string="Date Change",
        required=True,
    )

    @api.model
    def _selection_res_reference_id(self):
        return [(model.model, model.name) for model in self.env["ir.model"].search([])]

    @api.depends(
        "model_id",
        "res_id",
    )
    def _compute_res_reference_id(self):
        for document in self:
            result = False
            if document.model_id and document.res_id:
                result = "%s,%s" % (document.model, document.res_id)
            document.res_reference_id = result
