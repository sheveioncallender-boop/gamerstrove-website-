"""Remove decorative numbering while retaining existing editor content."""
from lxml import etree
from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for name in ('home', 'about', 'community', 'visit', 'beginner'):
        page = env.ref('gamers_trove_website.page_' + name, raise_if_not_found=False)
        if not page:
            continue
        view = page.view_id.with_context(lang=None)
        tree = etree.fromstring(view.arch_db.encode())
        nodes = tree.xpath("//*[contains(concat(' ',normalize-space(@class),' '),' gt-hero-caption ')]/span[1] | //*[contains(concat(' ',normalize-space(@class),' '),' gt-editorial-grid ')]/div/span[1]")
        changed = False
        for node in nodes:
            if ''.join(node.itertext()).strip() not in ('01 /', '01', '02', '03'):
                continue
            # Preserve the text following the number (e.g. SHOP. PLAY. CONNECT.).
            parent = node.getparent()
            previous = node.getprevious()
            if previous is None:
                parent.text = (parent.text or '') + (node.tail or '')
            else:
                previous.tail = (previous.tail or '') + (node.tail or '')
            parent.remove(node)
            changed = True
        if changed:
            view.write({'arch_db': etree.tostring(tree, encoding='unicode')})
