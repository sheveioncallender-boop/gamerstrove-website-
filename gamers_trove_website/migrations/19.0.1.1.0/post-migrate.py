"""Replace only the original hero image; retain all other website-editor changes."""
from lxml import etree
from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    page = env.ref('gamers_trove_website.page_home', raise_if_not_found=False)
    if not page:
        return
    view = page.view_id.with_context(lang=None)
    tree = etree.fromstring(view.arch_db.encode())
    changed = False
    for img in tree.xpath("//div[contains(concat(' ',normalize-space(@class),' '),' gt-hero-photo ')]/img"):
        if img.get('src') == '/gamers_trove_website/static/src/img/trade.jpg':
            img.set('src', '/gamers_trove_website/static/src/img/hero-players.jpg')
            img.set('alt', 'Friends enjoying a tabletop game together')
            img.set('width', '1800')
            img.set('height', '1202')
            changed = True
    if changed:
        for tag in tree.xpath("//div[contains(concat(' ',normalize-space(@class),' '),' gt-photo-tag ')]"):
            span = tag.find('span')
            strong = tag.find('strong')
            if span is not None and span.text == 'THE TROVE TITANS':
                span.text = 'MAKE TIME TO PLAY'
            if strong is not None and strong.text == 'REAL PLAYERS.':
                strong.text = 'GOOD GAMES.'
                br = strong.find('br')
                if br is not None and br.tail == 'REAL COMMUNITY.':
                    br.tail = 'GREAT COMPANY.'
        view.write({'arch_db': etree.tostring(tree, encoding='unicode')})
