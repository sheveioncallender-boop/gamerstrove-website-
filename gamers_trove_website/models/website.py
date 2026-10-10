from urllib.parse import urlencode
from odoo import fields, models
from odoo.fields import Domain


class Website(models.Model):
    _inherit = 'website'

    gt_brand_enabled = fields.Boolean('Gamer’s Trove branding')
    gt_demo_notice = fields.Boolean('Show client demo notice')
    gt_phone = fields.Char('Store phone', default='+1 868 376-5722')
    gt_whatsapp = fields.Char('WhatsApp number', default='18683765722')
    gt_email = fields.Char('Store email', default='gamers.trove.tt@gmail.com')
    gt_address = fields.Text('Store address', default='105 Cathay House, Carlton Centre\n61 St James Street, San Fernando\nTrinidad & Tobago')
    gt_hours = fields.Text('Opening hours')
    gt_instagram = fields.Char('Instagram URL', default='https://www.instagram.com/gamerstrovett/')
    gt_facebook = fields.Char('Facebook URL', default='https://www.facebook.com/GamersTroveTT/')
    gt_announcement = fields.Char('Announcement', translate=True, default='YOUR LOCAL GAME STORE. YOUR NEXT GREAT ADVENTURE.')

    def _gt_whatsapp_url(self):
        self.ensure_one()
        digits = ''.join(c for c in (self.gt_whatsapp or '') if c.isascii() and c.isdigit())
        return 'https://wa.me/' + digits if 7 <= len(digits) <= 15 else False

    def _gt_maps_url(self):
        self.ensure_one()
        return 'https://www.google.com/maps/search/?' + urlencode({'api': '1', 'query': self.gt_address}) if self.gt_address else False

    def _gt_products(self):
        self.ensure_one()
        Product = self.env['product.template'].with_context(website_id=self.id)
        if not self.gt_brand_enabled or not self.has_ecommerce_access():
            return Product.browse()
        return Product.search(Domain.AND([self.sale_product_domain(), [
            ('active', '=', True), ('is_published', '=', True), ('gt_featured', '=', True),
        ]]), order='website_sequence, id', limit=8)

    def _gt_categories(self):
        self.ensure_one()
        Category = self.env['product.public.category'].with_context(website_id=self.id)
        if not self.gt_brand_enabled or not self.has_ecommerce_access():
            return Category.browse()
        return Category.search(Domain.AND([self.website_domain(), [
            ('gt_featured', '=', True), ('has_published_products', '=', True),
        ]]), order='sequence, name, id', limit=8)

    def _gt_events(self):
        self.ensure_one()
        Event = self.env['event.event'].with_context(website_id=self.id)
        if not self.gt_brand_enabled:
            return Event.browse()
        # Never surface private, unpublished, archived or other-company events in a public block.
        return Event.search(Domain.AND([self.website_domain(), [
            ('active', '=', True), ('is_published', '=', True),
            ('website_visibility', '=', 'public'), ('gt_featured', '=', True),
            ('company_id', '=', self.company_id.id),
            ('date_end', '>=', fields.Datetime.now()),
        ]]), order='date_begin, id', limit=3)
