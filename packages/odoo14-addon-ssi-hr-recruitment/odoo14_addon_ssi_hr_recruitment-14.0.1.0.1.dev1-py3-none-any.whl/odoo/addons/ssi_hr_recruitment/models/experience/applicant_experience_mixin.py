# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ApplicantExperienceMixin(models.AbstractModel):
    _name = "applicant.experience.mixin"
    _inherit = [
        "mail.activity.mixin",
        "mail.thread",
        "mixin.date_duration",
    ]
    _description = "Abstract Class for Applicant Experience"
    _date_end_required = False

    name = fields.Char(
        string="Name",
    )
    applicant_id = fields.Many2one(
        string="Applicant",
        comodel_name="recruitment_applicant",
        required=True,
        ondelete="cascade",
        index=True,
        copy=False,
    )
    partner_address_id = fields.Many2one(
        comodel_name="res.partner",
        string="Address",
        help="Employer, School, University, " "Certification Authority",
        domain="[('is_company', '!=', False)]",
    )
    location = fields.Char(
        string="Location",
        help="Location",
    )
    expire = fields.Boolean(
        string="Expire",
        help="Expire",
        default=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
