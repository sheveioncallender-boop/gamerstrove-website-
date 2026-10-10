import base64
import json
from odoo.tools import file_open

MODULE = 'gamers_trove_website'
SNAPSHOT = MODULE + '.installation_snapshot'


def post_init_hook(env):
    website = env.ref('website.default_website')
    params = env['ir.config_parameter'].sudo()
    if params.get_param(SNAPSHOT):
        return
    with file_open(MODULE + '/static/src/img/brand.jpg', 'rb') as stream:
        logo = base64.b64encode(stream.read())
    snapshot = {'website_id': website.id, 'name': website.name,
                'homepage_url': website.homepage_url or False,
                'logo': website.logo.decode() if isinstance(website.logo, bytes) else website.logo or False}
    website.write({'name': 'Gamer’s Trove', 'logo': logo, 'homepage_url': '/trove-home', 'gt_brand_enabled': True})
    specs = [('shop', 'Shop', '/shop', 10), ('events', 'Tournaments', '/event', 20),
             ('community', 'Community', '/trove-community', 30),
             ('about', 'About us', '/about-trove', 40), ('visit', 'Visit us', '/visit-trove', 50)]
    for key, name, url, sequence in specs:
        existing = env['website.menu'].search([('website_id', '=', website.id), ('parent_id', '=', website.menu_id.id), ('url', '=', url)], limit=1)
        if existing:
            continue
        menu = env['website.menu'].create({'name': name, 'url': url, 'website_id': website.id,
                                          'parent_id': website.menu_id.id, 'sequence': sequence})
        env['ir.model.data'].create({'module': MODULE, 'name': 'menu_' + key, 'model': 'website.menu', 'res_id': menu.id, 'noupdate': True})
    params.set_param(SNAPSHOT, json.dumps(snapshot))


def uninstall_hook(env):
    params = env['ir.config_parameter'].sudo()
    raw = params.get_param(SNAPSHOT)
    if not raw:
        return
    old = json.loads(raw)
    website = env['website'].browse(old['website_id']).exists()
    if website:
        vals = {}
        if website.homepage_url == '/trove-home': vals['homepage_url'] = old['homepage_url']
        if website.name == 'Gamer’s Trove': vals['name'] = old['name']
        with file_open(MODULE + '/static/src/img/brand.jpg', 'rb') as stream:
            if website.logo == base64.b64encode(stream.read()): vals['logo'] = old['logo']
        website.write(vals)
    params.search([('key', '=', SNAPSHOT)]).unlink()
