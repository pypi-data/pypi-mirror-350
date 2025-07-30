# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RecruitmentStageResult(models.Model):
    _name = "recruitment_stage_result"
    _inherit = ["mixin.master_data"]
    _description = "Recruitment Stage Result"

    name = fields.Char(
        string="Result",
    )
    code = fields.Char(
        default="/",
    )
