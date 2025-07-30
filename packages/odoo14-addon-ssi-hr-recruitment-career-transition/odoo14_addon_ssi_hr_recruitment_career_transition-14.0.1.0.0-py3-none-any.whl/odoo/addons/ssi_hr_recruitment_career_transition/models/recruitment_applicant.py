# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import datetime

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class RecruitmentApplicant(models.Model):
    _inherit = "recruitment_applicant"

    join_transition_id = fields.Many2one(
        string="Join Transition",
        comodel_name="employee_career_transition",
        readonly=True,
        copy=False,
    )

    def _prepare_employee_data(self, partner):
        _super = super(RecruitmentApplicant, self)
        res = _super._prepare_employee_data(partner)
        res["work_information_method"] = "career_transition"
        return res

    def _get_join_type_id(self):
        result = []
        company = self.env.company
        join_type_id = company.join_transition_type_id.id
        if join_type_id:
            result = join_type_id
        return result

    def _prepare_career_transition_data(self, employee_id):
        self.ensure_one()
        data = {}
        join_type_id = self._get_join_type_id()
        if join_type_id:
            data = {
                "employee_id": employee_id.id,
                "type_id": join_type_id,
                "effective_date": datetime.now().strftime("%Y-%m-%d"),
            }
        else:
            error_message = _("Join Transition Type not define on company")
            raise ValidationError(error_message)
        return data

    def action_recruit(self):
        _super = super(RecruitmentApplicant, self)
        res = _super.action_recruit()
        obj_career_transition = self.env["employee_career_transition"]
        for record in self:
            try:
                career_transition_id = obj_career_transition.create(
                    record._prepare_career_transition_data(record.employee_id)
                )
                ctx = {"bypass_policy_check": True}
                career_transition_id.with_context(ctx).action_done()
            except Exception as e:
                error_message = _(
                    """
                Context: Creating a new data
                Model: employee_career_transition
                Problem: %s
                Solution: Please contact administrator
                """
                    % (e)
                )
                raise ValidationError(error_message)
            record.write({"join_transition_id": career_transition_id.id})
        return res
