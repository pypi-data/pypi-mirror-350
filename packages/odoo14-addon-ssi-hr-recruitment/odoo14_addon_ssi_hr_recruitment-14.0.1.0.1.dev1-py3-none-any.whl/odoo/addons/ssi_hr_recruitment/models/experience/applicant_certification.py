# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ApplicantCertification(models.Model):
    _name = "applicant.certification"
    _inherit = "applicant.experience.mixin"
    _description = "Applicant's Certification Experience"

    certification = fields.Char(
        string="Certification Number",
        help="Certification Number",
    )
