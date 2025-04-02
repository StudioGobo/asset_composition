# ----------------------------------------------------------------------------
# Copyright (c) Studio Gobo Ltd 2025
# Licensed under the MIT license.
# See LICENSE.TXT in the project root for license information.
# ----------------------------------------------------------------------------
# File			-> _discovery.py
# Created		-> March 2025
# Author		-> Michael Malinowski (Studio Gobo)
# ----------------------------------------------------------------------------
"""
This module contains the code dedicated to searching and discovering assets

You can search for assets using the following code:

```python
>>> import os
>>> import asset_composition
>>>
>>> results = asset_composition.search(
>>>     os.path.dirname(asset_composition.__file__),
>>>     "*.py",
>>> )
>>>
>>> for result in results:
>>>     print(result.identifier())
```

The search feature will cycle through all available discovery plugins and perform
the search and compound the results together. This means if you had a discovery
plugin for the local disk as well as a plugin for perforce or other such source
control then you can easily search both from the one call.

Results are always returned in the form of Asset classes.
"""
import os

import factories


class DiscoveryPlugin:

    @classmethod
    def search(cls, query, search_from) -> list:
        return list()


class DiscoveryFactory(factories.Factory):
    """
    The trait library is a factory holding a reference to all the available traits.
    Note that this should be treated as a singleton in most situations for the
    purpose of performance.
    """

    # -- Private variable for holding the active instance
    _INSTANCE: "DiscoveryFactory" = None

    def __init__(self, search_paths=None, exclude_builtin=False):
        # -- Initialise the parent class
        super(DiscoveryFactory, self).__init__(
            abstract=DiscoveryPlugin,
            paths=search_paths or list(),
            plugin_identifier="__name__",
        )
