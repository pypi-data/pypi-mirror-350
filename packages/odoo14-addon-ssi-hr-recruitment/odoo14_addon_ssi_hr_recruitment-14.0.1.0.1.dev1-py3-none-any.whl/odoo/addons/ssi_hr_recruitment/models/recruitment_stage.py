# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RecruitmentStage(models.Model):
    _name = "recruitment_stage"
    _description = "Recruitment Stage"
    _inherit = ["mixin.master_data"]
    _order = "sequence"

    name = fields.Char(
        string="Stage",
        help="Name of the stage.",
    )
    job_ids = fields.Many2many(
        string="Jobs",
        comodel_name="hr.job",
        relation="rel_recruitment_stage_2_job",
        column1="stage_id",
        column2="job_id",
        help="Specific jobs that uses this stage. Other jobs will not use this stage.",
    )

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Gives the sequence order when displaying a list of stages.",
    )
