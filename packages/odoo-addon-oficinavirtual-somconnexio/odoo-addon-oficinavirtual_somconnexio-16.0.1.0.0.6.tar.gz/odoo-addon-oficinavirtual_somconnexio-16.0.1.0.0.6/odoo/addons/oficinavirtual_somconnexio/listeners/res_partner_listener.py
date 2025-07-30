from odoo.addons.component.core import Component


class Partner(Component):
    _name = "partner.listener"
    _inherit = "base.event.listener"
    _apply_on = ["res.partner"]

    def on_record_create(self, record, fields=None):
        # Early return if is not a Contact(is the parent)
        if record.parent_id:
            return
        if record.is_customer:
            self.env["res.partner"].with_delay().create_user(record)
