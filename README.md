# Gamer’s Trove — Odoo 19 website, shop and tournament tickets

A redesigned storefront built for **Odoo 19 Community** (also compatible with Enterprise). Products, variants, prices, stock, carts, checkout, payments, orders, events, tickets and attendees remain native Odoo records and workflows. The module retains Odoo’s real header, search, account menu and cart.

## Install through Cloudpepper

1. Connect this repository and the `main` branch to the Odoo 19 instance. Both addon folders must be available at the repository root.
2. Update the Apps list. Install **Gamer’s Trove — Website & Tournaments** (`gamers_trove_website`). Dependencies install the Odoo shop, stock integration, Events and Online Event Ticketing.
3. For the client presentation, install **Gamer’s Trove — Client Demo** (`gamers_trove_demo`). Remove the Apps filter if needed to find the optional addon.
4. Open Website. The default website is configured with the new homepage, original logo and menu links.
5. Before adding transactional data, configure the company and website pricelist for **TTD**, confirm taxes, warehouse/delivery setup and payment providers. The addons do not change company currency, taxes, payment credentials or accounting settings.

Sample numeric prices are interpreted in the company’s configured currency. The static visual preview displays illustrative TTD prices. Demo products deliberately have no taxes and no fabricated stock counts; configure tax and inventory rules on real products before going live.

## Everything managed in Odoo

| Content / operation | Where to manage it |
| --- | --- |
| Hero, banner images, headings, company copy, galleries, FAQs | Website → Edit on the relevant page |
| Logo, menus and native header | Website editor / Website settings |
| Phone, email, WhatsApp, address, hours, social links, announcement | Website → Configuration → Settings → Gamer’s Trove |
| Product descriptions, photos, variants, prices, publication | Website / Sales → Products |
| Homepage product selection and labels | Product → Sales → Gamer’s Trove storefront |
| Homepage category selection, icons and order | Website eCommerce Categories → Show in Trove categories / Sequence |
| Stock, transfers, warehouses and availability | Inventory / native product settings |
| Orders, carts, payment methods, taxes and delivery | Native Sales, Website, Accounting and Inventory settings |
| Tournament details, schedule, ticket price, capacity, attendee questions | Events → select the event |
| Homepage tournament selection and photo | Event → Trove storefront |
| Attendees, registration status and check-in | Native Events Attendees / Registration Desk |
| Confirmation and reminder emails | Event → Communication; configure outgoing email first |

Only published, public, current/future events for the selected website/company appear on the homepage. Past, unpublished and restricted-visibility events are excluded. Product cards respect publication, website access, current visitor pricelist and fiscal position; they lead to native product pages so variants and stock rules are enforced.

## Paid tournament entry

`website_event_sale` supplies the complete native path:

Event page → choose available ticket(s) → attendee information → Odoo cart/checkout → configured payment provider → order/registration handling → native event ticket and check-in.

The ticket product uses Odoo 19 `service_tracking = 'event'`. There are no custom payment callbacks, bypass checkout routes, fake success states or duplicated attendee databases. Registration capacity is enforced by Odoo. Staff retain normal administrative authority to confirm/cancel sales and registrations. For reconciliation, review payment transactions/order status; an administrative sale confirmation is not evidence of a captured card payment.

An enabled payment provider is required for live online payments. No provider credentials were supplied or configured. Complete a staging transaction, confirmation email and ticket/check-in test before accepting real payments. Pairings, brackets, standings and game-specific tournament scoring are outside this version; it handles event listings, paid entry and attendance.

## Sample client data

The optional demo addon installs four sample products (including a three-option necklace variant), three future tournament examples and native ticket products. A small, configurable client-preview notice distinguishes illustrative stock/prices/dates from live offers. Demo products and events are tagged in the backend.

To finish the presentation, use **Website Settings → Gamer’s Trove → Unpublish demo products and tournaments**. This preserves orders, registrations and real products. Do not uninstall the demo addon after placing orders against its records; unpublish instead.

Sample data and editable pages are preserved on addon upgrades. The setup hook runs on initial install only. Existing company records, payment providers and stock balances are not overwritten. Initial installation targets `website.default_website`; for another website, configure page/menu ownership and branding intentionally.

## Repository layout

- `gamers_trove_website/`: production addon, Odoo models, editable website pages, live commerce/event blocks and original brand assets.
- `gamers_trove_demo/`: optional client-demo catalogue and events.
- `preview/`: static visual demonstration; checkout actions simulate locally and never charge money.
- `scripts/`: source validation and preview-generation helpers.
- `docs/`: asset credits, acceptance checklist and verification results.

## Verification

Run `python scripts/validate.py /path/to/odoo19` (requires lxml) for Python/XML/static checks and upstream external-ID/XPath compatibility. Native Odoo tests are included under `gamers_trove_website/tests/`; run them on a staging database:

```bash
odoo --addons-path=/path/to/odoo/addons,/path/to/repository -d trove_test -i gamers_trove_demo --test-enable --test-tags /gamers_trove_website --stop-after-init --without-demo=all
```

A live Odoo database and browser were not available during preparation. Installation, checkout, live provider callbacks and visual browser QA must be validated in staging. See `docs/ACCEPTANCE.md`.
