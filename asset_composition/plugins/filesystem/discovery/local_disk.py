# ----------------------------------------------------------------------------
# Copyright (c) Studio Gobo Ltd 2025
# Licensed under the MIT license.
# See LICENSE.TXT in the project root for license information.
# ----------------------------------------------------------------------------
# File			-> local_disk.py
# Created		-> March 2025
# Author		-> Michael Malinowski (Studio Gobo)
# ----------------------------------------------------------------------------
import glob

import asset_composition


class LocalDiskDiscovery(asset_composition.DiscoveryPlugin):
    """
    Discovery traits allow us to expose a mechanism of searching. In this case we
    expose a mechanism to search for local files/folders within a users machine.
    """

    # TODO: Need some guidance on what types are the arguments
    @classmethod
    def search(cls, query, search_from) -> list:

        if not query.startswith("*"):
            query = "*" + query

        if not query.endswith("*"):
            query += "*"

        if not isinstance(search_from, list):
            search_from: list = [search_from]

        results: list = []

        for search_root in search_from:
            results.extend(
                glob.glob("" + search_root + "/**/" + query, recursive=True),
            )

        return [result.replace("\\", "/") for result in results]
