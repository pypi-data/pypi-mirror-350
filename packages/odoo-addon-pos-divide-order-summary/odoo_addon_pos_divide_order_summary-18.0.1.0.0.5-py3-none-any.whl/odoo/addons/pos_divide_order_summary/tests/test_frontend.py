# Copyright 2025 Camptocamp (https://www.camptocamp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import odoo.tests

from odoo.addons.point_of_sale.tests.test_frontend import TestPointOfSaleHttpCommon


@odoo.tests.tagged("post_install", "-at_install")
class TestDivideOrderSummary(TestPointOfSaleHttpCommon):
    def test_divide_order_summary(self):
        self.main_pos_config.with_user(self.pos_user).open_ui()
        self.start_tour(
            "/pos/ui?config_id=%d" % self.main_pos_config.id,
            "DivideOrderSummary",
            login="pos_user",
        )
