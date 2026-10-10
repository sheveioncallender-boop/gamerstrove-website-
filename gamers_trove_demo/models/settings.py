from odoo import models
from odoo.exceptions import AccessError
from ..catalog import repair_catalog


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def action_gt_publish_catalog(self):
        self.ensure_one()
        if not self.env.user.has_group('base.group_system'):
            raise AccessError(self.env._('Only administrators can publish the client catalogue.'))
        count = repair_catalog(self.env, self.website_id, publish=True)
        if count:
            self.website_id.gt_demo_notice = True
        return {'type': 'ir.actions.client', 'tag': 'display_notification', 'params': {
            'title': self.env._('Client catalogue'),
            'message': self.env._('%s existing product(s) published with their product photos.', count),
            'type': 'success' if count else 'warning', 'sticky': False,
        }}
