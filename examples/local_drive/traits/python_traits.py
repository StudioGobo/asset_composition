# ----------------------------------------------------------------------------
# Copyright (c) Studio Gobo Ltd 2025
# Licensed under the MIT license.
# See LICENSE.TXT in the project root for license information.
# ----------------------------------------------------------------------------
# File			-> python_traits.py
# Created		-> March 2025
# Author		-> Michael Malinowski (Studio Gobo)
# ----------------------------------------------------------------------------
import asset_composition
from asset_composition._trait import _TraitAction


class PythonFileTrait(asset_composition.Trait):

    @classmethod
    def can_bind(cls, identifier: str) -> bool:
        if ".py" in identifier:
            return True

    def actions(self) -> list[_TraitAction]:
        return [
            self.create_action(
                name="Get Imports",
                function=self.get_imports,
            )
        ]

    def get_imports(self) -> bool:
        """
        Rough function to demonstrate a trait specific piece of
        functionality
        :return:
        """
        imported_modules: list = []

        with open(self.asset().identifier(), "r") as f:
            for line in f.readlines():
                if "import " in line:
                    imported_modules.append(
                        line.strip().split("import ")[-1].split(" ")[0]
                    )

        return sorted(list(set(imported_modules)))
