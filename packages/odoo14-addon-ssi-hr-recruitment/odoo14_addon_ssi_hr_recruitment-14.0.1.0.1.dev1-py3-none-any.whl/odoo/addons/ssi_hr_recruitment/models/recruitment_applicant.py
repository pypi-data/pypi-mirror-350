# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import datetime

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class RecruitmentApplicant(models.Model):
    _name = "recruitment_applicant"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_cancel",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_terminate",
        "mixin.state_change_history",
    ]
    _description = "Applicant"

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

    # State Change History
    _automatically_insert_state_change_history_page = True

    def _compute_policy(self):
        _super = super(RecruitmentApplicant, self)
        _super._compute_policy()

    recruit_ok = fields.Boolean(
        string="Can Recruit",
        compute="_compute_policy",
        compute_sudo=True,
        help="""Recruit policy

* If active user can see and execute 'Recruit' button""",
    )

    @api.model
    def _get_policy_field(self):
        res = super(RecruitmentApplicant, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "recruit_ok",
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
            ("recruited", "Recruited"),
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

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        job_id = self._context.get("default_job_id")
        search_domain = [("job_ids", "=", False)]
        if job_id:
            search_domain = ["|", ("job_ids", "=", job_id)] + search_domain
        if stages:
            search_domain = ["|", ("id", "in", stages.ids)] + search_domain

        stage_ids = stages._search(
            search_domain, order=order, access_rights_uid=SUPERUSER_ID
        )
        return stages.browse(stage_ids)

    @api.depends(
        "job_id",
        "state",
    )
    def _compute_stage(self):
        for record in self:
            if not record.stage_id:
                if record.job_id and record.state == "open":
                    stage_ids = (
                        self.env["recruitment_stage"]
                        .search(
                            [
                                "|",
                                ("job_ids", "=", False),
                                ("job_ids", "=", record.job_id.id),
                            ],
                            order="sequence asc",
                            limit=1,
                        )
                        .ids
                    )
                    record.stage_id = stage_ids[0] if stage_ids else False
                else:
                    record.stage_id = False

    stage_id = fields.Many2one(
        string="Stage",
        comodel_name="recruitment_stage",
        ondelete="restrict",
        tracking=True,
        compute="_compute_stage",
        store=True,
        readonly=False,
        domain="['|', ('job_ids', '=', False), ('job_ids', '=', job_id)]",
        copy=False,
        index=True,
        group_expand="_read_group_stage_ids",
    )

    @api.depends(
        "job_id",
        "date",
    )
    def _compute_allowed_vacancy_ids(self):
        for record in self:
            result = []
            if record.job_id and record.date:
                vacancy_ids = self.env["recruitment_vacancy"].search(
                    [
                        ("job_id", "=", record.job_id.id),
                        ("date_start", "<=", record.date),
                        ("date_end", ">=", record.date),
                        ("state", "=", "open"),
                    ]
                )
                result = vacancy_ids.ids

            record.allowed_vacancy_ids = result

    allowed_vacancy_ids = fields.Many2many(
        string="Allowed Vacancies",
        comodel_name="recruitment_vacancy",
        compute="_compute_allowed_vacancy_ids",
        compute_sudo=True,
        store=False,
    )
    vacancy_id = fields.Many2one(
        string="# Vacancy",
        comodel_name="recruitment_vacancy",
        required=True,
        ondelete="cascade",
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        readonly=True,
        copy=False,
    )

    @api.depends(
        "employee_id",
    )
    def _compute_is_employee_created(self):
        self.is_employee_created = False
        if self.employee_id:
            self.is_employee_created = True

    is_employee_created = fields.Boolean(
        string="Employee Created",
        compute="_compute_is_employee_created",
    )
    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    expected_salary = fields.Float(
        string="Expected Salary",
    )

    # APPLICANT INFORMATION FIELDS
    applicant_name = fields.Char(
        string="Applicant's Name",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    # GENERAL
    work_phone = fields.Char(
        string="Work Phone",
    )
    mobile_phone = fields.Char(
        string="Work Mobile",
    )
    work_email = fields.Char(
        string="Work Email",
    )
    street = fields.Char(
        string="Street",
    )
    street2 = fields.Char(
        string="2nd Street",
    )
    zip = fields.Char(
        string="Zip",
        change_default=True,
    )
    city = fields.Char(
        string="City",
    )
    address_country_id = fields.Many2one(
        string="Country",
        comodel_name="res.country",
        ondelete="restrict",
    )
    state_id = fields.Many2one(
        string="State",
        comodel_name="res.country.state",
        ondelete="restrict",
        domain="[('country_id', '=?', country_id)]",
    )
    # PERSONAL INFORMATION
    marital = fields.Selection(
        string="Marital Status",
        selection=[
            ("single", "Single"),
            ("married", "Married"),
            ("cohabitant", "Legal Cohabitant"),
            ("widower", "Widower"),
            ("divorced", "Divorced"),
        ],
        default="single",
    )
    spouse_complete_name = fields.Char(
        string="Spouse Complete Name",
    )
    spouse_birthdate = fields.Date(
        string="Spouse Birthdate",
    )
    children = fields.Integer(
        string="Number of Children",
    )
    country_id = fields.Many2one(
        string="Nationality (Country)",
        comodel_name="res.country",
    )
    gender = fields.Selection(
        string="Gender",
        selection=[("male", "Male"), ("female", "Female"), ("other", "Other")],
    )
    place_of_birth = fields.Char(
        string="Place of Birth",
    )
    country_of_birth = fields.Many2one(
        string="Country of Birth",
        comodel_name="res.country",
    )
    birthday = fields.Date(
        string="Date of Birth",
    )
    birth_state_id = fields.Many2one(
        string="Birth state",
        comodel_name="res.country.state",
    )
    blood_type = fields.Selection(
        string="Blood Type (ABO)",
        selection=[
            ("A", "A"),
            ("B", "B"),
            ("0", "O"),
            ("AB", "AB"),
        ],
        required=False,
    )
    blood_type_rhesus = fields.Selection(
        string="Blood Type (Rh)",
        selection=[
            ("positive", "+"),
            ("negative", "-"),
        ],
        required=False,
    )
    religion_id = fields.Many2one(
        string="Religion",
        comodel_name="res_partner_religion",
    )
    ethnicity_id = fields.Many2one(
        string="Ethnicity",
        comodel_name="res_partner_ethnicity",
    )
    # EXPERIENCES
    academic_ids = fields.One2many(
        comodel_name="applicant.academic",
        inverse_name="applicant_id",
        string="Academic experiences",
        help="Academic experiences",
    )
    certification_ids = fields.One2many(
        comodel_name="applicant.certification",
        inverse_name="applicant_id",
        string="Certifications",
        help="Certifications",
    )
    experience_ids = fields.One2many(
        comodel_name="applicant.experience",
        inverse_name="applicant_id",
        string="Professional Experiences",
        help="Professional Experiences",
    )
    # LANGUAGES
    language_ids = fields.One2many(
        string="Languages",
        comodel_name="applicant.language",
        inverse_name="applicant_id",
        help="Languages",
    )
    # ID NUMBERS
    id_number_ids = fields.One2many(
        string="Identification Numbers",
        comodel_name="applicant.id_number",
        inverse_name="applicant_id",
        help="Identification Numbers",
    )
    # Stages
    applicant_stage_ids = fields.One2many(
        string="Stages",
        comodel_name="recruitment_applicant_stage",
        inverse_name="applicant_id",
        help="Stages",
    )

    def _prepare_partner_address(self):
        self.ensure_one()
        data = {
            "name": self.applicant_name,
            "street": self.street,
            "street2": self.street2,
            "zip": self.zip,
            "city": self.city,
            "state_id": self.state_id and self.state_id.id or False,
            "country_id": self.address_country_id
            and self.address_country_id.id
            or False,
        }
        return data

    def _prepare_partner_personal(self):
        self.ensure_one()
        data = {
            "gender": self.gender,
            "birth_city": self.place_of_birth,
            "birthdate_date": self.birthday,
            "blood_type": self.blood_type,
            "blood_type_rhesus": self.blood_type_rhesus,
            "nationality_id": self.country_id and self.country_id.id or False,
            "religion_id": self.religion_id and self.religion_id.id or False,
            "ethnicity_id": self.ethnicity_id and self.ethnicity_id.id or False,
            "birth_country_id": self.country_of_birth
            and self.country_of_birth.id
            or False,
            "birth_state_id": self.birth_state_id and self.birth_state_id.id or False,
        }
        return data

    def _prepare_partner_academic(self, record, partner_id):
        self.ensure_one()
        data = {
            "name": record.name,
            "partner_id": partner_id.id,
            "date_start": record.date_start,
            "date_end": record.date_end,
            "partner_address_id": record.partner_address_id.id,
            "location": record.location,
            "expire": record.expire,
            "note": record.note,
            "diploma": record.diploma,
            "education_level_id": record.education_level_id.id,
            "field_of_study_id": record.field_of_study_id.id,
            "gpa": record.gpa,
            "activities": record.activities,
        }
        return data

    def _prepare_partner_certification(self, record, partner_id):
        self.ensure_one()
        data = {
            "name": record.name,
            "partner_id": partner_id.id,
            "date_start": record.date_start,
            "date_end": record.date_end,
            "partner_address_id": record.partner_address_id.id,
            "location": record.location,
            "expire": record.expire,
            "note": record.note,
            "certification": record.certification,
        }
        return data

    def _prepare_partner_experience(self, record, partner_id):
        self.ensure_one()
        data = {
            "name": record.name,
            "partner_id": partner_id.id,
            "date_start": record.date_start,
            "date_end": record.date_end,
            "partner_address_id": record.partner_address_id.id,
            "location": record.location,
            "expire": record.expire,
            "note": record.note,
            "job_position": record.job_position,
            "job_level": record.job_level,
        }
        return data

    def _prepare_partner_language(self, record, partner_id):
        self.ensure_one()
        data = {
            "name": record.name,
            "description": record.description,
            "partner_id": partner_id.id,
            "read_rating": record.read_rating,
            "write_rating": record.write_rating,
            "speak_rating": record.speak_rating,
            "listen_rating": record.listen_rating,
        }
        return data

    def _prepare_partner_id_number(self, record, partner_id):
        self.ensure_one()
        data = {
            "name": record.name,
            "category_id": record.category_id.id,
            "partner_id": partner_id.id,
            "partner_issued_id": record.issued_id.id,
            "place_issuance": record.place_issuance,
            "date_issued": record.date_issued,
            "valid_from": record.valid_from,
            "valid_until": record.valid_until,
            "status": "draft",
        }
        return data

    def _prepare_partner_data(self):
        self.ensure_one()
        data = {}
        data.update(self._prepare_partner_address())
        data.update(self._prepare_partner_personal())
        # raise ValidationError(_("%s") % data)
        return data

    def _prepare_employee_data(self, partner_id):
        self.ensure_one()
        data = {
            "name": self.applicant_name,
            "date_join": datetime.now().strftime("%Y-%m-%d"),
            "address_home_id": partner_id.id,
            "marital": self.marital,
            "spouse_complete_name": self.spouse_complete_name,
            "spouse_birthdate": self.spouse_birthdate,
            "children": self.children,
            "work_phone": self.work_phone,
            "mobile_phone": self.mobile_phone,
            "work_email": self.work_email,
        }
        return data

    def action_recruit(self):
        obj_employee = self.env["hr.employee"]
        obj_res_partner = self.env["res.partner"]
        for record in self:
            if (
                record.vacancy_id.applicant_recruited
                == record.vacancy_id.applicant_number
            ):
                error_message = """
                Document Type: %s
                Database ID: %s
                Expected New Employees: %s
                Problem: Recruitment has reached the expected new employees.
                """ % (
                    self._description.lower(),
                    record.id,
                    record.vacancy_id.applicant_number,
                )
                raise ValidationError(_(error_message))

            try:
                if not record.employee_id:
                    partner_id = obj_res_partner.create(record._prepare_partner_data())
                    employee_id = obj_employee.create(
                        record._prepare_employee_data(partner_id)
                    )
                    # EXPERIENCES
                    if record.academic_ids:
                        for academic in record.academic_ids:
                            self.env["partner.academic"].create(
                                record._prepare_partner_academic(academic, partner_id)
                            )
                    if record.certification_ids:
                        for certification in record.certification_ids:
                            self.env["partner.certification"].create(
                                record._prepare_partner_certification(
                                    certification, partner_id
                                )
                            )
                    if record.experience_ids:
                        for experience in record.experience_ids:
                            self.env["partner.experience"].create(
                                record._prepare_partner_experience(
                                    experience, partner_id
                                )
                            )
                    # LANGUANGES
                    if record.language_ids:
                        for language in record.language_ids:
                            self.env["partner.language"].create(
                                record._prepare_partner_language(language, partner_id)
                            )
                    # ID NUMBERS
                    if record.id_number_ids:
                        for id_number in record.id_number_ids:
                            self.env["res.partner.id_number"].create(
                                record._prepare_partner_id_number(id_number, partner_id)
                            )
                else:
                    error_message = _("Duplicate employee")
                    raise ValidationError(error_message)
            except Exception as e:
                error_message = _(
                    """
                Context: Creating a new data
                Model: hr.employee
                Problem: %s
                Solution: Please contact administrator
                """
                    % (e)
                )
                raise ValidationError(error_message)
            record.write(
                {
                    "employee_id": employee_id.id,
                    "state": "recruited",
                }
            )

    @ssi_decorator.post_approve_action()
    def _populate_applicant_stage_ids(self):
        if self.applicant_stage_ids:
            self.mapped("applicant_stage_ids").unlink()

        stage_ids = self.env["recruitment_stage"].search(
            [
                "|",
                ("job_ids", "=", False),
                ("job_ids", "=", self.job_id.id),
            ],
            order="sequence asc",
        )
        if stage_ids:
            for stage in stage_ids:
                self.env["recruitment_applicant_stage"].create(
                    {
                        "applicant_id": self.id,
                        "stage_id": stage.id,
                    }
                )

    @api.onchange(
        "job_id",
        "date",
    )
    def onchange_vacancy_id(self):
        self.vacancy_id = False


class RecruitmentApplicantStage(models.Model):
    _name = "recruitment_applicant_stage"
    _description = "Applicant Stage"

    applicant_id = fields.Many2one(
        string="Applicant",
        comodel_name="recruitment_applicant",
        required=True,
        ondelete="cascade",
        index=True,
        copy=False,
    )
    stage_id = fields.Many2one(
        string="Stage",
        comodel_name="recruitment_stage",
    )
    result_id = fields.Many2one(
        string="Result",
        comodel_name="recruitment_stage_result",
    )

    @api.depends(
        "applicant_id",
        "applicant_id.stage_id",
    )
    def _compute_position(self):
        for record in self:
            record.position = False
            if record.stage_id == record.applicant_id.stage_id:
                record.position = True

    position = fields.Boolean(
        string="Position",
        compute="_compute_position",
    )
    state = fields.Selection(
        string="States",
        related="applicant_id.state",
    )
    note = fields.Text(
        string="Note",
    )
