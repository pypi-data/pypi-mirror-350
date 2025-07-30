# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class RecruitmentVacancy(models.Model):
    _name = "recruitment_vacancy"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_cancel",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_terminate",
        "mixin.date_duration",
    ]
    _description = "Vacancy"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_open_button = False
    _automatically_insert_open_policy_fields = False

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "done_ok",
        "cancel_ok",
        "terminate_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "action_terminate",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_terminate",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    @api.model
    def _get_policy_field(self):
        res = super(RecruitmentVacancy, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "terminate_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("reject", "Reject"),
            ("terminate", "Terminate"),
            ("cancel", "Cancelled"),
        ],
    )

    job_id = fields.Many2one(
        string="Job Position",
        comodel_name="hr.job",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    applicant_number = fields.Integer(
        string="Expected New Employees",
        help="Number of new employees you expected to recruit.",
    )

    applicant_ids = fields.One2many(
        string="Applicants",
        comodel_name="recruitment_applicant",
        inverse_name="vacancy_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        copy=True,
    )

    @api.depends("applicant_ids")
    def _compute_total_applicant(self):
        for record in self:
            record.total_applicant = len(record.applicant_ids.ids)

    total_applicant = fields.Integer(
        string="Total Applicants",
        compute="_compute_total_applicant",
    )

    @api.depends(
        "applicant_ids",
        "applicant_ids.is_employee_created",
    )
    def _compute_total_applicant_recruited(self):
        for record in self:
            record.applicant_recruited = 0
            recruited = record.applicant_ids.filtered(lambda x: x.state == "recruited")
            if recruited:
                record.applicant_recruited = len(recruited.ids)

    applicant_recruited = fields.Integer(
        string="Recruited",
        compute="_compute_total_applicant_recruited",
        store=True,
    )

    @api.depends(
        "applicant_number",
        "applicant_recruited",
    )
    def _compute_all_recruited(self):
        for record in self:
            record.all_recruited = False
            if record.applicant_number == record.applicant_recruited:
                record.all_recruited = True

    all_recruited = fields.Boolean(
        string="All Recruited",
        compute="_compute_all_recruited",
        store=True,
    )
