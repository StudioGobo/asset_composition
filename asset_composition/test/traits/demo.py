# ----------------------------------------------------------------------------
# Copyright (c) Studio Gobo Ltd 2025
# Licensed under the MIT license.  
# See LICENSE.TXT in the project root for license information.
# ----------------------------------------------------------------------------
# File			-> demo.py
# Created		-> March 2025
# Author		-> Michael Malinowski (Studio Gobo)
# ----------------------------------------------------------------------------
import asset_composition

class EmptyTrait(asset_composition.Trait):
    pass

class MostBasicTrait(asset_composition.Trait):

    lightweight = True

    @classmethod
    def can_bind(cls, identifier):
        return True

    def label(self):
        return self.asset().identifier()

    def info(self):
        return "Basic Info"

    def icon(self):
        return "Basic Icon"

    def status_icons(self):
        """
        This allows a trait to determine the status icon that the asset should use to
        represent it in any interfaces
        """
        return ["Status Icon"]

    def custom_data(self):
        return {"Basic Data": True}

class HeavyTrait(asset_composition.Trait):

    lightweight = False

    @classmethod
    def can_bind(cls, identifier):
        return True


class BindOnlyToPyFiles(asset_composition.Trait):

    @classmethod
    def can_bind(cls, identifier):
        if ".py" in identifier.lower():
            return True


class NeverBindToPyFiles(asset_composition.Trait):

    @classmethod
    def can_bind(cls, identifier):
        if ".py" in identifier.lower():
            return False

        return True

class LowImportanceTrait(asset_composition.Trait):

    importance = 0

    @classmethod
    def can_bind(cls, identifier):
        return  True

    def label(self):
        return "low_importance"


class HighImportanceTrait(asset_composition.Trait):
    importance = 1

    @classmethod
    def can_bind(cls, identifier):
        return True

    def label(self):
        return "high_importance"

class InvalidTrait(asset_composition.Trait):

    @classmethod
    def can_bind(cls, identifier):
        if "invalid test" in identifier.lower():
            return True

    def is_valid(self):
        return False

class ActionTrait1(asset_composition.Trait):

    @classmethod
    def can_bind(cls, identifier):
        return True

    def actions(self):
        return [
            self.create_action(
                name="Action 1",
                function=ActionTrait1.action_1,
                category="Simple Actions",
                icon=None,
            )
        ]

    @staticmethod
    def action_1():
        return 1

class ActionTrait2(asset_composition.Trait):

    @classmethod
    def can_bind(cls, identifier):
        return True

    def actions(self):
        return [
            self.create_action(
                name="Action 2",
                function=ActionTrait1.action_1,
                category="Simple Actions",
                icon=None,
            )
        ]

    @staticmethod
    def action_2():
        return 2


class ChangeTrait1(asset_composition.Trait):

    @classmethod
    def can_bind(cls, identifier):
        return True

    def pull(self):
        self.asset().changed.emit()
        return True
