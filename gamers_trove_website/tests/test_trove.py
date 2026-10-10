from datetime import timedelta
from odoo import fields
from odoo.tests import HttpCase, tagged


@tagged('post_install', '-at_install')
class TestTrove(HttpCase):
    def setUp(self):
        super().setUp()
        self.website = self.env.ref('website.default_website')
        self.website.gt_brand_enabled = True

    def test_published_product_and_website_boundary(self):
        self.env['product.template'].search([('gt_featured', '=', True)]).gt_featured = False
        other = self.env['website'].create({'name': 'Other store', 'company_id': self.website.company_id.id})
        common = {'name': 'Boundary product', 'gt_featured': True, 'sale_ok': True,
                  'is_published': True, 'website_id': self.website.id, 'type': 'consu'}
        visible = self.env['product.template'].create(common)
        hidden = self.env['product.template'].create({**common, 'is_published': False})
        elsewhere = self.env['product.template'].create({**common, 'website_id': other.id})
        public_site = self.website.with_user(self.website.user_id)
        result = public_site._gt_products()
        self.assertIn(visible.id, result.ids)
        self.assertNotIn(hidden.id, result.ids)
        self.assertNotIn(elsewhere.id, result.ids)
        self.website.ecommerce_access = 'logged_in'
        self.assertFalse(public_site._gt_products())
        self.assertFalse(public_site._gt_categories())

    def test_event_publication_visibility_and_expiry(self):
        self.env['event.event'].search([('gt_featured', '=', True)]).gt_featured = False
        begin = fields.Datetime.now() + timedelta(days=4)
        common = {'name': 'Visible event', 'date_begin': begin, 'date_end': begin + timedelta(hours=4),
                  'company_id': self.website.company_id.id, 'website_id': self.website.id,
                  'gt_featured': True, 'is_published': True, 'website_visibility': 'public'}
        visible = self.env['event.event'].create(common)
        excluded = [self.env['event.event'].create({**common, 'website_visibility': kind}) for kind in ('link', 'logged_users')]
        excluded.append(self.env['event.event'].create({**common, 'is_published': False}))
        excluded.append(self.env['event.event'].create({**common, 'date_begin': begin - timedelta(days=8), 'date_end': begin - timedelta(days=7)}))
        result = self.website.with_user(self.website.user_id)._gt_events()
        self.assertIn(visible.id, result.ids)
        self.assertFalse(set(result.ids) & {e.id for e in excluded})

    def test_retire_demo_preserves_real_records(self):
        base = {'type': 'consu', 'sale_ok': True, 'is_published': True, 'website_id': self.website.id}
        demo = self.env['product.template'].create({**base, 'name': 'Demo', 'gt_demo': True})
        real = self.env['product.template'].create({**base, 'name': 'Real'})
        settings = self.env['res.config.settings'].create({'website_id': self.website.id})
        settings.action_gt_unpublish_demo()
        self.assertFalse(demo.is_published)
        self.assertTrue(real.is_published)
        self.assertTrue(demo.exists())

    def test_pages_render_with_native_layout(self):
        for url in ('/', '/about-trove', '/trove-community', '/visit-trove', '/start-playing', '/shop', '/event'):
            response = self.url_open(url)
            self.assertEqual(response.status_code, 200, url)
            self.assertNotIn('Traceback (most recent call last)', response.text)
            self.assertIn('gt-site', response.text)
        response = self.url_open('/')
        self.assertIn('YOUR NEXT', response.text)
        self.assertIn('/shop', response.text)

    def test_optional_demo_native_ticket_configuration(self):
        event = self.env.ref('gamers_trove_demo.event_yugioh', raise_if_not_found=False)
        if not event:
            self.skipTest('Optional client demo not installed')
        self.assertTrue(event.seats_limited)
        self.assertEqual(event.seats_max, 32)
        self.assertTrue(event.event_ticket_ids)
        for ticket in event.event_ticket_ids:
            self.assertEqual(ticket.product_id.service_tracking, 'event')
            self.assertEqual(ticket.product_id.type, 'service')
            self.assertEqual(ticket.product_id.invoice_policy, 'order')
            self.assertGreater(ticket.price, 0)
