# ----------------------------------------------------------------------------
# Copyright (c) Studio Gobo Ltd 2025
# Licensed under the MIT license.  
# See LICENSE.TXT in the project root for license information.
# ----------------------------------------------------------------------------
# File			-> paleo_trait.py
# Created		-> March 2025
# Author		-> Michael Malinowski (Studio Gobo)
# ----------------------------------------------------------------------------
import json
import tempfile
import urllib.request
import asset_composition


class PaleoBioRestApiResourceTrait(asset_composition.Trait):

    _TAXA_API = r"https://paleobiodb.org/data1.2/taxa"
    @classmethod
    def can_bind(cls, identifier: str) -> bool:
        return True

    def label(self):
        return self.asset().identifier()

    def children(self):
        url_name = self.label().replace(" ", "+")
        url = "".join(
            [
                self._TAXA_API,
                "/list.json?rowcount&show=class&rel=children&name=",
                url_name,
            ],
        )

        with urllib.request.urlopen(url) as response:
            data = json.load(response)["records"]

        children = [
            item["nam"]
            for item in data
            if "oid" in item and item["nam"] != self.label()
        ]
        return sorted(children)

    def icon(self):

        url_name = self.label().replace(" ", "+")
        url = "".join(
            [
                self._TAXA_API,
                "/list.json?rowcount&show=class&show=img&show=full&name=",
                url_name,
            ],
        )
        with urllib.request.urlopen(url) as response:
            data = json.load(response)["records"][0]

        if "img" not in data:
            print(data)
            return ""

        url = "".join(
            [
                self._TAXA_API,
                "/thumb.png?id=",
                data["img"],
            ]
        )

        response = urllib.request.urlopen(url)
        image = response.read()

        tmp_image = tempfile.NamedTemporaryFile(suffix="_paleo_icon.png")
        tmp_image.write(image)
        tmp_image.close()

        return tmp_image.name

    def custom_data(self):
        # -- Resolve the rest api url
        url_name = self.label().replace(" ", "+")
        url = "".join(
            [
                self._TAXA_API,
                "/list.json?rowcount&show=class&show=img&show=full&name=",
                url_name,
            ],
        )

        with urllib.request.urlopen(url) as response:
            all_data = json.load(response)["records"][0]

        era = "unknown"

        if "tei" in all_data:
            era = all_data["tei"]

        if "tli" in all_data:
            era += " to %s" % all_data["tli"]

        return dict(
            phylum=all_data["phl"],
            classification=all_data["cll"],
            era=era,
            mobility=all_data["jmo"],
            environment=all_data["jev"] if "jev" in all_data else "Unknown",
        )