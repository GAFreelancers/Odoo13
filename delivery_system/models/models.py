from odoo import models, fields, api, _
import datetime
from odoo.exceptions import AccessError, UserError, ValidationError
date_format = "%Y-%m-%d"



class DeliverySystem(models.Model):
    _name = 'delivery.new'

    name = fields.Char(string="Delivery Sequence", readonly=True, required=True, copy=False, default='New')

    state =  fields.Selection([('draft','Draft'),
                               ('confirm','Confirmed'),
                               ('packing','Preparing'),
                               ('billed','Billed'),
                               ('enroute','On The Way'),
                               ('cancel','cancelled'),
                               ('delivered','Delivered'),
                               ('done','Done')],string='Status', default='draft', track_visibility='onchange')

    ordered_on=fields.Datetime('Ordered On',default=datetime.datetime.now())
    confirmed_on=fields.Datetime('Confirmed On',readonly=True)
    packed_on=fields.Datetime('Packed On',readonly=True)
    billed_on=fields.Datetime('Billed On',readonly=True)
    enroute_on=fields.Datetime('Enroute On',readonly=True)
    cancelled_on=fields.Datetime('Cancelled On',readonly=True)
    delivered_on=fields.Datetime('Delivered On',readonly=True)
    completed_on=fields.Datetime('Completed On',readonly=True)

    customer_id = fields.Many2one('res.partner','Customer',required=1)
    customer_img=fields.Binary(related='customer_id.image_1920')
    phone=fields.Char(related='customer_id.phone',string='Phone')

    another_address=fields.Boolean('Deliver to another address ?')

    limit_reached=fields.Boolean('Limit')

    street=fields.Char(related='customer_id.street')
    street2=fields.Char(related='customer_id.street2')
    city=fields.Char(related='customer_id.city')
    state_id=fields.Many2one('res.country.state',related='customer_id.state_id')
    zip=fields.Char(related='customer_id.zip')
    country_id=fields.Many2one('res.country',related='customer_id.country_id')

    street1=fields.Char()
    street12=fields.Char()
    city1=fields.Char()
    state_id1=fields.Many2one('res.country.state')
    zip1=fields.Char()
    country_id1=fields.Many2one('res.country')

    order_line=fields.One2many('items.line','deliveries','Order Line')
    kanbancolor = fields.Integer('Color Index', compute="set_kanban_color")

    total=fields.Float('Total')


    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('delivery.new') or 'New'
        result = super(DeliverySystem, self).create(vals)
        return result


    def set_kanban_color(self):
        for record in self:
            kanbancolor = 0
            if record.state == 'draft':
                kanbancolor = 1
            elif record.state == 'confirm':
                kanbancolor = 2
            elif record.state == 'packing':
                kanbancolor = 3
            elif record.state == 'billed':
                kanbancolor = 4
            elif record.state == 'enroute':
                kanbancolor = 5
            elif record.state == 'cancel':
                kanbancolor = 6
            elif record.state == 'delivered':
                kanbancolor = 7
            elif record.state == 'done':
                kanbancolor = 8
            else:
                kanbancolor = 9
            record.kanbancolor = kanbancolor


    def action_confirm(self):
        total = 0
        for i in self.order_line:
            total = total + i.price_subtotal
        self.total = total
        self.state='confirm'
        self.confirmed_on=datetime.datetime.now()

    def action_prepare(self):
        self.state='packing'
        self.packed_on = datetime.datetime.now()

    def action_bill(self):
        self.state='billed'
        self.billed_on = datetime.datetime.now()

    def action_cancel(self):
        self.state='cancel'
        self.cancelled_on = datetime.datetime.now()

    def action_enroute(self):
        self.state='enroute'
        self.enroute_on = datetime.datetime.now()

    def action_delivered(self):
        self.state='delivered'
        self.delivered_on = datetime.datetime.now()

    def action_done(self):
        self.state='done'
        self.completed_on = datetime.datetime.now()

class Items(models.Model):
    _name= 'items.line'

    product_id=fields.Many2one('product.template','Product',required=True)
    name=fields.Text(string='Description')
    quantity=fields.Integer('Quantity',required=True)
    price_unit=fields.Float('Unit Price',required=True,related='product_id.list_price')
    price_subtotal=fields.Float('Sub Total')
    deliveries=fields.Many2one('delivery.new')

    @api.onchange('price_unit','quantity')
    def Total_Sub(self):
        self.price_subtotal=self.quantity * self.price_unit
