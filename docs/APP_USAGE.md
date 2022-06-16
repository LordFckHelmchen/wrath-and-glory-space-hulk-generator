## Usage

### Generator Settings

This section of the app allows you to change the general behavior of the generator.

#### Minimum number of rooms (per origin)

Does what it says. If you are lucky and roll multiple origins, the number will be multiplied by the number of origins.
The default is a reasonable number of standard games, but if higher numbers make for more interesting layouts (and a
much better feel for the scale of space hulks)

#### Layout engine

Determines how the space hulk's rooms are arranged.

- _fdp_ gives a good, regular layout.
- _circo_ is more organic and gives very interesting results for higher number of rooms. However, it might fail to
  create a proper layout! I use this for Eldar or Ork origins
- _osage_ gives a very regular, packed layout

_NOTE_: These options are a subset of graphviz's [_Layout Engines_](https://graphviz.org/docs/layouts).

#### Connection type

Determines how the rooms are connected, e.g. how the hallways are drawn.

- _ortho_ produces rectangular connections, that look most like "built hallways". If the number of rooms is large,
  this might fail due to overlapping edges, especially with the _circo_ engine. In such cases the layout will simply
  fallback to straight lines.
- _spline_ makes curved lines, that might have less overlap than the straight lines.
- _line_ makes simple, straight lines between the rooms. This works best with _circo_.

_NOTE_: These options are a subset of graphviz's [_splines_](https://graphviz.org/docs/attrs/splines) attributes.

### Space Hulk

This section allows you to create a new space hulk, a new layout or to export the created layout as a vectorized (read
"high-resolution") PDF file. Initially, only the _Create new hulk?_ option is available. After you created a first hulk,
the other two options become visible.

_NOTE_: Currently only the actual map is exported without the non-map-related events (e.g. origins, occupants). This
will be fixed in a next release. I'm currently figuring-out how to best do this (so input is once again welcome)!