from odoo import http
from odoo.addons.mass_mailing.controllers import main


class MassMailingController(main.MassMailController):
    @http.route("/mail/mailing/unsubscribe", type="json", auth="none")
    def unsubscribe(self, mailing_id, opt_in_ids, opt_out_ids, email, res_id, token):
        partner = http.request.env["res.partner"].sudo().search([("email", "=", email)])
        if partner.exists():
            if not self._valid_unsubscribe_token(mailing_id, res_id, email, token):
                return "unauthorized"
            partner.write({"only_indispensable_emails": True})
            return True
        return "error"
