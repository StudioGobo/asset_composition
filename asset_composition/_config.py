# ----------------------------------------------------------------------------
# Copyright (c) Studio Gobo Ltd 2025
# Licensed under the MIT license.
# See LICENSE.TXT in the project root for license information.
# ----------------------------------------------------------------------------
# File			-> _config.py
# Created		-> March 2025
# Author		-> Michael Malinowski (Studio Gobo)
# ----------------------------------------------------------------------------
import json
import os

from . import _discovery, _trait


class Configuration:
    """
    The configuration class contains references to the factories
    and allows the configuration to be serialised to a file if
    required and deserialized from that same file format.
    """

    def __init__(self, filepath: str | None = None):

        # -- We store the reference to the factories as
        # -- private variables, as we consider them
        # -- read only from an instantiation perspective.
        self._trait_factory: _trait.TraitFactory | None = None
        self._discovery_factory: _discovery.DiscoveryFactory | None = None
        self._filepath: str | None = filepath

        # -- If we're given a filepath and that filepath exists
        # -- then we load it from a file
        if filepath:
            self._deserialise(filepath)

        # -- Otherwise we just instantiate the factories in their basic
        # -- form
        else:
            self._initialise()

    def _initialise(self) -> None:

        self._trait_factory = _trait.TraitFactory()
        self._discovery_factory = _discovery.DiscoveryFactory()

    # noinspection SpellCheckingInspection
    def _deserialise(self, filepath: str) -> None:
        """
        This will populate the configuration based on the file
        given

        Args:
            :filepath: The absolute path to the configuration file
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(filepath)

        # -- Start by initialising the factory objects
        self._initialise()

        # -- Read the data file
        with open(filepath, "r") as f:
            data: dict = json.load(f)

        # -- Add all the factory paths
        for path in data["trait_paths"]:
            self.traits.add_path(path)

        for path in data["discovery_paths"]:
            self.discovery.add_path(path)

        # -- Add the disabled traits
        for disabled_trait in data["disabled_traits"]:
            self.traits.set_disabled(disabled_trait, True)

        for disabled_discovery in data["disabled_discoveries"]:
            self.discovery.set_disabled(disabled_discovery, True)

    @property
    def traits(self) -> _trait.TraitFactory:
        """
        Read only accessor to the trait factory

        Returns:
            The Trait Factory
        """
        return self._trait_factory

    @property
    def discovery(self) -> _discovery.DiscoveryFactory:
        """
        Read only accessor to the discovery factory
        Returns:
            The Discovery Factory
        """
        return self._discovery_factory

    def serialise(self, filepath=None) -> dict:
        """
        This will write the state of the configuration to a json
        file.

        Args:
            :filepath: The absolute path to save the configuration file to

        Return:
            Dictionary of saved data
        """

        data = dict(
            trait_paths=self.traits.paths(),
            discovery_paths=self.discovery.paths(),
            disabled_traits=[
                trait
                for trait in self.traits.identifiers(include_disabled=True)
                if self.traits.is_disabled(trait)
            ],
            disabled_discoveries=[
                discovery
                for discovery in self.discovery.identifiers(include_disabled=True)
                if self.discovery.is_disabled(discovery)
            ],
        )

        if filepath:
            self._filepath = filepath

        if self._filepath:
            directory = os.path.dirname(self._filepath)

            if not os.path.exists(directory):
                os.makedirs(directory)

            if self._filepath:
                with open(self._filepath, "w") as f:
                    json.dump(data, f, indent=4, sort_keys=True)

        return data
