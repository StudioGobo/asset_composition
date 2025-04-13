## What is an Asset

At the core of any discussion about asset management in games, 
VFX, or film, lies the fundamental question: *What exactly is 
an asset?* These conversations are always fascinating because 
they are so diverse, often leaving us without a single, 
definitive answer. For example, the definition of an asset 
can vary significantly from one studio to another, or even 
shift from project to project within the same studio. 
Additionally, different disciplines working on the same 
project might have entirely different perspectives on what 
constitutes an asset.


In content creation, it’s common to consider files generated 
in tools like *Maya*, *Blender*, or *Houdini* as assets. Such files 
tend to be highly visible and frequently shared across 
departments. However, when we step back and consider the 
bigger picture, it’s clear that projects are built on far more 
than just these content files. Production teams depend on 
tracking and feedback platforms like *Shotgun* or *Jira*, while 
pipeline developers often maintain databases that store 
relational data between files and other critical information. 
Even director feedback may be delivered through online 
content delivery networks. All this data in its many forms is 
critical to the development of a project. 


If we adopt a broader definition of an asset as anything 
indispensable to a project’s development, it becomes clear 
that limiting our perspective to just files — or worse, a narrow 
subset of files — means engaging with only a fraction of the 
overall process. A truly comprehensive approach requires 
recognition that any form of data can be considered an asset.


When we consider assets as simply data in various forms, 
utilized by a diverse range of people, the challenge of 
designing tools and pipelines around them becomes 
significantly more complex. In this context, we can no longer 
rely on assumptions that assets are files stored in specific 
locations or adhering to particular standards. While some 
assets may fit this mold, many do not. This raises the 
question: how do we begin to create a unified API for assets 
when they can differ so dramatically from one another? The 
key lies in developing a flexible and adaptable framework 
that can accommodate this diversity while maintaining 
consistency and usability across the pipeline.

## Asset Composition

The `asset_composition` library aims to provide a framework to 
address this challenge. At its core is an `Asset` class, which 
is intentionally minimalistic. It takes an *identifier* for 
an asset and exposes basic functionality, such as retrieving 
a label, determining if it has a parent or children, or 
accessing custom data.


The real power, however, lies in its use of the *class 
composition* design pattern, which allows traits to be 
dynamically bound to an asset. For instance, you could 
implement a `FileSystemTrait` that checks whether the asset's 
identifier exists on the user's hard drive. If it does, the 
trait is automatically bound to the asset. There’s no limit 
to the number of traits that can be attached, enabling both 
broad and highly specific functionality. For example, while 
a `FileSystemTrait` might handle general file operations, a 
`HoudiniDigitalAssetTrait` could be designed to bind 
exclusively to files that exist and have the *.hda* extension. 
This flexibility makes the library adaptable to a wide range 
of asset types and use cases.


Both of these examples focus on files, but the concept is 
not restricted in that way. An asset’s *identifier* could 
just as easily be a URL, an ID to resolve from a REST API, 
or a reference to a remote database. *Traits* implement a 
`can_bind` function, where they are passed the *identifier* 
and determine for themselves whether they can bind to the 
asset. This approach keeps traits discrete and 
encapsulated, enabling you to extend an asset’s 
functionality in a highly contextual way.


By adopting this design, our codebase becomes flexible and 
scalable, easily adapting to changing requirements. It also 
allows you to extend functionality to asset types that are 
vastly different from the traditional files we typically 
consider assets. This modularity ensures that your system 
remains robust and adaptable, no matter how diverse your 
assets may be.

## Asset Discovery

We can also implement `Discovery` classes which act as 
specialized search mechanisms, each designed to look for 
assets in specific ways. For example, one `Discovery Plugin` 
might search the user’s local drive, while another could 
query a remote REST API. In all cases, the `Discovery Plugin` 
will each return a list of `Asset` instances. This means 
that, as a developer, you can call a single search function 
and receive the composited results from all available 
Discovery plugins.

This approach creates an incredibly flexible foundation for 
building an *asset pipeline*. It allows you to manage both 
high-level and super specific functionality while 
maintaining strong code encapsulation and modularity. The 
result is a system that is adaptable, scalable, and adheres 
to best practices in software design.

## Asset Explorer

The second library, `asset_explorer`, focuses on visualizing 
assets. It’s an out-of-the-box, user-friendly interface 
built on `Qt`. Once you provide it with the locations of your 
`Traits` and `Discovery` plugins, along with *search roots* (the 
locations to look for assets), the user is presented with 
Assets through various tailored views. This makes it a 
straightforward yet powerful tool for browsing and 
interacting with your assets in a visually intuitive way.

By default, the *Explorer* includes three views: the 
`Hierarchy View`, which displays the hierarchical structure 
of assets (ideal for files on disk or in source control, 
for example); the `Search View`, which is well-suited for 
interacting with more abstract data; and the `Favourites View`,
which shows assets the user has tagged as “favourites” (a 
built-in feature of the `Explorer`). Importantly, all views 
present the same `Asset` objects, and the contextual menus 
for each asset are dynamically generated based on 
functionality declared in the traits. This design allows 
you to easily extend a trait’s functionality and expose it 
to the user with minimal effort, without needing to hardcode 
that functionality into either the `Asset` class or the 
`Explorer` itself. Once again, the flexibility and power of 
the system come down to the traits, ensuring a modular and 
maintainable approach.

Taking the same pattern of flexibility and extendibility, 
all three default views are implemented in a plugin pattern 
approach. This makes it easy for a developer to create 
additional views specific to the needs of a projects or 
data set. 

## Summary

In summary, the entire paradigm is built on the idea that 
assets can be anything — as long as there’s a mechanism to 
identify them. From there, you can create a rich set of 
Traits that define how pipelines, tools, and users interact 
with assets possessing those traits. This approach ensures 
flexibility and adaptability, allowing you to tailor the 
system to your specific needs.
