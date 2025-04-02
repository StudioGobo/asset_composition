# ----------------------------------------------------------------------------
# Copyright (c) Studio Gobo Ltd 2025
# Licensed under the MIT license.  
# See LICENSE.TXT in the project root for license information.
# ----------------------------------------------------------------------------
# File			-> test_config.py
# Created		-> March 2025
# Author		-> Michael Malinowski (Studio Gobo)
# ----------------------------------------------------------------------------
import os
import unittest
import tempfile
from os import close

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

    def test_can_serialise_configuration(self):
        compositor = self._get_test_compositor()

        data = compositor.configuration.serialise()

        self.assertEqual(
            len(data["trait_paths"]),
            2,
        )

        self.assertEqual(
            len(data["discovery_paths"]),
            1,
        )

    def test_can_save_configuration(self):
        compositor = self._get_test_compositor()

        save_file = tempfile.NamedTemporaryFile(delete=False)
        filepath = save_file.name
        save_file.close()

        compositor.configuration.serialise(filepath=filepath)

        self.assertTrue(
            os.path.exists(filepath),
        )

    def test_can_load_configuration(self):
        compositor = self._get_test_compositor()

        save_file = tempfile.NamedTemporaryFile(delete=False)
        filepath = save_file.name
        save_file.close()

        compositor.configuration.serialise(filepath=filepath)

        new_config = asset_composition.Configuration(filepath=filepath)

        self.assertEqual(
            len(new_config.traits.paths()),
            2,
        )

        self.assertEqual(
            len(new_config.discovery.paths()),
            1,
        )