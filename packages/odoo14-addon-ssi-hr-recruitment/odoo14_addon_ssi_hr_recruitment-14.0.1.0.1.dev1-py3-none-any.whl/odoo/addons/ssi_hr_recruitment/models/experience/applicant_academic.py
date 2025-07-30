# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ApplicantAcademic(models.Model):
    _name = "applicant.academic"
    _inherit = "applicant.experience.mixin"
    _description = "Applicant's Academic Experience"

    diploma = fields.Char(
        string="Diploma Number",
    )
    education_level_id = fields.Many2one(
        string="Education Level",
        comodel_name="partner.formal_education_level",
    )
    field_of_study_id = fields.Many2one(
        string="Field of Study",
        comodel_name="partner.field_of_study",
    )
    gpa = fields.Float(
        string="Latest GPA",
    )
    activities = fields.Text(
        string="Activities and associations",
    )
