# ----------------------------------------------------------------------------
# Copyright (c) Studio Gobo Ltd 2025
# Licensed under the MIT license.  
# See LICENSE.TXT in the project root for license information.
# ----------------------------------------------------------------------------
# File			-> test_asset.py
# Created		-> March 2025
# Author		-> Michael Malinowski (Studio Gobo)
# ----------------------------------------------------------------------------
import os
import unittest
import functools
import asset_composition


# --------------------------------------------------------------------------------------
class AssetUnitTest(unittest.TestCase):

    def _get_test_compositor(self):

        configuration = asset_composition.Configuration()
        configuration.traits.add_path(
            os.path.join(
                os.path.dirname(__file__),
                "traits",
            ),
        )
        configuration.traits.add_path(
            os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "plugins",
                "traits",
            ),
        )
        configuration.discovery.add_path(
            os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "plugins",
                "discovery",
            ),
        )
        compositor = asset_composition.Compositor(configuration=configuration)
        return compositor

    def test_can_create_configuration(self):
        configuration = asset_composition.Configuration()

    def test_can_instance_compositor(self):
        compositor = asset_composition.Compositor()

    def test_can_instance_compositor_with_configuration(self):
        compositor = self._get_test_compositor()

    def test_can_bind_traits(self):

        compositor = self._get_test_compositor()
        asset = compositor.get(__file__)

        self.assertIn(
            "BindOnlyToPyFiles",
            asset.trait_names(),
        )

        self.assertNotIn(
            "NeverBindToPyFiles",
            asset.trait_names(),
        )

    def test_importance(self):

        compositor = self._get_test_compositor()
        asset = compositor.get(__file__)

        self.assertIn(
            "LowImportanceTrait",
            asset.trait_names(),
        )

        self.assertIn(
            "HighImportanceTrait",
            asset.trait_names(),
        )

        self.assertEqual(
            asset.label(),
            "high_importance"
        )

    def test_rebinding(self):

        compositor = self._get_test_compositor()
        asset = compositor.get(__file__)

        initial_trait_count = len(asset.traits())
        asset.fully_load()

        self.assertEqual(
            initial_trait_count,
            len(asset.traits()),
        )

    def test_access_lightweight(self):

        compositor = self._get_test_compositor()
        asset = compositor.get(__file__, lightweight=True)

        self.assertTrue(
            asset.is_lightweight(),
        )

        asset.fully_load()

        self.assertFalse(
            asset.is_lightweight(),
        )

    def test_access_label(self):

        compositor = self._get_test_compositor()
        asset = compositor.get(__file__, lightweight=True)

        self.assertTrue(
            str(asset.label()).endswith("test_asset.py")
        )

    def test_access_info(self):

        compositor = self._get_test_compositor()
        asset = compositor.get(__file__)

        self.assertEqual(
            asset.info(),
            "Basic Info",
        )

    def test_access_status_icons(self):

        compositor = self._get_test_compositor()
        asset = compositor.get(__file__)

        self.assertIn(
            "Status Icon",
            asset.status_icons(),
        )

    def test_access_is_valid(self):

        compositor = self._get_test_compositor()
        asset = compositor.get(__file__)

        self.assertTrue(
            asset.is_valid(),
        )
        asset = compositor.get("invalid test")

        self.assertFalse(
            asset.is_valid(),
        )

    def test_access_custom_data(self):

        compositor = self._get_test_compositor()
        asset = compositor.get(__file__)

        self.assertIn(
            "Basic Data",
            asset.custom_data(),
        )

        self.assertEqual(
            asset.custom_data()["Basic Data"],
            True,
        )

    def test_actions(self):
        compositor = self._get_test_compositor()
        asset = compositor.get(__file__)

        action_names = [
            action.name()
            for action in asset.actions()
        ]

        self.assertIn(
            "Action 1",
            action_names,
        )

        action = asset.action("Action 1")
        self.assertIsNotNone(
            action,
        )

        self.assertEqual(
            action.call(),
            1
        )

        self.assertIn(
            "[Action:Simple Actions:Action 1]",
            str(action)
        )

    def test_change_signals(self):

        compositor = self._get_test_compositor()
        asset = compositor.get(__file__)
        data = dict(result=False)

        func = functools.partial(
            self._set_result_true,
            data,
        )
        asset.changed.connect(
            func,
        )
        asset.pull()
        self.assertTrue(
            data["result"],
        )

    def _set_result_true(self, data):
        data["result"] = True