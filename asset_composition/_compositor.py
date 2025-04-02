# ----------------------------------------------------------------------------
# Copyright (c) Studio Gobo Ltd 2025
# Licensed under the MIT license.
# See LICENSE.TXT in the project root for license information.
# ----------------------------------------------------------------------------
# File			-> _compositor.py
# Created		-> March 2025
# Author		-> Michael Malinowski (Studio Gobo)
# ----------------------------------------------------------------------------
import functools

from . import _asset, _config


class Compositor:
    """
    The compositor is a class which contains the accessors
    to all the factories.
    """

    def __init__(self, configuration: _config.Configuration | None = None):
        self.configuration: _config.Configuration = (
            configuration or _config.Configuration()
        )

    @functools.cache
    def get(
        self,
        identifier: str,
        lightweight: bool = False,
    ) -> "asset_composition.Asset":
        """
        Convenience function for getting an Asset class from an identifier.

        Args:
            identifier: Identifier of the asset
            lightweight: If lightweight, then only traits marked as being lightweight
                will be bound to the asset.
        Returns:
            Asset
        """
        return _asset.Asset(
            identifier=identifier,
            lightweight=lightweight,
            compositor=self,
        )

    # TODO: need to clarify the argument types
    def search(self, query, search_from=None) -> list:
        """This will run a search query using all available discovery plugins.

        Args:
            query (str): The string to search for. You may use wildcard characters
            search_from (_type_, optional): Location from which to perform the search. Defaults to None.

        Returns:
            list: List of found assets
        """
        if not query:
            return []

        # -- This is where we will collate the results from each search
        results = list()

        # -- Cycle all our discovery plugins
        for discovery_plugin in self.configuration.discovery.plugins():

            # -- Extend the results from the discovery plugin
            results.extend(
                discovery_plugin.search(
                    query,
                    search_from,
                ),
            )

        # -- Ensure the results are unique
        unique_results = list(set(results))

        # -- Convert the results to asset class instances
        return [_asset.Asset(p, compositor=self) for p in sorted(unique_results)]
