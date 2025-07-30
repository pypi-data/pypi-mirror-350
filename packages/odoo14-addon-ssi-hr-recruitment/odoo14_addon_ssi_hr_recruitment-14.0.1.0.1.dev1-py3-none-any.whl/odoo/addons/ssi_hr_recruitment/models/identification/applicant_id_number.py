# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ApplicantIDNumber(models.Model):
    _name = "applicant.id_number"
    _description = "Applicant ID Number"

    applicant_id = fields.Many2one(
        string="Applicant",
        comodel_name="recruitment_applicant",
        required=True,
        ondelete="cascade",
        index=True,
        copy=False,
    )
    name = fields.Char(
        string="ID Number",
        required=True,
        help="The ID itself. For example, Driver License number of this person",
    )
    category_id = fields.Many2one(
        string="Category",
        required=True,
        comodel_name="res.partner.id_category",
        help="ID type defined in configuration. For example, Driver License",
    )
    issued_id = fields.Many2one(
        string="Issued by",
        comodel_name="res.partner",
        help="Another partner, who issued this ID. For example, Traffic "
        "National Institution",
    )
    place_issuance = fields.Char(
        string="Place of Issuance",
        help="The place where the ID has been issued. For example the country "
        "for passports and visa",
    )
    date_issued = fields.Date(
        string="Issued on",
        help="Issued date. For example, date when person approved his driving "
        "exam, 21/10/2009",
    )
    valid_from = fields.Date(
        string="Valid from", help="Validation period stating date."
    )
    valid_until = fields.Date(
        string="Valid until",
        help="Expiration date. For example, date when person needs to renew "
        "his driver license, 21/10/2019",
    )
