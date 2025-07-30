from odoo import fields, models, tools


class TestMassMailing(models.TransientModel):
    _inherit = "mailing.mailing.test"
    partner_email_to = fields.Many2one(
        "res.partner", "Test Partner", domain=[("mass_mailing_contacts_count", ">", 0)]
    )

    def send_mail_test(self):
        self.ensure_one()
        mails = self.env["mail.mail"]
        mailing = self.mass_mailing_id
        test_emails = tools.email_split(self.partner_email_to.email)
        mass_mail_layout = self.env.ref("mass_mailing.mass_mailing_mail_layout")
        contact = self.partner_email_to.mass_mailing_contact_ids[0]
        for test_mail in test_emails:
            body = self.env["mail.template"]._render_template(
                self.mass_mailing_id.body_html,
                "mail.mass_mailing.contact",
                [contact.id],
                post_process=True,
            )
            # Convert links in absolute URLs before the application of the shortener
            body = self.env["mail.thread"].message_parse(body)['body']
            body = tools.html_sanitize(
                body, sanitize_attributes=True, sanitize_style=True
            )
            mail_values = {
                "email_from": mailing.email_from,
                "reply_to": mailing.reply_to,
                "email_to": test_mail,
                "subject": mailing.name,
                "body_html": self.env['ir.qweb']._render(
                    mass_mail_layout, {"body": body}, minimal_qcontext=True
                ),
                "notification": True,
                "mailing_id": mailing.id,
                "attachment_ids": [
                    (4, attachment.id) for attachment in mailing.attachment_ids
                ],
                "auto_delete": True,
                "mail_server_id": mailing.mail_server_id.id,
            }
            mail = self.env["mail.mail"].create(mail_values)
            mails |= mail
        mails.send()
        return True
