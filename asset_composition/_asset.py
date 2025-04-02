# ----------------------------------------------------------------------------
# Copyright (c) Studio Gobo Ltd 2025
# Licensed under the MIT license.
# See LICENSE.TXT in the project root for license information.
# ----------------------------------------------------------------------------
# File			-> _asset.py
# Created		-> March 2025
# Author		-> Michael Malinowski (Studio Gobo)
# ----------------------------------------------------------------------------
import signalling
import xcomposite


class Asset(xcomposite.Composition):
    """
    The asset class represents a single asset. An asset is simply a class that
    represents something with an identifier. The identifier could be a filepath or
    a url or something else entirely.

    It is then up to the traits to decide whether they can bind to this asset based
    on the identifier.

    Some traits are heavier than others, so we make a distinction between
    lightweight traits and heavy traits. That way if a user only wants a quick
    access to a trait they can choose to instance this class with only traits that
    are marked as being lightweight.

    If you want a fully functional version of the asset, you should leave the
    lightweight flag as false.

    Args:
        identifier (str): The identifier of the asset.
        compositor: The Compositor class which instanced this asset.
        lightweight (bool): Marks the asset as lightweight, meaning it will only
            bind to lightweight traits. This is useful to prevent heavy traits
            binding when you dont need them.
    """

    # noinspection PyUnresolvedReferences
    def __init__(
        self,
        identifier: str,
        compositor: "asset_composition.Compositor",
        lightweight: bool = False,
    ):
        super(Asset, self).__init__()

        # -- Store the trait factory or instance one. Note that if we instance one
        # -- we're using it as a singleton.
        self.compositor: "asset_composition.Compositor" = compositor

        # -- Store the identifier privately, so we make it read only
        self._identifier: str = identifier
        self._lightweight: bool = lightweight

        # -- ALlow this class (or any traits) to notify this asset that it has
        # -- has changed in some meaningful way
        self.status_changed: signalling.Signal = signalling.Signal()
        self.changed: signalling.Signal = signalling.Signal()

        # -- Perform our binding
        self._perform_trait_binding(self._lightweight)

    def identifier(self) -> str:
        """
        Returns the identifier for this asset.
        """
        return self._identifier

    def is_lightweight(self) -> bool:
        """
        When an asset class is instantiated, it can be instanced in a lightweight mode
        meaning that not all traits will be bound, and only traits that are considered
        featherweight will be bound.

        This is particularly useful if you're querying a lot of assets but do not
        need a great deal of functionality from it.
        """
        return self._lightweight

    def _perform_trait_binding(self, lightweight: bool = False) -> None:
        """
        Private function that performs the binding. All existing bound traits
        will be removed, then traits will be re-applied. Note that traits are
        always bound in order of importance.
        """
        # -- Clear any existing traits
        for trait in self.traits()[:]:
            print(trait)
            self.unbind(trait)

        # -- Get the traits in order of importance
        traits = sorted(
            self.compositor.configuration.traits.plugins(),
            key=lambda t: t.importance,
            reverse=True,
        )

        for trait in traits:

            # -- If we're only binding lightweight traits and this trait is not
            # -- lightweight, then we skip it
            if lightweight and not trait.lightweight:
                continue

            # -- Perform the binding if its viable
            if trait.can_bind(self.identifier()):
                self.bind(trait(asset=self))

        # -- Update our lightweight flag to represent our new state
        self._lightweight = lightweight

    def fully_load(self) -> None:
        """
        If you have loaded an asset in a lightweight binding you can call this to
        fully bind
        """
        self._perform_trait_binding(lightweight=False)

    def traits(self) -> list:
        """
        Returns a list of the trait classes bound to this asset
        """
        return self.components()

    def trait_names(self) -> list:
        """
        Returns a list of trait names which are bound to this asset
        """
        results: list = []

        for component in self._components:
            results.append(component.__class__.__name__)

        return results

    @xcomposite.take_first
    def label(self) -> str:
        """
        The label is a short-hand human-readable representation for the asset
        """
        return str(self)

    @xcomposite.take_first
    def info(self) -> str:
        """
        This can be used for tooltip information. By default it will return the identifier
        """
        return str(self.identifier())

    @xcomposite.take_first
    def icon(self) -> str:
        """
        This allows a trait to determine the icon that the asset should use to
        represent it in any interfaces
        """
        return ""

    @xcomposite.extend_unique
    def status_icons(self) -> list:
        """
        This allows a trait to determine the status icon that the asset should use to
        represent it in any interfaces
        """
        return []

    @xcomposite.extend_unique
    def actions(self) -> list:
        """
        This will return a list of TraitAction classes
        """
        return []

    @xcomposite.extend_unique
    def children(self) -> list:
        """
        This should resolve any children relative to the asset this trait is bound to
        """
        return []

    @xcomposite.take_first
    def parent(self) -> str:
        """
        This should resolve the parent asset this trait is bound to
        """
        return ""

    @xcomposite.any_true
    def pull(self) -> bool:
        """
        This should ensure that the the asset is available for use. If the trait
        has performed an action and ensured its ready then it should return True
        """
        return False

    @xcomposite.any_false
    def is_visible(self) -> bool:
        """
        If you dont want an asset item to be visible to interfaces you should
        return False in this.
        """
        return True

    @xcomposite.any_false
    def is_valid(self) -> bool:
        """
        If you dont want an asset item to be visible to interfaces you should
        return False in this.
        """
        return True

    @xcomposite.update_dictionary
    def custom_data(self) -> dict:
        return {}

    def action(self, action_name):
        """
        This will attempt to return the action with the given name
        """
        for action_ in self.actions():
            if action_.name() == action_name:
                return action_

        return None

    def has_action(self, action_name) -> bool:
        for action in self.actions():
            if action.name() == action_name:
                return True
        return False
