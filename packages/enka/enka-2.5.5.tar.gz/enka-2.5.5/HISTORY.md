# [2.5.5](https://github.com/seriaati/enka-py/compare/v2.5.4..v2.5.5) - 2025-05-27

## Bug Fixes

- Correct parameter order in PROFILE_API_URL formatting - ([cb097c4](https://github.com/seriaati/enka-py/commit/cb097c44a2dde1d716d3f636826ae0fe1580a45a))
- Raise EnkaAPIError immediately - ([fea4a5c](https://github.com/seriaati/enka-py/commit/fea4a5c290b837d45712712e964134c7f723bf57))
- Fix package not being published to pypi in bump-version.yml - ([0f91bcb](https://github.com/seriaati/enka-py/commit/0f91bcb5d835d3520696d254ac422c8f46af05e3))

## Continuous Integrations

- Remove biweekly release - ([3c26c49](https://github.com/seriaati/enka-py/commit/3c26c49206490e3ed8e5a155cd98e77c89858ba8))
- Modify workflow PR trigger - ([d2753fe](https://github.com/seriaati/enka-py/commit/d2753feedfaddcaab4414b439733a4b5de8af1bf))
- Add bump version workflow - ([e75c9e9](https://github.com/seriaati/enka-py/commit/e75c9e99193a0e1897595f813553e597b539fec1))
- Remove Python version specifier in release.yml - ([7f45967](https://github.com/seriaati/enka-py/commit/7f459673d433b64c4b617ea828854d8df5534b96))

## Documentation

- Add profile API reference page - ([c31deb9](https://github.com/seriaati/enka-py/commit/c31deb93b095e5783ee17fbddc6e54256f3c4e63))
- Add profile endpoint tutorial - ([9366958](https://github.com/seriaati/enka-py/commit/936695853080ab8e97d34208f5df183edba45cf5))
- Improve clarity in profile fetching section - ([6ada0c6](https://github.com/seriaati/enka-py/commit/6ada0c61f8fb2962632949d06cbf8fd2fc7d4dfb))
- Improve profile endpoint docs - ([9def308](https://github.com/seriaati/enka-py/commit/9def3085b74fc586d79c3b0f78642521f7a9acb0))
- Update README - ([22ab78c](https://github.com/seriaati/enka-py/commit/22ab78c9ebfb399ae914b91bb45caf17c8eb1e0f))
- Add ZZZ support notice - ([14c1653](https://github.com/seriaati/enka-py/commit/14c165375d169d1132d0011e2f1779bebc897e35))

## Features

- Add request timeout handling and configuration ([#108](https://github.com/seriaati/enka-py/issues/108)) - ([a30df6b](https://github.com/seriaati/enka-py/commit/a30df6be18f41580ed197de74beb06800fb345fa))
- Add OwnerInput typed dict - ([103a39a](https://github.com/seriaati/enka-py/commit/103a39aefa3bb753975490bb78a8bad30e09140d))
- Find wrong UID format early on - ([efc0c41](https://github.com/seriaati/enka-py/commit/efc0c417237de9b69c715584fcb18683c34a6176))
- Add fetch_builds method to ZZZClient and define Build model - ([4cb3616](https://github.com/seriaati/enka-py/commit/4cb361669b30c7f6f374b7addeb4355df0a1d673))
- Add backup API for HSR ([#109](https://github.com/seriaati/enka-py/issues/109)) - ([3172d13](https://github.com/seriaati/enka-py/commit/3172d13e7d6670d56855e486b1fa6e19d2b792c1))

## Refactoring

- Move profile endpoint fetch to BaseClient - ([dd04b8a](https://github.com/seriaati/enka-py/commit/dd04b8ab5742c429fd300344c9f94119f1ba3fa6))
- Move API endpoint URLs to a single file - ([e438b45](https://github.com/seriaati/enka-py/commit/e438b45eb239f49877120b297c4fbc082536ea9d))

## Style

- Make all imports relative - ([65c5b3a](https://github.com/seriaati/enka-py/commit/65c5b3a60dedb6334a4f8698fd311b9745adc9b8))
- Organize imports - ([875a999](https://github.com/seriaati/enka-py/commit/875a99971c2cbb82f5d6d5b73f61dc458efd2cfd))

## Tests

- Add test for fetch_builds method in ZZZClient - ([6d962f1](https://github.com/seriaati/enka-py/commit/6d962f107da1efe712cba575f30bd7bdf812d2d8))
- Fix test failing for empty showcase - ([c3eed34](https://github.com/seriaati/enka-py/commit/c3eed342ed0ef15b07ccbfd1fa3227f30ad358e1))
- Add fetch_builds tests for HSR and GI - ([0772221](https://github.com/seriaati/enka-py/commit/0772221176c690b255c4e04d185eccc5b6fd29ab))

