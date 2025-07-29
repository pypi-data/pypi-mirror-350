# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError
from odoo.tools.safe_eval import safe_eval

from odoo.addons.ssi_decorator import ssi_decorator


class AccountReceivablePenaltyComputation(models.Model):
    _name = "account.receivable_penalty_computation"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
        "mixin.company_currency",
        "mixin.state_change_history",
        "mixin.localdict",
    ]
    _description = "Account Receivable Penalty Computation"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _automatically_insert_state_change_history_page = True

    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    # FIELD
    penalty_id = fields.Many2one(
        string="# Penalty",
        comodel_name="account.receivable_penalty",
        required=False,
        ondelete="set null",
        readonly=True,
    )
    batch_id = fields.Many2one(
        string="# Batch",
        comodel_name="batch_receivable_penalty_computation",
        readonly=True,
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        domain=[
            ("parent_id", "=", False),
        ],
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "partner_id",
        "type_id",
    )
    def _compute_allowed_base_move_line_ids(self):
        AML = self.env["account.move.line"]
        for record in self:
            result = []
            if record.partner_id and record.type_id:
                ttype = record.type_id
                criteria = [
                    ("partner_id.id", "=", record.partner_id.id),
                    ("account_id.id", "in", ttype.account_ids.ids),
                    ("debit", ">", 0.0),
                    ("reconciled", "=", False),
                ]
                result = AML.search(criteria).ids
            record.allowed_base_move_line_ids = result

    allowed_base_move_line_ids = fields.Many2many(
        string="Allowed Base Move Line",
        comodel_name="account.move.line",
        compute="_compute_allowed_base_move_line_ids",
        store=False,
    )
    base_move_line_id = fields.Many2one(
        string="Base Move Line",
        comodel_name="account.move.line",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    base_move_id = fields.Many2one(
        string="# Base Accounting Entry",
        comodel_name="account.move",
        related="base_move_line_id.move_id",
        store=True,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="account.receivable_penalty_type",
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
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
    date_cutoff = fields.Date(
        string="Date Cutoff",
        compute="_compute_date_cutoff",
        store=True,
        compute_sudo=True,
    )
    days_overdue = fields.Integer(
        string="Days Overdue",
        compute="_compute_days_overdue",
        store=True,
        compute_sudo=True,
    )
    amount_residual = fields.Monetary(
        string="Residual Amount",
        compute="_compute_amount_residual",
        currency_field="company_currency_id",
        store=True,
        compute_sudo=True,
    )
    payment_amount_to_date = fields.Monetary(
        string="Payment Amount to Date",
        compute="_compute_amount_residual",
        currency_field="company_currency_id",
        store=True,
        compute_sudo=True,
    )
    payment_amount_at_date = fields.Monetary(
        string="Payment Amount at Date",
        compute="_compute_amount_residual",
        currency_field="company_currency_id",
        store=True,
        compute_sudo=True,
    )
    base_amount = fields.Monetary(
        string="Base Amount",
        currency_field="company_currency_id",
        required=True,
    )
    penalty_amount = fields.Monetary(
        string="Penalty Amount",
        currency_field="company_currency_id",
        required=True,
    )
    account_move_line_id = fields.Many2one(
        string="# Move Line",
        comodel_name="account.move.line",
        readonly=True,
        copy=False,
    )

    @api.model
    def _get_policy_field(self):
        res = super(AccountReceivablePenaltyComputation, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.constrains(
        "base_move_line_id",
        "type_id",
        "state",
    )
    def _constrains_max_limit(self):
        for record in self.sudo():
            if not record._check_max_limit() and record.state in [
                "confirm",
                "open",
                "done",
            ]:
                error_message = """
                Document Type: %s
                Context: Update document
                Database ID: %s
                Problem: Max penalty limit exceed
                Solution: Change document base move line or type
                """ % (
                    self._description.title(),
                    record.id,
                )
                raise UserError(_(error_message))

    @api.depends(
        "date",
        "type_id",
    )
    def _compute_date_cutoff(self):
        for record in self:
            offset = 0
            result = False
            if record.date and record.type_id:
                offset = record._calculate_date_cutoff()
                result = record.date + relativedelta(days=-offset)
            record.date_cutoff = result

    @api.depends(
        "base_move_line_id",
        "date_cutoff",
        "type_id",
    )
    def _compute_days_overdue(self):
        for record in self:
            result = 0
            if (
                record.base_move_line_id
                and record.date
                and record.base_move_line_id.date_maturity
            ):
                dt_date_due = record.base_move_line_id.date_maturity
                dt_date = record.date_cutoff
                result = (dt_date - dt_date_due).days
            record.days_overdue = result

    @api.depends(
        "base_move_line_id",
        "date",
        "date_cutoff",
    )
    def _compute_amount_residual(self):
        for record in self:
            amount_residual = payment_amount_to_date = payment_amount_at_date = 0.0
            if record.base_move_line_id and record.date_cutoff:
                base_ml = record.base_move_line_id
                lines = base_ml.matched_debit_ids.mapped(
                    "debit_move_id"
                ) + base_ml.matched_credit_ids.mapped("credit_move_id")
                line_ids = lines.ids
                criteria = [
                    ("id", "in", line_ids),
                    ("date", "<=", record.date_cutoff),
                ]
                payment_lines = self.env["account.move.line"].search(criteria)
                for payment_line in payment_lines:
                    amount_residual += payment_line.credit + payment_line.debit
                    if payment_line.date < record.date_cutoff:
                        payment_amount_to_date += payment_line.credit
                    elif payment_line.date == record.date_cutoff:
                        payment_amount_at_date += payment_line.credit
                amount_residual = base_ml.debit - amount_residual
            record.amount_residual = amount_residual
            record.payment_amount_to_date = payment_amount_to_date
            record.payment_amount_at_date = payment_amount_at_date

    @api.onchange(
        "type_id",
        "base_move_line_id",
        "date_cutoff",
    )
    def onchange_base_amount(self):
        self.base_amount = 0.0
        if self.type_id and self.base_move_line_id:
            self.base_amount = self._calculate_base_amount()

    @api.onchange(
        "base_amount",
        "type_id",
        "base_move_line_id",
        "date_cutoff",
    )
    def onchange_penalty_amount(self):
        self.penalty_amount = 0.0
        if self.type_id and self.base_move_line_id:
            self.penalty_amount = self._calculate_penalty_amount()

    def _check_max_limit(self):
        self.ensure_one()
        result = True
        if not self.type_id.limit_max_penalty_ok:
            return result

        PenaltyComputation = self.env["account.receivable_penalty_computation"]
        partner = self.partner_id.commercial_partner_id
        criteria = [
            ("partner_id.commercial_partner_id.id", "=", partner.id),
            ("type_id.id", "=", self.type_id.id),
            ("state", "in", ["confirm", "open", "done"]),
            ("base_move_line_id.id", "=", self.base_move_line_id.id),
        ]
        if PenaltyComputation.search_count(criteria) > self.type_id.max_penalty:
            result = False

        return result

    def _create_aml(self):
        self.ensure_one()
        obj_account_move_line = self.env["account.move.line"]
        aml = obj_account_move_line.with_context(check_move_validity=False).create(
            self._prepare_aml_data()
        )
        self.write(
            {
                "account_move_line_id": aml.id,
            }
        )

    def _calculate_date_cutoff(self):
        self.ensure_one()
        res = False
        localdict = self._get_default_localdict()
        try:
            ttype = self.type_id
            safe_eval(ttype.date_cutoff_python, localdict, mode="exec", nocopy=True)
            res = localdict["result"]
        except Exception as error:
            raise UserError(_("Error evaluating date cutoff conditions.\n %s") % error)
        return res

    def _calculate_base_amount(self):
        self.ensure_one()
        res = False
        localdict = self._get_default_localdict()
        try:
            ttype = self.type_id
            safe_eval(ttype.base_amount_python, localdict, mode="exec", nocopy=True)
            res = localdict["result"]
        except Exception as error:
            raise UserError(_("Error evaluating base amount conditions.\n %s") % error)
        return res

    def _calculate_penalty_amount(self):
        self.ensure_one()
        res = False
        localdict = self._get_default_localdict()
        try:
            ttype = self.type_id
            safe_eval(ttype.penalty_amount_python, localdict, mode="exec", nocopy=True)
            res = localdict["result"]
        except Exception as error:
            raise UserError(
                _("Error evaluating penalty amount conditions.\n %s") % error
            )
        return res

    def _prepare_aml_data(self):
        self.ensure_one()
        penalty = self.penalty_id
        debit, credit, amount_currency = self._get_aml_amount(
            penalty.company_currency_id
        )
        return {
            "move_id": penalty.move_id.id,
            "name": self.name,
            "partner_id": penalty.base_move_line_id.partner_id.id,
            "account_id": penalty.income_account_id.id,
            "quantity": 1.0,
            "price_unit": self.penalty_amount,
            "debit": debit,
            "credit": credit,
            "currency_id": penalty.company_currency_id.id,
            "amount_currency": amount_currency,
        }

    def _get_aml_amount(self, currency):
        self.ensure_one()
        debit = credit = amount = amount_currency = 0.0
        penalty = self.penalty_id
        move_date = penalty.date

        amount_currency = self.penalty_amount
        amount = currency.with_context(date=move_date).compute(
            amount_currency,
            penalty.company_currency_id,
        )

        if amount < 0.0:
            debit = abs(amount)
        else:
            credit = abs(amount)

        return debit, credit, amount_currency

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
