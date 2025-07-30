from odoo import models, fields, api, _
from odoo.addons.account_payment_partner.models.account_move import (
    AccountMove as APPAccountMove,
)
from ..services.account_invoice_process import (
    AccountInvoiceProcess,
)
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = "account.move"

    # TODO: Remove after stop invoicing with OC
    oc_taxes = fields.Char()
    oc_total = fields.Float()
    oc_untaxed = fields.Float()
    oc_total_taxed = fields.Float()
    #################
    payment_mode_type = fields.Char(compute="_compute_payment_mode_type", store=True)
    last_return_amount = fields.Float(compute="_compute_last_return_amount")
    account_id = fields.Many2one('account.account', copy=True)
    b2_file_id = fields.Char()
    invoice_tokenized_url = fields.Char()
    # Field check the invoicing with the OC results
    billing_run_id = fields.Char()

    # Field to send the invoices to the correct emails
    emails = fields.Char(
        string="Emails",
    )

    def create_invoice(self, **params):
        service = AccountInvoiceProcess(self.env)
        service.create(**params)

    @api.model
    def _prepare_refund(
        self, invoice, invoice_date=None, date=None, description=None, journal_id=None
    ):
        vals = super(APPAccountMove, self)._prepare_refund(
            invoice,
            invoice_date=invoice_date,
            date=date,
            description=description,
            journal_id=journal_id,
        )
        if invoice.move_type == "in_invoice":
            vals["partner_bank_id"] = invoice.partner_bank_id.id
        return vals

    def set_cooperator_effective(self, effective_date):
        if self.partner_id.share_ids.filtered(lambda rec: rec.share_number > 0):
            return True
        return super(AccountInvoice, self).set_cooperator_effective(effective_date)

    def action_post(self):
        to_post_invoices = self.filtered(lambda inv: inv.state != "posted")
        if to_post_invoices.filtered(lambda inv: not inv.journal_id.active):
            raise UserError(
                _("The journal of the invoice is archived, cannot be validated")
            )
        return super().action_post()

    def get_invoice_pdf(self):
        invoice_number = self.name
        return {
            "type": "ir.actions.act_url",
            "url": f"/web/binary/download_invoice?invoice_number={invoice_number}",
            "target": "new",
        }

    @api.depends("move_type")
    def _compute_payment_mode_type(self):
        for inv in self:
            if inv.move_type in ("out_invoice", "in_refund"):
                inv.payment_mode_type = "inbound"
            elif inv.move_type in ("out_refund", "in_invoice"):
                inv.payment_mode_type = "outbound"
            else:
                inv.payment_mode_type = False

    def _compute_last_return_amount(self):
        for inv in self:
            inv.last_return_amount = 0.0
            payment_returns = self.env['payment.return.line'].search([
                ('move_line_ids.move_id', '=', inv.id)
            ], order='date desc', limit=1)
            if payment_returns:
                inv.last_return_amount = abs(payment_returns.amount)
