# Staging acceptance checks

1. Install the website addon on Odoo 19, then the optional demo addon. Confirm no installation traceback and the default homepage resolves at `/`.
2. Open all five custom pages on desktop and mobile. Confirm native Odoo menus, search, cart and account controls work.
3. Edit the hero text/image and a company page through Website Edit, save, upgrade the addon, and confirm edits remain.
4. Change a product name, price, variant, publication flag and homepage-feature flag. Verify the homepage and native shop respond without code changes.
5. Confirm featured products respect website/company boundaries, pricelist, tax display, restricted eCommerce access and unpublished records.
6. Open a demo product, choose a variant, add to cart, change quantity and remove it. Configure real inventory and verify out-of-stock behavior on a real test product.
7. Change a tournament date, capacity, fee, format, image and publication state. Confirm homepage display and native event page agree.
8. Register two attendees for a paid ticket. Verify both attendee records remain linked to the correct order lines, quantities and event.
9. With a configured test payment provider: complete payment, confirm order/registration handling, ticket email and check-in. Also exercise failed/cancelled payments and a duplicate callback using the provider’s supported testing tools.
10. Test capacity at the final seat and concurrent booking attempts. Verify full/closed events cannot be booked through native event routes.
11. Confirm logged-user-only, link-only, other-company and other-website events are excluded from the homepage.
12. Unpublish sample products/events with the settings button. Confirm real records and historical transactions remain.
13. Verify company TTD currency, website pricelist, VAT treatment, delivery methods, payment-provider configuration, outgoing mail and customer-facing event/refund terms before going live.
