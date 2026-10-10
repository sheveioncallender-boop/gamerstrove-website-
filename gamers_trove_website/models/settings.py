from odoo import fields, models
from odoo.exceptions import AccessError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    gt_brand_enabled = fields.Boolean(related='website_id.gt_brand_enabled', readonly=False)
    gt_demo_notice = fields.Boolean(related='website_id.gt_demo_notice', readonly=False)
    gt_phone = fields.Char(related='website_id.gt_phone', readonly=False)
    gt_whatsapp = fields.Char(related='website_id.gt_whatsapp', readonly=False)
    gt_email = fields.Char(related='website_id.gt_email', readonly=False)
    gt_address = fields.Text(related='website_id.gt_address', readonly=False)
    gt_hours = fields.Text(related='website_id.gt_hours', readonly=False)
    gt_instagram = fields.Char(related='website_id.gt_instagram', readonly=False)
    gt_facebook = fields.Char(related='website_id.gt_facebook', readonly=False)
    gt_announcement = fields.Char(related='website_id.gt_announcement', readonly=False)

    def action_gt_unpublish_demo(self):
        self.ensure_one()
        if not self.env.user.has_group('base.group_system'):
            raise AccessError(self.env._('Only administrators can retire the client demonstration.'))
        domain = [('gt_demo', '=', True), ('website_id', '=', self.website_id.id)]
        self.env['product.template'].search(domain).write({'is_published': False})
        self.env['event.event'].search(domain).write({'is_published': False})
        self.website_id.gt_demo_notice = False
        return {'type': 'ir.actions.client', 'tag': 'display_notification', 'params': {
            'title': self.env._('Demo retired'),
            'message': self.env._('Sample products and events are unpublished. Orders, attendees and real records are unchanged.'),
            'type': 'success', 'sticky': False,
        }}
