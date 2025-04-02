# ----------------------------------------------------------------------------
# Copyright (c) Studio Gobo Ltd 2025
# Licensed under the MIT license.  
# See LICENSE.TXT in the project root for license information.
# ----------------------------------------------------------------------------
# File			-> test_discovery.py
# Created		-> March 2025
# Author		-> Michael Malinowski (Studio Gobo)
# ----------------------------------------------------------------------------
import os
import unittest
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
                "filesystem",
                "traits",
            ),
        )
        configuration.discovery.add_path(
            os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "plugins",
                "filesystem",
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

    def test_discovery_library_found_plugins(self):
        compositor = self._get_test_compositor()
        self.assertGreaterEqual(
            len(compositor.configuration.discovery.plugins()),
            1,
        )

    def test_can_find_assets(self):

        compositor = self._get_test_compositor()
        print(compositor.configuration.discovery.plugins())
        results = compositor.search(
            query="*.py",
            search_from=os.path.dirname(__file__),
        )

        self.assertGreater(len(results), 1)
