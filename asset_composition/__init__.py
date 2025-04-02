# ----------------------------------------------------------------------------
# Copyright (c) Studio Gobo Ltd 2025
# Licensed under the MIT license.
# See LICENSE.TXT in the project root for license information.
# ----------------------------------------------------------------------------
# File			-> __init__.py
# Created		-> March 2025
# Author		-> Michael Malinowski (Studio Gobo)
# ----------------------------------------------------------------------------
"""
Overview
asset_composition is a module which exposes an Asset class which
can be extended and refined through Traits which are non-hierarchical
functional blocks that help build the form and interface of an asset.

What is an Asset
This module was initially written with game/tv/vfx development in mind
and therefore the concept of an asset within this module is essentially
a piece of information which has an identifier.

This could be a file where its identifier is the local filepath. It could
equally be web resource where the identifier is a url. However, essentially
as asset composition is simply a wrapper around a piece of information which
allows it to be exposed via Traits.

What  is a Trait
A trait can be thought of as a piece of functionality that understands
a particular aspect of an asset and can therefore make assumptions about
it and expose information or actions relating to it.

For instance, you might have a trait which only binds to asset identifiers
which it recognises as being files on your hard drive. Because this trait
is specific to local files and will only bind with local file assets it can
safely make assumptions about how to get the size of the file etc. It could
also expose actions to make it easy to show the file in an explorer window or
a shell.

Equally you could have a Trait specific to Perforce, Git, SVN or other source
control mechanism. In this case the trait could check whether you have the latest
version of that file, or who the last person was to edit it.

Crucially Traits are not hierarchical. This is a crucial point to recognise. Instead
a Trait is typically focused on a particular aspect of an asset. This gives a lot
more flexibility than trying to create a rich asset through inheritance. For
instance, if we take the example above where we have a file trait and an source
control trait. Not all files will within source control, and equally not all files
within the source control will be local to the users drive. Therefore there is no
guaranteed safe inheritance structure. But by using traits we can dynamically bind
to assets based on what the asset is.

Fundamentally an asset class does not choose what traits it has, instead when we
instance an asset class it will ask all traits to bind to it if the trait feels
it can.

Getting Started

The easiest way to get started would be to run code like this. In this example
we're importing the asset composition module and we're instancing an asset class
based on a string. In this particular example we're instancing an asset class
for the information "foobar".

```python
>>> import asset_composition
>>> asset = asset_composition.get("foobar")
Asset
```

Out the box, asset_composition comes with a small selection of traits to serve
as examples of what can be achieved. Many of these traits are focused around local
files. Given that "foobar" is not a local file the asset class is instanced but it
will have no traits bound to it because all the available traits have said that
they do not know how to interact with an asset with the given identifier.

Lets try another example. In this example we're passing the filepath to the
asset_composition module. Because this module comes with traits relating to
local files, this will now print the asset and its bound traits.

```python
>>> import asset_composition
>>> asset = asset_composition.get(asset_composition.__file__)
[Asset (LocalFileTrait; LocalFileSystemTrait)]
```

This demonstrates that the traits bound to an asset self-determine whether they
can represent an asset with the given identifier or not, and will only bind to the
asset if they decide they can.

Because this has the LocalFileTrait and the LocalFileSystemTrait, we can start to
ask about its parent, children or actions.

```python
>>> import asset_composition
>>>
>>> # -- Get the asset class for this file
>>> asset = asset_composition.get(asset_composition.__file__)
>>> print(asset)
[Asset (LocalFileTrait; LocalFileSystemTrait)]
>>>
>>> # -- Get the identifier of the parent, and instance an asset
>>> # -- class for the parent identifier
>>> parent_identifier = asset.parent()
>>> parent_asset = asset_composition.get(parent_identifier)
>>>
>>> print(parent_asset)
[Asset (LocalFileSystemTrait; LocalFolderTrait)]
>>> print(parent_asset.identifier())
D:/pydev/develop/asset_management-main/asset_composition
```

In the example above notice that the traits bound to the parent asset are
different to the ones bound to the initial asset. The initial asset
has a LocalFileTrait trait whilst the parent has the LocalFolderTrait. Yet both
have the common LocalFileSystemTrait.

This approach gives a huge amount of flexibility when extending the behaviour
and functionality that an asset can provide. Crucially its done in a highly scalable
way which promotes encapsulated functionality rather than monolithic code.

Creating Traits

Given that Traits are at the core of the asset_composition module it is highly
likely that you will want to implement your own traits to represent your own
types of data. Below is the smallest piece of code you can use to define a trait.

We start by declaring a class which inherits from asset_composition.Trait. We
also implement the can_bind method (not that this is a class method and therefore
must be decorated as such). Whenever an asset is instanced it will ask this trait
if the trait can bind to the asset. It does this by passing the identifier, and
it is then up to the trait to decide whether it can feasibly bind to this asset
or not.

Note that this function can be called a lot - therefore its important
to keep this function lean and optimised. Returning True will mean that
the Trait will be bound to the asset.

```python
import asset_composition

class MyExampleTrait(asset_composition.Trait):

    @classmethod
    def can_bind(cls, identifier: str) -> bool:
        return True
```

Re-implementing Trait Methods

Traits can implement any of the following:

    @xcomposite.take_first
    def label(self) -> str:

    @xcomposite.take_first
    def info(self) -> str:

    @xcomposite.take_first
    def icon(self) -> str:

    @xcomposite.extend_unique
    def status_icons(self) -> list:

    @xcomposite.extend_unique
    def actions(self) -> list:

    @xcomposite.extend_unique
    def children(self) -> list:

    @xcomposite.take_first
    def parent(self) -> str:

    @xcomposite.any_true
    def pull(self):

    @xcomposite.any_false
    def is_visible(self) -> bool:

    @xcomposite.any_false
    def is_valid(self) -> bool:

    @xcomposite.update_dictionary
    def custom_data(self) -> dict:

When re-implementing these functions you do not need to decorate them
like they are listed here, but these decorators show you how the asset
will composite all the results. For instance, multiple traits might
implement the "label" method, but the Asset will take the result from
the first Trait which implements it. Equally the is_valid method will
always return False if any of the traits return False.

Taking note of the composition method is important when deciding how
you want a trait to work. Traits have a class property of "importance"
which is zero by default. But if you have a specific trait which you
always want to come first you can increase its importance value. Traits
are always bound in order of importance.

When we call one of these functions from the asset, such that demonstrated
here, the asset class will cycle over every trait and call the .actions
method if it is implemented. It will then use the xcomposite decorator
outlined above to composite the results. In this case it will return a single
list of all the actions from all the traits bound to the asset.

A more thorough Trait Example

```python
>>> import os
>>> import subprocess
>>> import asset_composition
>>>
>>>
>>> class LocalFileSystemTrait(asset_composition.Trait):
>>>
>>>     @classmethod
>>>     def can_bind(cls, identifier: str) -> bool:
>>>         if os.path.exists(identifier):
>>>             return True
>>>
>>>     def label(self) -> str:
>>>         return os.path.basename(self.asset().identifier())
>>>
>>>     def parent(self) -> str:
>>>         return os.path.dirname(self.asset().identifier()).replace("\\", "/")
>>>
>>>     # ----------------------------------------------------------------------------------
>>>     def actions(self):
>>>         return [
>>>             self.action("Copy Path", self.copy_path, "System", "Copy Path"),
>>>             self.action("Open Explorer", self.explorer, "System", "Open Explorer"),
>>>         ]
>>>
>>>     # ----------------------------------------------------------------------------------
>>>     def copy_path(self):
>>>         cmd = 'echo ' + self.asset().identifier() + '|clip'
>>>         return subprocess.check_call(cmd, shell=True)
>>>
>>>     # ----------------------------------------------------------------------------------
>>>     def explorer(self):
>>>         os.system(
>>>             f"explorer.exe /select, \"{self.asset().identifier()}\""
>>>         )
```
```python
>>> import asset_composition
>>>
>>> asset = asset_composition.get(asset_composition.__file__)
>>> print(asset.actions())
```

Searching For Assets

Asset Composition also implements a flexible and scalable way of searching
for assets through a common interface. Instead of hard coding how assets
should be found, you can instead implement Discovery classes.

These classes have the role of being able to find assets based on a given
starting point and a search query.

For instance, this library comes with a local file search out the box which
returns all the assets within a directory and sub directories, and its implementation
looks like this:

```python
>>> import glob
>>> import asset_composition
>>>
>>> class LocalDiskDiscovery(asset_composition.DiscoveryPlugin):
>>>
>>>     @classmethod
>>>     def search(cls, search_from, query):
>>>         if not query.startswith("*"):
>>>             query = "*" + query
>>>
>>>         if not query.endswith("*"):
>>>             query += "*"
>>>
>>>         results = glob.glob("" + search_from + "/**/"+query, recursive=True)
>>>
>>>         return [
>>>             result.replace("\\", "/")
>>>             for result in results
>>>         ]
```

Therefore the minimal implementation needs only to implement the ```search```
method. From within this method you could be searching a local drive like shown
above or be querying an online rest api, interfacing with a source control system
etc. The only requirement is that it returns a list of identifiers which will then
have asset classes instanced for them.


"""
from ._asset import Asset
from ._compositor import Compositor
from ._config import Configuration
from ._discovery import DiscoveryFactory, DiscoveryPlugin
from ._trait import Trait, TraitFactory

__version__ = "1.2.5"
