# ----------------------------------------------------------------------------
# Copyright (c) Studio Gobo Ltd 2025
# Licensed under the MIT license.
# See LICENSE.TXT in the project root for license information.
# ----------------------------------------------------------------------------
# File			-> _trait.py
# Created		-> March 2025
# Author		-> Michael Malinowski (Studio Gobo)
# ----------------------------------------------------------------------------
from typing import Callable

import factories


class Trait:
    """
    A trait is a block of functionality that can be assigned to an asset. Traits use
    sideways inheritance rather than vertical and therefore an asset might have
    multiple traits that implement the same function. In this scenario the
    xcomposite return rules define how the return will be rationalized.
    """

    # -- If you declare a trait as lightweight it will always be bound
    # -- but there should be a strong emphasis on the trait to perform
    # -- all its binding and initialisation in a high performant manor.
    lightweight: bool = False

    # -- Most assets will have multiple traits bound to it. You can use the
    # -- importance value to declare how important this trait is. Traits are
    # -- always bound in order of importance, which is important for any functions
    # -- that resolve with a take_first logic.
    importance: int = 0

    def __init__(self, asset: "asset_composition.Asset"):
        self._asset: "asset_composition.Asset" = asset

    def asset(self) -> "asset_composition.Asset":
        """
        This will return the asset class this trait is bound to
        """
        return self._asset

    @classmethod
    def can_bind(cls, identifier: str) -> bool:
        """
        This function is where you should test whether this trait is suitable to be
        bound to a trait with the given identifier.
        """
        return False

    def create_action(
        self, name, function, category=None, icon=None, hidden=False
    ) -> "_TraitAction":
        return _TraitAction(
            name=name,
            function=function,
            category=category,
            icon=icon or "Action",
            hidden=hidden,
        )


# --------------------------------------------------------------------------------------
class _TraitAction(object):
    """
    This is a structure defining the name, functionality and category of an action
    which an asset can have
    """

    def __init__(
        self,
        name: str,
        function: Callable,
        category: str = "",
        icon: str = "",
        hidden: bool = False,
    ):
        self._name: str = name
        self._function: Callable = function
        self._category: str = category
        self._icon: str = icon
        self._hidden: bool = hidden

    def name(self) -> str:
        return self._name

    @property
    def function(self) -> Callable:
        return self._function

    def category(self) -> str:
        return self._category

    def icon(self) -> str:
        return self._icon

    def hidden(self) -> bool:
        return self._hidden

    @property
    def call(self) -> Callable:
        return self.function

    def __repr__(self) -> str:
        return f"[Action:{self.category()}:{self.name()}]"


class TraitFactory(factories.Factory):
    """
    The trait library is a factory holding a reference to all the available traits.
    Note that this should be treated as a singleton in most situations for the
    purpose of performance.
    """

    # -- Private variable for holding the active instance
    _INSTANCE: "TraitFactory" = None

    def __init__(self, search_paths=None, exclude_builtin=False):
        # -- Initialise the parent class
        super(TraitFactory, self).__init__(
            abstract=Trait,
            paths=search_paths or list(),
            plugin_identifier="__name__",
        )
