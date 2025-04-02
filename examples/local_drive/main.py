# ----------------------------------------------------------------------------
# Copyright (c) Studio Gobo Ltd 2025
# Licensed under the MIT license.
# See LICENSE.TXT in the project root for license information.
# ----------------------------------------------------------------------------
# File			-> main.py
# Created		-> March 2025
# Author		-> Michael Malinowski (Studio Gobo)
# ----------------------------------------------------------------------------
import os

import asset_composition

if __name__ == "__main__":

    configuration = asset_composition.Configuration()

    # -- Add our local drive traits
    configuration.traits.add_path(
        os.path.join(
            os.path.dirname(__file__),
            "traits",
        ),
    )

    # -- Add the built in traits
    configuration.traits.add_path(
        os.path.join(
            os.path.dirname(asset_composition.__file__),
            "plugins",
            "filesystem",
            "traits",
        ),
    )

    # -- Instance a compositor object. This object is what we use
    # -- to instance assets and perform searches
    compositor = asset_composition.Compositor(configuration)

    # -- Start by setting up our environment, specifically
    # -- We'll start by creating a
    asset_composition_folder: str = os.path.dirname(asset_composition.__file__)

    # -- Get the folder as an asset
    asset: asset_composition.Asset = compositor.get(asset_composition_folder)

    # -- Lets log some information
    print("Asset Label : %s" % asset.label())
    print("Asset Icon : %s" % asset.icon())

    # -- Lets have a look at the parent. Note that the asset
    # -- class itself is not hard coding how the parent is resolved
    # -- but the trait is doing so. This allows complete flexibility
    # -- for the asset. For instance, an asset in this instance is a file
    # -- or folder, but it could be a rest api url, or a repository path.
    print("Asset Parent : %s" % asset.parent())

    # -- In the same way, lets cycle its children
    for child in asset.children():

        # -- Get the child identifier and convert it to a child asset
        child_asset: asset_composition.Asset = compositor.get(child)

        # -- Print the relationship
        print("%s is a child of %s" % (child_asset.label(), asset.label()))

        # -- We can start to interact with this too.
        if child_asset.has_action("Get Imports"):
            for imported_module in child_asset.action("Get Imports").call():
                print("%s uses %s" % (child_asset.label(), imported_module))

    # -- Equally we can search the drive too. This will return a list
    # -- of assets, so we give it our trait factory so they can be bound
    # -- with our custom traits
    results: list = compositor.search(
        query="*.py",
        search_from=asset_composition_folder,
    )

    for result in results:
        print("Found Via Search : %s" % result.label())
