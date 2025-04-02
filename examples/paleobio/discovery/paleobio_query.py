# ----------------------------------------------------------------------------
# Copyright (c) Studio Gobo Ltd 2025
# Licensed under the MIT license.
# See LICENSE.TXT in the project root for license information.
# ----------------------------------------------------------------------------
# File			-> paleobio_query.py
# Created		-> March 2025
# Author		-> Michael Malinowski (Studio Gobo)
# ----------------------------------------------------------------------------
"""
This discovery mechanism will search the paleobio rest api for a dinosaur
and return the results
"""
import json
import urllib.request

import asset_composition


class PaleoBioSearch(asset_composition.DiscoveryPlugin):
    """
    Discovery traits allow us to expose a mechanism of searching. In this case we
    expose a mechanism to search for local files/folders within a users machine.
    """

    @classmethod
    def search(cls, query, search_from) -> list:
        url: str = (
            r"https://paleobiodb.org/data1.2/taxa/list.json?rowcount&show=class&match_name=%"
            + query
            + "%"
        )

        with urllib.request.urlopen(url) as response:
            data = json.load(response)["records"]

        results = [record["nam"] for record in data if "nam" in record]

        return sorted(results)
