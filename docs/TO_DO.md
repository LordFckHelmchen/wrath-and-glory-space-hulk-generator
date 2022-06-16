# Open To-Dos

## Generator

- [space_hulk.py](src/generator/space_hulk.py)
    - [ ] FEAT: Add name & description field to
    - [ ] FEAT: Link occupations & purposes
- [ ] FEAT: Add Floor Tiling (via [WaveFunctionCollapse](https://github.com/ikarth/wfc_2019f)?)

## App

- [ ] FEAT: Add top-level description & how to
- [ ] FEAT: Communicate Graphviz edge type fallback warning to user to avoid simply nothing happening on edge type
  change
- [ ] FIX: Use memoizable_cache instead of cache in [layout_file_creator.py](src/app/layout_file_creator.py)
- [ ] FEAT: Implement change of space hulk properties from [hulk_property_changer.py](src/app/hulk_property_changer.py)
    - [ ] FEAT: Log change of hulk props
    - [ ] FIX: Crash with duplication-adjusted event collection entries
    - [ ] FIX: Crash on empty selection of fields that require at least 1 entry (e.g. origins)
    - [ ] FIX: Reassignment of values in case of `EventCountOutOfRangeError`

