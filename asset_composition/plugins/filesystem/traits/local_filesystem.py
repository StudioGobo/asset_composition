# ----------------------------------------------------------------------------
# Copyright (c) Studio Gobo Ltd 2025
# Licensed under the MIT license.
# See LICENSE.TXT in the project root for license information.
# ----------------------------------------------------------------------------
# File			-> local_filesystem.py
# Created		-> March 2025
# Author		-> Michael Malinowski (Studio Gobo)
# ----------------------------------------------------------------------------
import os
import subprocess

import asset_composition


class LocalFileSystemTrait(asset_composition.Trait):
    """
    This trait represents any file or folder on the users local hard drive. It is
    where we expose functionality that is common to all local files.
    """

    @classmethod
    def can_bind(cls, identifier: str) -> bool:
        if os.path.exists(identifier):
            return True

    def label(self) -> str:
        return os.path.basename(self.asset().identifier())

    def parent(self) -> str:
        return os.path.dirname(
            str(self.asset().identifier()),
        ).replace("\\", "/")

    # ----------------------------------------------------------------------------------
    def actions(self):
        return [
            self.create_action(
                name="Copy Path",
                function=self.copy_path,
                category="System",
                icon="Copy Path",
            ),
            self.create_action(
                name="Open Explorer",
                function=self.explorer,
                category="System",
                icon="Open Explorer",
            ),
        ]

    # ----------------------------------------------------------------------------------
    def copy_path(self):
        cmd = "echo " + self.asset().identifier() + "|clip"
        return subprocess.check_call(cmd, shell=True)

    # ----------------------------------------------------------------------------------
    def explorer(self):
        windows_path = self.asset().identifier().replace('/', '\\')
        command = f'explorer.exe /select, "{windows_path}"'
        os.system(command)


class LocalFileTrait(asset_composition.Trait):
    """
    This trait is bound to any file that exists for a user and is a file
    """

    importance = 1

    @classmethod
    def can_bind(cls, identifier: str) -> bool:
        if os.path.exists(identifier) and os.path.isfile(identifier):
            return True


class LocalFolderTrait(asset_composition.Trait):
    """
    This trait is bound to any folder that exists for a user and is a folder. This
    allows us to define how we get children from this asset.
    """

    @classmethod
    def can_bind(cls, identifier: str) -> bool:
        if os.path.exists(identifier) and os.path.isdir(identifier):
            return True

    def children(self) -> list:

        directories: list = []
        files: list = []

        try:
            for child in os.listdir(self.asset().identifier()):
                absolute_path = os.path.join(
                    self.asset().identifier(),
                    child,
                ).replace("\\", "/")

                if os.path.isdir(absolute_path):
                    directories.append(absolute_path)

                else:
                    files.append(absolute_path)

        except PermissionError:
            return list()

        results = sorted(directories) + sorted(files)
        return results
