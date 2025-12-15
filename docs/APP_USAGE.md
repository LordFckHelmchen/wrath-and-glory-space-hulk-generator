## Usage

### Generator Settings

This section of the app allows you to change the general behavior of the generator.

#### Minimum number of rooms (per origin)

This setting affects the number of rooms that will be rolled on the Wrath & Glory random tables.

The default is a reasonable number for standard games, but higher numbers make for more interesting layouts (and a much
better feel for the scale of space hulks).

If you are lucky, and multiple origins have been rolled for the current space hulk, the number of rooms will be
multiplied by the number of origins.

#### Layouter type

This determines what kind of layouter is used to draw the map of the rolled space hulk. Current options are:

- _GraphvizLayouter_

  This layouter uses the [Graphviz](https://graphviz.org) backend to render an actual graph of the generated space hulk.
  Each node in the graph reflects a room rolled on the random table. The rooms are rendered to scale, e.g. you get an
  actual feeling for the size of a _Vast Hanger_ vs. a _Damaged Consoles_. The edges are the corridors between the rooms
  and can be rendered in several different ways (e.g edged vs. curved). This allows for different looks of the map, for
  example for Eldar a more rounded look might make sense.

- _DeBroglieLayouter_

  This layouter uses the [wave-function collapse](https://github.com/mxgmn/WaveFunctionCollapse)-based
  [DeBroglie](https://github.com/BorisTheBrave/DeBroglie) backend. It renders a (bit-) map from the
  [_Space Hulk board-game tile-set_](https://imgur.com/gallery/k0AsAC8) assembled by
  [aknight2015](https://github.com/aknight2015) & 1632fan. The tile-frequency and shape reflect the original rules from
  the [_Space Hulk board game_](https://en.wikipedia.org/wiki/Space_Hulk). The map is much more oriented to actual
  table-top play, but does not reflect the rolled Space Hulk events (e.g. currently this is generated independently).

#### Layouter Settings

##### GraphvizLayouter

Only available of the according _Layouter type_ is selected.

###### Layout engine

Determines how the space hulk's rooms are arranged.

- _fdp_ gives a good, regular layout.
- _circo_ is more organic and gives very interesting results for higher number of rooms. However, it might fail to
  create a proper layout! I use this for Eldar or Ork origins
- _osage_ gives a very regular, packed layout

_NOTE_: These options are a subset of graphviz's [_Layout Engines_](https://graphviz.org/docs/layouts).

###### Connection type

Determines how the rooms are connected, e.g. how the hallways are drawn.

- _ortho_ produces rectangular connections, that look most like "built hallways". If the number of rooms is large, this
  might fail due to overlapping edges, especially with the _circo_ engine. In such cases the layout will simply fallback
  to straight lines.
- _spline_ makes curved lines, that might have less overlap than the straight lines.
- _line_ makes simple, straight lines between the rooms. This works best with _circo_.

_NOTE_: These options are a subset of graphviz's [_splines_](https://graphviz.org/docs/attrs/splines) attributes.

##### DeBroglieLayouter

Only available of the according _Layouter type_ is selected. This layouter currently has not settings.

### Space Hulk

This section allows you to

- *Create new hulk?*

  This generates a new space hulk and a new map

- *Create new layout*

  This only creates a new map but keeps the generated space hulk

- *Download PDF*

  This lets you download the generated space hulk and the created map

  - The *GraphvizLayouter* generates a vectorized (read "high-resolution") map
  - The *DeBroglieLayouter* only creates a (rather low-res) bitmap

Initially, only the _Create new hulk?_ option is available. After you created a first hulk, the other two options become
visible.
