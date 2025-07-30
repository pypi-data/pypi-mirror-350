# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ApplicantExperience(models.Model):
    _name = "applicant.experience"
    _inherit = "applicant.experience.mixin"
    _description = "Applicant's Professional Experience"

    job_position = fields.Char(
        string="Job Position",
    )
    job_level = fields.Char(
        string="Job Level",
    )
