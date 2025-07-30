from odoo.addons.somconnexio.tests.sc_test_case import SCTestCase
from odoo.tests import common, patch
from odoo.exceptions import ValidationError


class MassMailingTest(SCTestCase):
    def test_untranslated_name(self):
        mass_mailing = self.browse_ref("mass_mailing.mass_mail_1")
        mass_mailing.with_context(lang="en_US").name = "test_en"
        mass_mailing.with_context(lang="es_ES").name = "test_es"
        self.assertEqual(mass_mailing.with_context(lang="en_US").name, "test_es")


class TestMassMailingCommon(common.TransactionCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.partner_es_a = self.env["res.partner"].create(
            {
                "name": "Mark Foreman",
                "email": "mark.foreman@example.com",
            }
        )
        self.partner_es_b = self.env["res.partner"].create(
            {
                "name": "Lucy Down",
                "email": "lucy.down@example.com",
            }
        )
        mailing_list = self.env["mailing.list"].create(
            {
                "name": "A",
                "contact_ids": [
                    (
                        0,
                        0,
                        {
                            "name": self.partner_es_a.name,
                            "email": self.partner_es_a.email,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": self.partner_es_b.name,
                            "email": self.partner_es_b.email,
                        },
                    ),
                ],
            }
        )
        self.mass_mailing = self.env["mailing.mailing"].create(
            {
                "subject": "test",
                "reply_to_mode": "new",
                "reply_to": "Administrator <admin@yourcompany.example.com>",
                "mailing_model_id": self.env.ref(
                    "mass_mailing.model_mailing_list"
                ).id,
                "mailing_domain": "[('list_ids', 'in', [%d])]" % mailing_list.id,
                "contact_list_ids": [[6, False, [mailing_list.id]]],
                "name": "sdf",
                "body_html": """
        Hi,
        % set url = "www.odoo.com"
        % set httpurl = "https://www.odoo.eu"
        Website0: <a id="url0" href="https://www.odoo.tz/my/${object.name}">
            https://www.odoo.tz/my/${object.name}
        </h1>
        Website1: <a id="url1" href="https://www.odoo.be">https://www.odoo.be</h1>
        Website2: <a id="url2" href="https://${url}">https://${url}</h1>
        Website3: <a id="url3" href="${httpurl}">${httpurl}</h1>
        Email: <a id="url4" href="mailto:test@odoo.com">test@odoo.com</h1>
                    """,
                "schedule_date": False,
                "state": "draft",
                "keep_archives": True,
            }
        )

    @patch(
        "odoo.addons.mass_mailing_somconnexio.models.mass_mailing.MassMailing.validate_opt_out"  # noqa
    )
    @patch("odoo.addons.mass_mailing.models.mailing.MassMailing.action_put_in_queue")
    def test_validate_lang_all_partners_same_lang(self, _, __):
        self.partner_es_a.lang = "es_ES"
        self.partner_es_b.lang = "es_ES"
        self.mass_mailing.lang = "es_ES"
        self.assertTrue(self.mass_mailing.action_put_in_queue())

    @patch(
        "odoo.addons.mass_mailing_somconnexio.models.mass_mailing.MassMailing.validate_opt_out"  # noqa
    )
    @patch("odoo.addons.mass_mailing.models.mailing.MassMailing.action_put_in_queue")
    def test_validate_partners_different_lang(self, _, __):
        self.partner_es_a.lang = "es_ES"
        self.partner_es_b.lang = "ca_ES"
        self.mass_mailing.lang = "es_ES"
        self.assertRaises(ValidationError, self.mass_mailing.action_put_in_queue)

    @patch(
        "odoo.addons.mass_mailing_somconnexio.models.mass_mailing.MassMailing.validate_opt_out"  # noqa
    )
    @patch(
        "odoo.addons.mass_mailing.models.mailing.MassMailing.action_schedule"
    )
    def test_validate_partners_different_lang_action_schedule(self, _, __):
        self.partner_es_a.lang = "es_ES"
        self.partner_es_b.lang = "ca_ES"
        self.mass_mailing.lang = "es_ES"
        with self.assertRaises(ValidationError):
            self.mass_mailing.action_schedule()

    @patch(
        "odoo.addons.mass_mailing_somconnexio.models.mass_mailing.MassMailing.validate_opt_out"  # noqa
    )
    @patch(
        "odoo.addons.mass_mailing.models.mailing.MassMailing.action_test"
    )
    def test_validate_partners_different_lang_action_test_mailing(self, _, __):
        self.partner_es_a.lang = "es_ES"
        self.partner_es_b.lang = "ca_ES"
        self.mass_mailing.lang = "es_ES"
        with self.assertRaises(ValidationError):
            self.mass_mailing.action_test()

    @patch(
        "odoo.addons.mass_mailing_somconnexio.models.mass_mailing.MassMailing.validate_lang"  # noqa
    )
    @patch("odoo.addons.mass_mailing.models.mailing.MassMailing.action_put_in_queue")
    def test_validate_partners_indispensable(self, _, __):
        self.partner_es_a.only_indispensable_emails = True
        self.partner_es_b.only_indispensable_emails = False
        self.mass_mailing.indispensable_email = True
        self.assertTrue(self.mass_mailing.action_put_in_queue())

    @patch(
        "odoo.addons.mass_mailing_somconnexio.models.mass_mailing.MassMailing.validate_lang"  # noqa
    )
    @patch("odoo.addons.mass_mailing.models.mailing.MassMailing.action_put_in_queue")
    def test_validate_partners_not_indispensable(self, _, __):
        self.partner_es_a.only_indispensable_emails = True
        self.partner_es_b.only_indispensable_emails = False
        self.mass_mailing.indispensable_email = False
        self.assertRaises(ValidationError, self.mass_mailing.action_put_in_queue)

    @patch("odoo.addons.mass_mailing.models.mailing.MassMailing.action_put_in_queue")
    def test_validate_partners_default_case(self, _):
        self.assertTrue(self.mass_mailing.action_put_in_queue())
