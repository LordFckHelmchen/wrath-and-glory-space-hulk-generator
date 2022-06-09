# Wrath & Glory Space Hulk Generator

[Use Cases](docs/USE_CASES.md)

## ToDo

### Generator

- [space_hulk.py](src/generator/space_hulk.py)
    - [ ] FEAT: Add name & description field to
    - [ ] FEAT: Link occupations & purposes

### App

- [ ] FEAT: Implement change of space hulk properties from [hulk_property_changer.py](src/app/hulk_property_changer.py)
    - [ ] FEAT: Log change of hulk props
        - [ ] FIX: Crash with duplication-adjusted event collection entries
        - [ ] FIX: Crash on empty selection of fields that require at least 1 entry (e.g. origins)
        - [ ] FIX: Reassignment of values in case of `EventCountOutOfRangeError`