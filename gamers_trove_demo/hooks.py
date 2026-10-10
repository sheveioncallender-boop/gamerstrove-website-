"""Install once, retain native records and staff edits on subsequent upgrades."""
import base64
import json
from datetime import datetime, timedelta
from odoo import Command
from odoo.tools import file_open

MODULE = 'gamers_trove_demo'


def _image(module, name):
    with file_open(module + '/static/src/img/' + name, 'rb') as stream:
        return base64.b64encode(stream.read())


def _record(env, model, key, values):
    existing = env.ref(MODULE + '.' + key, raise_if_not_found=False)
    if existing:
        return existing
    record = env[model].create(values)
    env['ir.model.data'].create({'module': MODULE, 'name': key, 'model': model, 'res_id': record.id, 'noupdate': True})
    return record


def post_init_hook(env):
    website = env.ref('website.default_website')
    company = website.company_id
    env = env(context={**env.context, 'allowed_company_ids': [company.id]})
    website = website.with_env(env)
    products = [
        ('blue_eyes', 'Blue-Eyes White Destiny Structure Deck', 'yugioh', 160, 'blue-eyes.png', 'Deck ready', 'A Blue-Eyes themed Yu-Gi-Oh! structure deck. Sample product for the client presentation.'),
        ('foundations', 'Foundations Starter Collection', 'magic', 495, 'foundations.png', 'Build your deck', 'A Magic: The Gathering collection for exploring deck building. Sample product for the client presentation.'),
        ('beginner', 'Foundations Beginner Box', 'magic', 280, 'beginner.png', 'Start here', 'An introduction to Magic: The Gathering. Sample product for the client presentation.'),
        ('genshin', 'Genshin Impact Element Necklace', 'collectibles', 85, 'genshin.jpg', 'Fan favourites', 'A fan accessory inspired by Genshin Impact, as featured on the store’s social page. Sample selection and price.'),
    ]
    for i, (key, name, category, price, image, badge, description) in enumerate(products):
        category_id = env.ref('gamers_trove_website.category_' + category).id
        owner = 'gamers_trove_website' if image == 'genshin.jpg' else MODULE
        product = _record(env, 'product.template', 'product_' + key, {
            'name': name, 'default_code': 'GT-DEMO-%03d' % (i + 1),
            'type': 'consu', 'is_storable': False, 'sale_ok': True, 'purchase_ok': False,
            'list_price': price, 'taxes_id': [Command.clear()],
            'website_id': website.id, 'company_id': company.id,
            'is_published': True, 'gt_featured': True, 'gt_demo': True, 'gt_badge': badge,
            'website_sequence': (i + 1) * 10,
            'public_categ_ids': [Command.set([category_id])],
            'image_1920': _image(owner, image), 'description_sale': description,
            'website_description': '<p>' + description + '</p>',
        })
        if key == 'genshin' and not product.attribute_line_ids:
            attribute = _record(env, 'product.attribute', 'element_attribute', {'name': 'Element', 'create_variant': 'always', 'display_type': 'radio'})
            values = [_record(env, 'product.attribute.value', 'element_' + n.lower(), {'name': n, 'attribute_id': attribute.id}) for n in ('Anemo', 'Geo', 'Pyro')]
            _record(env, 'product.template.attribute.line', 'necklace_elements', {'product_tmpl_id': product.id, 'attribute_id': attribute.id, 'value_ids': [Command.set([v.id for v in values])]})

    venue = _record(env, 'res.partner', 'venue', {
        'name': 'Gamer’s Trove', 'street': '105 Cathay House, Carlton Centre',
        'street2': '61 St James Street', 'city': 'San Fernando',
        'country_id': env.ref('base.tt').id, 'phone': website.gt_phone, 'email': website.gt_email,
    })
    ticket_product = _record(env, 'product.product', 'ticket_product', {
        'name': 'Tournament Entry', 'type': 'service', 'service_tracking': 'event',
        'invoice_policy': 'order', 'sale_ok': True, 'purchase_ok': False,
        'list_price': 100, 'company_id': company.id, 'website_id': website.id,
        'is_published': False, 'gt_demo': True, 'taxes_id': [Command.clear()],
    })
    # Two weeks ahead, on a Saturday at 1 pm Trinidad time (17:00 UTC).
    now = datetime.utcnow()
    start = (now + timedelta(days=14 + (5 - now.weekday()) % 7)).replace(hour=17, minute=0, second=0, microsecond=0)
    specs = [('yugioh', 'Yu-Gi-Oh! Saturday Showdown', 'Yu-Gi-Oh! · Advanced Constructed', 100, 32, 'weekends.jpg'),
             ('magic', 'Magic: The Gathering Game Day', 'Magic: The Gathering · Casual play', 85, 24, 'recap.jpg'),
             ('riftbound', 'Riftbound Community Tournament', 'Riftbound · Constructed', 60, 16, 'trade.jpg')]
    for i, (key, name, game, fee, capacity, image) in enumerate(specs):
        begin = start + timedelta(days=i * 7)
        event = _record(env, 'event.event', 'event_' + key, {
            'name': name, 'subtitle': 'Find your next match at the Trove.',
            'date_begin': begin, 'date_end': begin + timedelta(hours=4),
            'date_tz': 'America/Port_of_Spain', 'company_id': company.id,
            'website_id': website.id, 'address_id': venue.id,
            'website_visibility': 'public', 'is_published': True,
            'seats_limited': True, 'seats_max': capacity,
            'gt_featured': True, 'gt_demo': True, 'gt_game': game,
            'gt_card_image': _image('gamers_trove_website', image),
            'cover_properties': json.dumps({'background-image': "url('/gamers_trove_website/static/src/img/%s')" % image, 'opacity': '0.65', 'resize_class': 'cover_auto'}),
            'description': '<div class="container py-4"><p><strong>Client demonstration event.</strong> This is an example tournament, not an announced live fixture.</p><h2>Bring your game.</h2><p>Choose a ticket below, complete the attendee details and continue through the store checkout.</p><h3>Before entering</h3><p>For a live tournament, the organiser will confirm the format, deck rules, check-in time, equipment, eligibility and cancellation terms here.</p></div>',
        })
        _record(env, 'event.event.ticket', 'entry_' + key, {'name': 'Player entry', 'event_id': event.id, 'product_id': ticket_product.id, 'price': fee, 'seats_max': capacity})
    website.gt_demo_notice = True
