from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        # Add a print or a logger to ensure the method is called correctly
        _logger.info("Overridden action_sold method called for property ID: %s", self.id)
        
        # Step 1: Call the super method to ensure any parent logic is executed
        super(EstateProperty, self).action_sold()
        
        # Step 2: Create an empty customer invoice (account.move)
        # Loop through each record (property) in case multiple properties are sold at once
        for record in self:
            partner_id = record.buyer_id.id  # Assuming the buyer is stored in buyer_id
            
            if not partner_id:
                raise ValueError(f"No buyer found for property {record.name} (ID: {record.id})")
            
            # Define the values for the account.move (Customer Invoice)
            invoice_vals = {
            'partner_id': record.buyer_id.id,  # Use buyer_id to associate the invoice with the buyer
            'move_type': 'out_invoice',  # Customer invoice type
            'invoice_line_ids': [
                (0, 0, {
                    'name': 'Selling Price',
                    'quantity': 1,
                    'price_unit': record.selling_price * 0.06,  # Ensure correct selling_price field is used
                }),
                (0, 0, {
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100,  # Static fee value
                })
            ]
        }
            
            # Create the account.move record (invoice)
            invoice = self.env['account.move'].create(invoice_vals)
            
            _logger.info(f"Invoice created for property {record.name} (ID: {record.id}) with invoice ID: {invoice.id}")

        return True
