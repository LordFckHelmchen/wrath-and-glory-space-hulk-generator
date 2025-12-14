# CHANGELOG

<!-- version list -->

## v2.1.0 (2025-12-14)

### Build System

- Switch to uv from poetry
  ([`404513c`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/404513c0282c21467aa6b0f391e25dcc382da370))

### Chores

- Add missing newline
  ([`f0260da`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/f0260da4ef6e3b6be6b8a32445ffd3d0b6195aaa))

- Add missing newline
  ([`adfe987`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/adfe98712d60faea618ecfab197367a84d2fce03))

### Continuous Integration

- Rework semantic release pipeline
  ([`e93d217`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/e93d21728bfb4e52afe24ba19273c3ad81a7db19))

### Features

- Added semantic releases
  ([`ce08c1a`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/ce08c1a43195e44accec857164938145623b429c))


## v2.0.0 (2023-05-14)

### Bug Fixes

- Create parent directory before attempting to copy preview
  ([`11b0340`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/11b03400545c1354795cb87df999db9aec87917e))

- Update preview when creating a new layout
  ([`88681c0`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/88681c08d815fac62fb8a13ac2b14d7a1064df18))

### Build System

- Add img2pdf dependency
  ([`9e03d84`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/9e03d846ad793f4011c1aa4aa1bf4257ff93599d))

- Add pytest action dependencies and update lock file
  ([`75937ec`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/75937ec14a3d3ba044bcd28256c2f63c4ca17db2))

- Update dev-dependencies
  ([`b2669e0`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/b2669e0d7bb7708a5c7f5e73723bfe5553d55e6e))

### Chores

- Add space hulk tiles
  ([`d60aac6`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/d60aac6e7ac3ef8289dddcd6243269c7919e44f8))

- Bump version & add space hulk board game keyword
  ([`ecd71eb`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/ecd71eb9aa3576744f48effa143dff8a23021d6b))

### Continuous Integration

- **pytest**: Enable md-report & emojis on pytest-action
  ([`571ad3a`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/571ad3a5c45397f2c01da9e76e482552d6362764))

- **tests**: Add names for stages
  ([`125f9ae`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/125f9ae505cad009858a32a8a84a2b165e5cc9e0))

- **tests**: Change to pytest + Coveralls
  ([`9f73913`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/9f73913c8ef12ee110d10bb631dd2c89f94a753f))

### Documentation

- Add coverage badge
  ([`072b723`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/072b72362c498d194c108fb2fae99a196fc633b1))

- Add DeBroglie to usage description
  ([`c312da8`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/c312da878da59488d74e13c47f83eb93a943aac1))

- Add details on development
  ([`a108189`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/a108189b0ac9ea2f1ca6c43d4d33ef0ff5f2f0f9))

- Extend export section of usage description
  ([`4fb7a1f`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/4fb7a1f893dc382403d85c99677f812784d6b6b1))

- Fix some errors in README
  ([`1a014a2`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/1a014a25514dbe063aa9d0ccdb18e8d8f88d9fc9))

- Update screenshot
  ([`201b0e8`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/201b0e8e6f28778798cffcf96aedda0d11aabd73))

### Features

- Add DeBrouglie Linux executable
  ([`0b149e0`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/0b149e0720ec67dc8d8b851bf83c1793cb513026))

- Add first working version of space hulk game rules
  ([`ceccfe7`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/ceccfe7ec42c07aa453b4f0a45b1e430865b8718))

- Add Space Hulk game tiles & DeBrouglie config
  ([`e35a5b6`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/e35a5b63223bea9c2b1d1ac601e8d1297c060259))

- Pave the way for wfc-based space hulk game layout with more tests
  ([`94cd804`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/94cd804c79a1aab6fd5ec878f1b26432172e1740))

### Refactoring

- Don't create dedicated file-type variable
  ([`8e31005`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/8e31005e5fd6b057d74102e651c7057b21b505dc))

- First batch of changes for layouter interface
  ([`afccd4c`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/afccd4c255240675274b26dd802cd62d94a9adf2))

- More reorganization of the layouters
  ([`f6192d1`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/f6192d121de3d00384d0ad978f723419534305d1))

- Move IndexableEnum to top-level layouter
  ([`5d433f9`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/5d433f93a7d45e33d9b7b80ea32e73eb46119d2b))

- Next batch of changes for layouter interface
  ([`2c4c330`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/2c4c330d949c2d5d9f761220a84c01fb4ddd7a8d))

- Remove duplicated tile config
  ([`408f8e7`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/408f8e7ae92ea632bb6c9bcd0b413a351d339427))

- Reorganize repo layout for new layouter class
  ([`5e4f8bf`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/5e4f8bfbfda50f1660659eba816549dad403c74b))

### Testing

- Change to pytest
  ([`653c53f`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/653c53f2d10a7edb284e7469c4f3265d52ff620a))

- Try to fix deadlock in app test
  ([`9294040`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/9294040385927d91ddc4424b9891367f6be1a1d6))


## v1.3.5 (2023-03-12)

### Bug Fixes

- Fix import error for PositiveInt
  ([`2a21b94`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/2a21b94efaa54d86ee486bc344659be164769899))

### Build System

- Add poetry config
  ([`3672bd5`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/3672bd51fc7df8b01774bd612bf9f2770b9ef9d5))

- Fix & extend pyproject.toml metadata
  ([`dc0ea21`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/dc0ea212c16604c5c27d135006e65ac1e4851916))

- **ruff**: Allow print output in tests
  ([`47eef5b`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/47eef5b083a381641fecb9d01b873b231bfd7bf5))

- **ruff**: Change isort config to single-line
  ([`cf0dd82`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/cf0dd82dbd1608abd2fd0d9c9e0e051071bbaa93))

- **ruff**: Ignore some more annotation issues
  ([`076fe6f`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/076fe6f261b1ce28740329a10c244526a63ab51c))

### Chores

- Add logs to ignore
  ([`63fdf16`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/63fdf1688b52f7621d268354f7dac50132672d25))

- Add ruff cache to gitignore
  ([`04cb6cb`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/04cb6cb1eb1b75f2abb32a3e0e5fb89a18b0ea53))

- Bump version
  ([`a9b6897`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/a9b6897ffbd5e6579b8fc722a0371fee5a848560))

- Correctly gitignore all generated files
  ([`eba8b14`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/eba8b146dc08b9673f044feb8e0512b95e5ccb6d))

- Update python version to match GH's version
  ([`2aa7862`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/2aa7862246bd88bdf7aca30640f2caab6f97b802))

### Continuous Integration

- Archive generated html output from app test
  ([`06a3cf0`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/06a3cf05997da1c822a2eaca6e8b97568d3c9c72))

- Attempt to cache dependencies for successive runs
  ([`0d0e0f0`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/0d0e0f0d35560189f7f90d6db4c2c165c5b6f27b))

- Separate code check steps & remove codeQL
  ([`6159c30`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/6159c30acbaf622581bef03d5c38e83cf3bec1ed))

- Separate tests & linting from codeQL
  ([`b6e2727`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/b6e2727471eb892117fb50f197770f253d44c967))

- Switch poetry action
  ([`200631b`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/200631b3b238662570d217494cb3f84efdf0249a))

- Try to always archive generated html output from app test
  ([`cf9ddf0`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/cf9ddf05f532656a907f5658517f8c67216f824d))

- Updated poetry & add ruff & black
  ([`cb829bc`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/cb829bc0760da5d1306ad462aa3b40a61f686ee0))

### Documentation

- Add ruff & black badges
  ([`d2c11f8`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/d2c11f8d8b4e1642c6685be75ab85d687532c3a5))

- Change build badge
  ([`c6744d0`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/c6744d08f827c920e54b8f4f90266a7ce6e42308))

### Refactoring

- Black format files
  ([`8982898`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/898289850f333a5f6845a22242058d2710d75649))

- Fix all other issues with ruff
  ([`190a412`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/190a412253bd461fdbf3f0fb70d31c006cdf2cd8))

- Fix fixable issues with ruff
  ([`15e8472`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/15e8472f250a4e288cd34d84932f31d8bf170889))

- Fix ruff issues in streamlit_app
  ([`fa52d54`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/fa52d5490a88b1ca5d76249eddd0cdfee2d99404))

- Remove defaulted options from streamlit config
  ([`38b729e`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/38b729e0e66f660d28dacb68da974da7f191d4e5))

### Testing

- Add generated html output to app test
  ([`7f45f54`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/7f45f5401b94c1dac9eb806e2f5b67774e383871))

- Add init file to tests
  ([`c989b95`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/c989b954fd2b52e1852c4390503331d3bbc2453c))

- Add retry attempt for app test to circumvent initial run problems
  ([`679d9cf`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/679d9cf5977c17d3533e110b96a6c9b359a4ada7))

- Assert output equality before response code equality in app test
  ([`acf324e`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/acf324ef398ce09a3d3752219e449529130876c1))

- Create output before assert in app test
  ([`be0cee8`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/be0cee84303043e3968f91409ea2d72e6f686765))

- Extend initial wait time and add diagnostics for app test
  ([`40fd1f6`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/40fd1f6177d483a079e1a24d005b9b11ab59eb5e))

- Fix wrong test class name in app test
  ([`dd51ff0`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/dd51ff001b0e7d55334e1f6d7c952cf89aefe681))

- Make asserts subtests in app test and add some diagnostics
  ([`a5f2bc6`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/a5f2bc613ee13924cf3cd7001dea8c06f982c9fe))


## v1.3.4 (2022-10-14)

### Build System

- **deps**: Bump protobuf from 3.20.1 to 3.20.2
  ([`de677d7`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/de677d7ae2aeb0fcb110275e9344fac5e253912d))

- **deps**: Update dependencies and bump version
  ([`1fc63e0`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/1fc63e0c3a307351dbdeecd3c2c9fe5b3f578d63))


## v1.3.2 (2022-09-05)

### Build System

- **deps**: Bump mistune from 0.8.4 to 2.0.3
  ([`7f8013e`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/7f8013e65c216ec1a64bef67d37dbfece34bb324))

- **deps**: Bump nbconvert from 5.5.0 to 6.5.1
  ([`ddb1327`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/ddb1327fb5db9812f5a8956209a898404da4ab8f))

### Chores

- Bump version
  ([`80dab2b`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/80dab2bd9778b68947d105fb34ed38df0325d2f6))

- Bump version
  ([`7f8c21b`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/7f8c21b2d4ba8fcd998eaf26b43431fd75141d39))

### Continuous Integration

- Add poetry to install dependencies
  ([`168e1b4`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/168e1b4e4acc85817658b3897a2b081503fcd4ad))

- Add unittest execution step
  ([`1b21e55`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/1b21e55d9c7bd0295246dea2fc6ed5477b6697de))

- Change schedule and target branch for CodeQL
  ([`a7a9e9a`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/a7a9e9a43469fc9339d8de1f1db1f6c4cae510cb))

- Fix ImportError for test directory
  ([`3e0d141`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/3e0d1419ed6563efb5a875450b4122cfcc95dc0e))

- Fix wrong unittest command
  ([`aedeb4c`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/aedeb4ca21284afa5014cd5d86d92d000421d289))

### Documentation

- Add more badges to README
  ([`af722c2`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/af722c270644fcaa32e00f52019160ea8126b116))


## v1.3.1 (2022-08-02)

### Build System

- Update dependencies
  ([`008fe7c`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/008fe7c7b12cc6497e994581c9d540248195f5ba))

### Chores

- Bump version
  ([`57ec13d`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/57ec13dfbc3779b78aeaf979339fefd5598fd2ef))

### Documentation

- Fix run command in README.md
  ([`db47852`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/db478526ba2485152ec5cb855b610a2d245fca01))

- Remove note on missing space hulk details from docs.
  ([`acba3f4`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/acba3f4cf822a7ddfa8fc239794d7957b3b2820d))


## v1.3.0 (2022-07-02)

### Features

- Add support for full-data pdf-export
  ([`0e90c1c`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/0e90c1cb743b8bacf1a9bd5473d9d64c7a6d83c2))

- Store space hulk details in exported pdf
  ([`67890b7`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/67890b789573cb7a22cad88fe783a896c6a070dc))


## v1.2.1 (2022-06-21)

### Bug Fixes

- Indexable enum not being iterable error and move default properties of layouter out of class
  ([`3edbd88`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/3edbd885cbcf778b3512fb29c1de639940a3932a))

### Build System

- Use badge for version display in app & use experimental_memo for version caching
  ([`4ebdd9b`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/4ebdd9b37b1e8c1ce20a0b0f6f1ae944cfc4fd9a))

### Chores

- Update dependencies
  ([`9bc43f1`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/9bc43f1d1a3e8766f071e5e2dc63c5bc8512fd03))

### Features

- Provide direct-access properties for layout engine & edge type to avoid accessing the default
  values
  ([`0b27e31`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/0b27e317c15cd8cd2b311b07d962d040d35066c0))

### Refactoring

- Move metrics above preview & restructure app code
  ([`e0f0ad5`](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/commit/e0f0ad540fe41cb2f09e30426d0a78d9134f4479))


## v1.0.0 (2022-06-20)

- Initial Release
