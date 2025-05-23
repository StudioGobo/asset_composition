# Overview

asset_composition is a module which exposes an Asset class which
can be extended and refined through Traits which are non-hierarchical
functional blocks that help build the form and interface of an asset.

# What is an Asset

This module was initially written with game/tv/vfx development in mind
and therefore the concept of an asset within this module is essentially
a piece of information which has an identifier.

This could be a file where its identifier is the local file path. It could
equally be a web resource where the identifier is a URL or id. However, essentially
an asset composition is simply a wrapper around a piece of information which
allows it to be exposed and represented via Traits.

# What is a Trait

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

Crucially Traits are not hierarchical. Instead a Trait is typically focused on a
particular aspect type of asset. This gives a lot more flexibility than trying to
create a rich asset through inheritance.

For instance, if we take the example above where we have a file trait and an source
control trait. Not all files will be within source control, and equally not all files
within the source control will be local to the users drive. Therefore there is no
guaranteed safe inheritance structure. But by using traits we can dynamically bind
to assets based on what the asset is.

Fundamentally an asset class does not choose what traits it has, instead when we
instance an asset class it will ask all traits to bind to it if the trait feels
it can.

# Configuration & Compositors

In order to use the compositional asset you first need to instance a Compositor.
A `Compositor` is a very light weight class which requires a configuration (explained
further below) and then exposes the following two methods:

- get(identifier): This method will attempt to resolve the `Asset` class for the given identifier. The resulting `Asset` will have all its traits bound to it

- search(query, search_from): This allows you to search based on a query and also a reference point. This will then return `Asset` classes for all the matching results

Both of these methods use dynamic functionality to construct the response. To instance
an `Asset` class, the `get` function will query traits to see which can help represent
the given identifier. Equally the mechanism to search for assets is not hard coded
either. Instead you can implement `DiscoveryPlugins' which allow you to tailor how
assets can be searched for. All available discovery plugins will be utilised and a
unique list will be returned.

This makes it possible to do things like searching your local hard drive (through a
local disk discovery plugin) as well as searching source control (using a git discovery
plugin) and having the results combined.

Because both of these mechanisms rely on plugins, they are each managed by factories
that are ultimately searching in various locations for `Trait` and `Discovery` classes.

To make this easier to manage, `asset_composition` exposes a `Configuration` class
where you can declare any plugin paths as well as any disabled plugins.

Crucially, you can save a configuration to a file, and reload from that configuration,
meaning you don't have to initialise it manually every time, equally you can use that
configuration file in a deployment.

# Running the Examples

The `asset_composition` module comes with two examples:

- `examples/local_drive`: This shows the composition module in its most simplistic 
form. It uses a discovery mechanism to search the location of files within the 
modules own location. It then uses `FileSystemTraits` to enrich the output.

- `examples/paleobio`: This example shows how traits can be used to bind to 
a REST API and represent dinosaur taxonomy as assets.

### Getting Setup

In order to run the examples you **must** install the required python dependencies, 
which are :

- factories
- scribble
- xcomposite
- signalling

All of these can be installed using `pip install <modulename>`

You **must** place the `asset_composition` module in a location where your python
interpreter can import it. Typically this is in the site-packages folder of your python
or virtual env. Alternatively you can use `sys.path.append("")` within your 
script/main.py to add the folder containing the module to the python path so that
it is importable. 

Once this is setup you can execute the `main.py` as an argument of your python 
executable, such as: `python.exe c:/my_python/examples/local_drive/main.py`


# Getting Started

To start with you must create a configuration. In this example we create a
configuration, and add both trait and discovery paths to it - in this case
pointing the `Configuration` at the traits and discovery plugins that come
built in to the `asset_composition` library.

```python
import os
import asset_composition

# -- Create a new configuration
configuration = asset_composition.Configuration()

# -- Add the built in traits
configuration.traits.add_path(
    os.path.join(
        os.path.dirname(asset_composition.__file__),
        "plugins",
        "filesystem",
        "traits",
    ),
)
configuration.discovery.add_path(
    os.path.join(
        os.path.dirname(asset_composition.__file__),
        "plugins",
        "filesystem",
        "discovery",
    ),
)
```

Optionally, you can save the configuration using...

```python
configuration.serialise(filepath="foobar.json")
```

If a configuration file already exists, you can instance it using...

```python
asset_composition.Configuration(filepath="foobar.json")
```

Once you have a configuration, you can then instance a `Compositor` class simply
by passing your configuration as an argument. From there you can start to query
assets by passing an identifier.

```python
import asset_composition

compositor = asset_composition.Compositor(
    configuration=asset_composition.Configuration(filepath="foobar.json"),
)

asset = compositor.get("foobar")
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
asset = compositor.get(asset_composition.__file__)
[Asset (LocalFileTrait; LocalFileSystemTrait)]
```

This demonstrates that the traits bound to an asset self-determine whether they
can represent an asset with the given identifier or not, and will only bind to the
asset if they decide they can.

Because this has the LocalFileTrait and the LocalFileSystemTrait, we can start to
ask about its parent, children or actions.

```python
compositor = asset_composition.Compositor(configuration)

# -- Get the asset class for this file
asset = compositor.get(asset_composition.__file__)
print(asset)
#[Asset (LocalFileTrait; LocalFileSystemTrait)]

# -- Get the identifier of the parent, and instance an asset
# -- class for the parent identifier
parent_identifier = asset.parent()
parent_asset = compositor.get(parent_identifier)

print(parent_asset)
#[Asset (LocalFileSystemTrait; LocalFolderTrait)]
print(parent_asset.identifier())
#D:/pydev/develop/asset_management-main/asset
```

In the example above notice that the traits bound to the parent asset are
different to the ones bound to the initial asset. The initial asset
has a LocalFileTrait trait whilst the parent has the LocalFolderTrait. Yet both
have the common LocalFileSystemTrait.

This approach gives a huge amount of flexibility when extending the behaviour
and functionality that an asset can provide. Crucially its done in a highly scalable
way which promotes encapsulated functionality rather than monolithic code.

# Creating Traits

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
import os
import subprocess
import asset_composition


class LocalFileSystemTrait(asset_composition.Trait):

    @classmethod
    def can_bind(cls, identifier: str) -> bool:
        if os.path.exists(identifier):
            return True

    def label(self) -> str:
        return os.path.basename(self.asset().identifier())

    def parent(self) -> str:
        return os.path.dirname(self.asset().identifier()).replace("\\", "/")

    # ----------------------------------------------------------------------------------
    def actions(self):
        return [
            self.action("Copy Path", self.copy_path, "System", "Copy Path"),
            self.action("Open Explorer", self.explorer, "System", "Open Explorer"),
        ]

    # ----------------------------------------------------------------------------------
    def copy_path(self):
        cmd = 'echo ' + self.asset().identifier() + '|clip'
        return subprocess.check_call(cmd, shell=True)

    # ----------------------------------------------------------------------------------
    def explorer(self):
        os.system(
            f"explorer.exe /select, \"{self.asset().identifier()}\""
        )
```

```python
import asset_composition

asset = asset_composition.get(asset_composition.__file__)
print(asset.actions())
```

# Searching For Assets

Asset Composition also implements a flexible and scalable way of searching
for assets through a common interface. Instead of hard coding how assets
should be found, you can instead implement Discovery classes.

These classes have the role of being able to find assets based on a given
starting point and a search query.

For instance, this library comes with a local file search out the box which
returns all the assets within a directory and sub directories, and its implementation
looks like this:

```python
import glob
import asset_composition


class LocalDiskDiscovery(asset_composition.DiscoveryPlugin):

    @classmethod
    def search(cls, query, search_from):
        if not query.startswith("*"):
            query = "*" + query

        if not query.endswith("*"):
            query += "*"

        results = glob.glob("" + search_from + "/**/"+query, recursive=True)

        return [
            result.replace("\\", "/")
            for result in results
        ]
```

Therefore the minimal implementation needs only to implement the `search`
method. From within this method you could be searching a local drive like shown
above or be querying an online rest api, interfacing with a source control system
etc. The only requirement is that it returns a list of identifiers which will then
have asset classes instanced for them.

# Testing

This module has ~90% test coverage, when adding or extending functionality it is
strongly recommended to add more tests to asset_composition.tests. These are implemented
using unittest and therefore come with no additional dependency.
