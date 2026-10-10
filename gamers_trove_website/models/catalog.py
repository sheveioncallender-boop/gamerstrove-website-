from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    gt_featured = fields.Boolean('Feature on Trove homepage', copy=False)
    gt_demo = fields.Boolean('Trove demo product', copy=False)
    gt_badge = fields.Char('Storefront label', translate=True, help='Optional label, such as Staff pick. Leave blank to hide.')


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'
    gt_featured = fields.Boolean('Show in Trove categories', copy=False)
    gt_icon = fields.Selection([
        ('cards', 'Cards'), ('magic', 'Magic'), ('dice', 'Dice'),
        ('board', 'Board games'), ('gift', 'Collectibles'), ('shield', 'Accessories'),
    ], default='cards', string='Category symbol')


class EventEvent(models.Model):
    _inherit = 'event.event'
    gt_featured = fields.Boolean('Feature on Trove homepage', copy=False)
    gt_demo = fields.Boolean('Trove demo tournament', copy=False)
    gt_game = fields.Char('Game / format', translate=True)
    gt_card_image = fields.Image('Homepage tournament image', max_width=1600, max_height=1600)
