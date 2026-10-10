"""Structural checks. Does not substitute for installation on an Odoo database."""
import ast
import sys
from pathlib import Path
from lxml import etree

root = Path(__file__).resolve().parents[1]
upstream = Path(sys.argv[1]) if len(sys.argv) > 1 else None
modules = ('gamers_trove_website', 'gamers_trove_demo')
local_ids = {}
for module in modules:
    folder = root / module
    manifest = ast.literal_eval((folder / '__manifest__.py').read_text())
    assert manifest['version'].startswith('19.0.')
    for path in folder.rglob('*.py'): ast.parse(path.read_text(), filename=str(path))
    for path in manifest.get('data', []): assert (folder / path).is_file(), path
    for paths in manifest.get('assets', {}).values():
        for asset in paths: assert (root / asset).is_file(), asset
    for path in folder.rglob('*.xml'):
        tree = etree.parse(str(path))
        for node in tree.xpath('//*[@id]'):
            if node.tag in ('record','template','menuitem'):
                xmlid = node.get('id'); full = xmlid if '.' in xmlid else module + '.' + xmlid
                assert full not in local_ids, full
                local_ids[full] = node
        for node in tree.xpath('//*[@t-value or @t-if or @t-foreach or @t-out or @t-options]'):
            for key in ('t-value','t-if','t-foreach','t-out','t-options'):
                if node.get(key): compile(node.get(key), str(path), 'eval')
        for node in tree.xpath('//*[@src]'):
            src = node.get('src')
            if src.startswith('/gamers_trove_'): assert (root / src.lstrip('/')).is_file(), src
        for node in tree.xpath('//record[@model="website.page"]'):
            assert node.getparent().get('noupdate') == '1', 'Page edits would reset during upgrade'
            assert node.xpath('.//*[@t-call="website.layout"]'), 'Native Odoo layout missing'
            assert node.xpath('.//*[@id="wrap" and contains(@class,"oe_structure")]'), 'Editor structure missing'
print('PASS: manifests, Python syntax, XML, QWeb expressions, assets and page-edit preservation')
if upstream:
    upstream_ids = {}
    for base in (upstream/'addons', upstream/'odoo/addons'):
        for path in base.glob('*/**/*.xml'):
            module = path.relative_to(base).parts[0]
            try:tree = etree.parse(str(path))
            except etree.XMLSyntaxError:continue
            for node in tree.xpath('//*[@id]'):
                if node.tag in ('record','template','menuitem'):
                    xid = node.get('id');full=xid if '.' in xid else module+'.'+xid
                    upstream_ids[full] = node
    all_ids = {**upstream_ids, **local_ids}
    checks = 0
    for module in modules:
        for path in (root/module).rglob('*.xml'):
            tree = etree.parse(str(path))
            for node in tree.xpath('//*[@ref or @inherit_id or @t-call]'):
                for attr in ('ref','inherit_id','t-call'):
                    xid=node.get(attr)
                    if not xid:continue
                    xid=xid if '.' in xid else module+'.'+xid
                    assert xid in all_ids, (path, 'Missing external ID', xid)
                    checks+=1
            for record in tree.xpath('//record[field[@name="inherit_id"]]'):
                parent=all_ids[record.find('field[@name="inherit_id"]').get('ref')]
                for xp in record.xpath('./field[@name="arch"]/xpath'):
                    assert parent.xpath(xp.get('expr')), ('Unmatched native XPath',xp.get('expr'))
    print('PASS:',checks,'external references and native backend-view XPaths against Odoo 19 source')
print('LIMIT: runtime install, rendered QWeb and payment/browser flows require staging Odoo.')
