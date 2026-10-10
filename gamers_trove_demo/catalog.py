"""Repair known demo records only. Never replace a staff-supplied product image."""
from odoo.tools import file_open
import base64

PRODUCT_IMAGES = {
    'blue_eyes': ('gamers_trove_demo', 'blue-eyes.png'),
    'foundations': ('gamers_trove_demo', 'foundations.png'),
    'beginner': ('gamers_trove_demo', 'beginner.png'),
    'genshin': ('gamers_trove_website', 'genshin.jpg'),
}


def repair_catalog(env, website, publish=False):
    count = 0
    for key, (module, filename) in PRODUCT_IMAGES.items():
        product = env.ref('gamers_trove_demo.product_' + key, raise_if_not_found=False)
        if not product or not product.gt_demo or product.website_id != website:
            continue
        values = {}
        if not product.image_1920:
            with file_open(module + '/static/src/img/' + filename, 'rb') as image:
                values['image_1920'] = base64.b64encode(image.read())
        if publish:
            values.update(active=True, sale_ok=True, is_published=True, gt_featured=True)
            product.public_categ_ids.write({'gt_featured': True})
        if values:
            product.write(values)
        count += 1
    return count
