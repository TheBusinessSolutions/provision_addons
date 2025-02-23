# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright 2024 Michael Tietz (MT Software) <mtietz@mt-software.de>
from odoo import exceptions

from .common import TestMtoMtsRouteCommon


class TestMtoMtsRoute(TestMtoMtsRouteCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.warehouse = cls.env.ref("stock.warehouse0")
        cls.setUpRules()

    def test_standard_mto_route(self):
        mto_route = self.env.ref("stock.route_warehouse0_mto")
        mto_route.active = True
        self.product.route_ids = [(6, 0, [mto_route.id])]
        moves = self._run_procurement(2.0)
        self.assertEqual(len(moves), 2)

    def test_standard_mts_route(self):
        moves = self._run_procurement(2.0)
        self.assertEqual(len(moves), 1)

    def test_mts_mto_route_split(self):
        mto_mts_route = self.env.ref("stock_mts_mto_rule.route_mto_mts")
        self.product.route_ids = [(6, 0, [mto_mts_route.id])]
        self._create_quant(1.0)
        moves = self._run_procurement(2.0)
        self.assertEqual(3, len(moves))
        move_mts = self.env["stock.move"].search(
            [
                ("group_id", "=", self.group.id),
                ("location_dest_id", "=", self.customer_loc.id),
                ("procure_method", "=", "make_to_stock"),
            ]
        )
        self.assertEqual(1, len(move_mts))
        self.assertEqual(1.0, move_mts.product_uom_qty)
        self.assertEqual("assigned", move_mts.state)
        move_mto = self.env["stock.move"].search(
            [
                ("group_id", "=", self.group.id),
                ("location_dest_id", "=", self.customer_loc.id),
                ("procure_method", "=", "make_to_order"),
            ]
        )
        self.assertEqual(1, len(move_mto))
        self.assertEqual("waiting", move_mto.state)

    def test_mts_mto_route_no_split(self):
        """Check the no split rule."""
        mto_mts_route = self.env.ref("stock_mts_mto_rule.route_mto_mts")
        mto_mts_route.rule_ids.mts_quantity_rule = "full"
        self.product.route_ids = [(6, 0, [mto_mts_route.id])]
        self._create_quant(1.0)
        moves = self._run_procurement(2.0).filtered(
            lambda m: m.location_dest_id == self.customer_loc
        )
        self.assertEqual(1, len(moves))
        self.assertEqual(2.0, moves[0].product_uom_qty)
        self.assertEqual("make_to_order", moves[0].procure_method)

    def test_mts_mto_route_mto_only(self):
        mto_mts_route = self.env.ref("stock_mts_mto_rule.route_mto_mts")
        self.product.route_ids = [(6, 0, [mto_mts_route.id])]
        moves = self._run_procurement(2.0).filtered(
            lambda m: m.location_dest_id == self.customer_loc
        )
        self.assertEqual(1, len(moves))
        self.assertEqual(2.0, moves.product_uom_qty)
        self.assertEqual("make_to_order", moves.procure_method)

    def test_mts_mto_route_mts_only(self):
        mto_mts_route = self.env.ref("stock_mts_mto_rule.route_mto_mts")
        self.product.route_ids = [(6, 0, [mto_mts_route.id])]
        self._create_quant(3.0)
        moves = self._run_procurement(2.0)
        self.assertEqual(1, len(moves))
        self.assertEqual(2.0, moves.product_uom_qty)
        self.assertEqual("make_to_stock", moves.procure_method)

    def test_mts_mto_rule_contrains(self):
        rule = self.env["stock.rule"].search(
            [("action", "=", "split_procurement")], limit=1
        )
        with self.assertRaises(exceptions.ValidationError):
            rule.write({"mts_rule_id": False})

    def test_mts_mto_route_mto_removed(self):
        self.env.ref("stock_mts_mto_rule.route_mto_mts").unlink()
        with self.assertRaises(exceptions.UserError):
            # mts_mto_rule_id is checked as a global rule
            self.warehouse.mts_mto_rule_id = False

    def test_mts_mto_route_mts_removed(self):
        self.warehouse.mto_mts_management = True
        rules = self.env["stock.rule"].search(
            [
                ("location_src_id", "=", self.warehouse.lot_stock_id.id),
                ("route_id", "=", self.warehouse.delivery_route_id.id),
            ]
        )
        self.env.cr.execute(
            "UPDATE stock_move SET rule_id = NULL WHERE rule_id IN %s",
            (tuple(rules.ids),),
        )
        self.warehouse.mts_mto_rule_id = False
        self.warehouse.mto_mts_management = True
        self.assertTrue(self.warehouse.mts_mto_rule_id)

    def test_mts_mto_route_mto_no_mts_rule(self):
        self.warehouse.mts_mto_rule_id = False
        self.warehouse.mto_pull_id = False
        self.warehouse.mto_mts_management = True
        self.assertTrue(self.warehouse.mts_mto_rule_id)

    def test_create_routes(self):
        self.warehouse._create_or_update_route()
        mts_mto_route = self.warehouse.mts_mto_rule_id
        self.assertEqual(mts_mto_route.warehouse_id, self.warehouse)
        self.assertEqual(
            mts_mto_route.location_id, self.warehouse.mto_pull_id.location_id
        )
        self.assertEqual(
            mts_mto_route.picking_type_id, self.warehouse.mto_pull_id.picking_type_id
        )
        self.assertEqual(
            mts_mto_route.route_id, self.env.ref("stock_mts_mto_rule.route_mto_mts")
        )

    def test_remove_mts_mto_management(self):
        warehouse_rule = self.warehouse.mts_mto_rule_id
        self.assertTrue(self.warehouse.mts_mto_rule_id)
        self.warehouse.mto_mts_management = False
        self.assertFalse(warehouse_rule.active)

    def test_get_all_routes_for_wh(self):
        routes = self.warehouse._get_all_routes()
        self.assertTrue(self.warehouse.mts_mto_rule_id)
        self.assertTrue(self.warehouse.mts_mto_rule_id.route_id in routes)

    def test_rename_warehouse(self):
        rule_name = self.warehouse.mts_mto_rule_id.name
        new_warehouse_name = "NewName"
        new_rule_name = rule_name.replace(self.warehouse.name, new_warehouse_name, 1)
        self.warehouse.name = new_warehouse_name
        self.assertEqual(new_rule_name, self.warehouse.mts_mto_rule_id.name)
