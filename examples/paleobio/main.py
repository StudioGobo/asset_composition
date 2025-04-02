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


if __name__ == '__main__':

    configuration = asset_composition.Configuration()

    # -- Add our local drive traits
    configuration.traits.add_path(
        os.path.join(
            os.path.dirname(__file__),
            "traits",
        ),
    )

    # -- Add our local drive traits
    configuration.discovery.add_path(
        os.path.join(
            os.path.dirname(__file__),
            "discovery",
        ),
    )

    # -- Instance a compositor object. This object is what we use
    # -- to instance assets and perform searches
    compositor = asset_composition.Compositor(configuration)

    # -- Get the folder as an asset
    asset = compositor.get("Dinosauria")

    # -- Lets log some information - including an icon which is
    # -- automatically resolved, downloaded and stored.
    print("Asset Label : %s" % asset.label())
    print("Asset Icon : %s" % asset.icon())

    # -- In the same way, lets cycle its children
    for child in asset.children():

        # -- Get the child identifier and convert it to a child asset
        child_asset = compositor.get(child)

        # -- Print the relationship
        print(child_asset.label())

        for data_key, data_value in child_asset.custom_data().items():
            print("    %s = %s" % (data_key.ljust(20, " "), data_value))

    # -- We can also search for assets rather than being explicit. Searches
    # -- are also managed through a plugin based approach - so this particular
    # -- search will query the paleobio rest api
    results = compositor.search(
        search_from="",
        query="veloci",
    )

    for result in results:
        print("Found Via Search : %s" % result.label())
        for data_key, data_value in result.custom_data().items():
            print("    %s = %s" % (data_key.ljust(20, " "), data_value))