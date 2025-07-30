# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class MixinStateChangeHistory(models.AbstractModel):
    _name = "mixin.state_change_history"
    _description = "Mixin Object for State Change History"

    _automatically_insert_state_change_history_page = False
    _state_change_history_xpath_reference = "//page[last()]"

    state_change_history_ids = fields.One2many(
        string="States Change History",
        comodel_name="state_change_history",
        inverse_name="res_id",
        domain=lambda self: [("model", "=", self._name)],
        auto_join=True,
    )

    def _prepare_state_change_history(self, state_to, cancel_reason_id):
        self.ensure_one()
        obj_base_cancel_reason = self.env["base.cancel_reason"]
        Model = self.env["ir.model"]
        models = Model.search([("model", "=", self._name)])
        reason = "-"
        if cancel_reason_id:
            reason_id = obj_base_cancel_reason.search([
                ("id", "=", cancel_reason_id)
            ])
            reason = reason_id.name
        values = {
            "model_id": models[0].id,
            "res_id": self.id,
            "user_id": self.env.user.id,
            "state_from": self.state,
            "state_to": state_to,
            "date_change": fields.Datetime.now(),
            "reason": reason,
        }
        return values

    def create_state_change_history(self, state_to, cancel_reason_id=False):
        self.ensure_one()
        obj_state_change_history = self.env["state_change_history"]
        obj_state_change_history.create(self._prepare_state_change_history(state_to, cancel_reason_id))
        return True

    def write(self, vals):
        for rec in self:
            if "state" in vals:
                if "cancel_reason_id" in vals:
                    rec.sudo().create_state_change_history(
                        vals.get("state", False),
                        vals.get("cancel_reason_id", False),
                    )   
                else:
                    rec.sudo().create_state_change_history(vals.get("state", False))
        return super(MixinStateChangeHistory, self).write(vals)

    @ssi_decorator.insert_on_form_view()
    def _state_change_history_insert_form_element(self, view_arch):
        if self._automatically_insert_state_change_history_page:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id="ssi_state_change_history_mixin.state_change_history",
                xpath=self._state_change_history_xpath_reference,
                position="after",
            )
        return view_arch
