from odoo import SUPERUSER_ID, api
from odoo.addons.gamers_trove_demo.catalog import repair_catalog


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    website = env.ref('website.default_website')
    # Keep a retired demonstration retired. The explicit settings action can republish it.
    repair_catalog(env, website, publish=website.gt_demo_notice)
