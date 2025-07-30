# CHANGELOG


## v0.11.0 (2025-05-26)

### Bug Fixes

- Add custom exception for unset environment variables
  ([`784080a`](https://github.com/bhklab/damply/commit/784080a42b927e6f9dc5bf94b1e940ddc283e045))

- Adjust test for Windows path handling to set strict mode explicitly
  ([`57db00a`](https://github.com/bhklab/damply/commit/57db00a24484b857a5d7674942c587a4e34c75af))

- Restore assertion for Windows file owner retrieval test
  ([`9986a79`](https://github.com/bhklab/damply/commit/9986a7989e061c108d4e09d55de779753871ffba))

- Update sha256 checksum for damply package version 0.10.0
  ([`0be6951`](https://github.com/bhklab/damply/commit/0be695117bbe86d476753edc2a7cde339a29faba))

### Chores

- Update version and checksum in pixi.lock; modify README metadata
  ([`b480d2b`](https://github.com/bhklab/damply/commit/b480d2babb75c0226e00dc8174a3fdc86f0a77b1))

### Documentation

- Clean up index.md
  ([`3b1d489`](https://github.com/bhklab/damply/commit/3b1d489aa0f41e12f083f826c9d041e451a0541c))

- Remove about page
  ([`c960dbd`](https://github.com/bhklab/damply/commit/c960dbdd9211c08b56d8cea175d6332bf3457200))

- Update to mkdocs
  ([`6f8c456`](https://github.com/bhklab/damply/commit/6f8c456f49917d8fe8233ee3ede81f03fc40d308))

### Features

- Add documentation for DamplyDirs module and its usage
  ([`74d9c79`](https://github.com/bhklab/damply/commit/74d9c7987d8bdf8affbdef12b6985c8382432b0a))

- Add Windows support to CI workflow matrix
  ([`650c192`](https://github.com/bhklab/damply/commit/650c19286021844586937c3d11ecb2b916f82c48))

- Implement DamplyDirs singleton initialization and add comprehensive tests
  ([`c48deb9`](https://github.com/bhklab/damply/commit/c48deb97837259542950c1ab6d31831ee911c31a))

- Refactor damplydirs logic, include documentation, and add comprehensive tests
  ([`cf026d4`](https://github.com/bhklab/damply/commit/cf026d4ff0351af3cc109e2d802ddc14c9b1c78e))

feat: refactor damplydirs logic, include documentation, and add comprehensive tests

### Refactoring

- Streamline directory structure handling and improve error management
  ([`00ad73d`](https://github.com/bhklab/damply/commit/00ad73dd79d364b7950410c39898c39c04aebd42))

- Update file owner tests for platform-specific handling and improve readability
  ([`860d04f`](https://github.com/bhklab/damply/commit/860d04fb8d1a30928c08e7633b494d1be3f7087c))


## v0.10.0 (2025-05-20)

### Bug Fixes

- Update pypi references from '.' to './' for consistency
  ([`bc1715f`](https://github.com/bhklab/damply/commit/bc1715f7b692b5ea8f6ab239df1c698c7e419f0d))

- Update repository references and descriptions from jjjermiah to bhklab
  ([`ad73779`](https://github.com/bhklab/damply/commit/ad73779b06649b2e1f173eea26f2d508b871ab15))

### Chores

- Comment out Test-PyPi-Installation and Publish-To-Test-PyPi jobs in CI workflow
  ([`2ed0229`](https://github.com/bhklab/damply/commit/2ed0229f43e0b0a3b46cf52a77478840afcf305b))

- Format and lint
  ([`5130657`](https://github.com/bhklab/damply/commit/5130657f3fd937dd4e0ea15079df9e1473adeac6))

- Move ruff config out and update deps
  ([`2f5a3fe`](https://github.com/bhklab/damply/commit/2f5a3fe4defebcb19bfcf7abc0643ce405787523))

- Reformat
  ([`7a275c7`](https://github.com/bhklab/damply/commit/7a275c772c8d86f8223c746625fc35f621fc4f05))

- Remove empty __init__.py file from dmpdirs directory
  ([`47ff2cd`](https://github.com/bhklab/damply/commit/47ff2cd9916039b8397fd02141d8a1a422a657b6))

- Update lockfile
  ([`aa9e4d9`](https://github.com/bhklab/damply/commit/aa9e4d93ceeaed09c559f2e71ff9e7af8a9675da))

### Code Style

- Standardize indentation and formatting in whose.py
  ([`07e495f`](https://github.com/bhklab/damply/commit/07e495f9a54c366abee030a832e7f92662a6e073))

### Continuous Integration

- Disable fail-fast in job strategy for improved stability across OS matrix
  ([`f84c26e`](https://github.com/bhklab/damply/commit/f84c26e43579614623633649967e5aa310adf0bf))

- Streamline Codecov integration by removing redundant steps and ensuring coverage tracking
  ([`eb1fdef`](https://github.com/bhklab/damply/commit/eb1fdef4fa4f776d0c5d26a243863dd23fa02831))

- Update actions versions
  ([`5e341a8`](https://github.com/bhklab/damply/commit/5e341a83e909251f756d33eebf4d16b59759aa24))

### Features

- Add dmpdirs module for standardized project directory access
  ([`dc324e6`](https://github.com/bhklab/damply/commit/dc324e612f72d4cde802377dd9ae98d421705afd))

- Add dmpdirs module for standardized project directory access
  ([`0eeb8c5`](https://github.com/bhklab/damply/commit/0eeb8c58a35ae3b81c41a843567092acc76931f5))

- Update dependencies and refactor codebase
  ([`6b9905c`](https://github.com/bhklab/damply/commit/6b9905c1acf8e09d60b3812f3206b909d38178c1))

- Added `pybytesize` dependency to `pyproject.toml`. - Refactored `DirectoryAudit` to use
  `path.stat()` instead of `os.stat()`. - Enhanced documentation in `DamplyDirs` class for better
  clarity on usage and available directories. - Renamed `DirectoryNotFoundError` to
  `DirectoryNameNotFoundError` for better accuracy. - Updated import statement for `ByteSize` to use
  the new package location. - Refactored `damplyplot` function to improve variable naming and
  clarity. - Removed obsolete `ByteSize` class and related tests. - Improved type hints across
  various modules for better code clarity. - Updated exception handling in `whose.py` for better
  error messages. - Cleaned up unused imports and improved code formatting.

### Refactoring

- Comment out Codecov steps in CI workflow for clarity
  ([`368671c`](https://github.com/bhklab/damply/commit/368671c326a809871d7c6636ae5b90691e3753dd))

- Organize imports and improve formatting across multiple files
  ([`6d3d97a`](https://github.com/bhklab/damply/commit/6d3d97af3440659f73bf8672d318ffc1327e5760))

- Rename DirectoryNotFoundError to DirectoryNameNotFoundError for clarity; remove unused test
  ([`b3bd833`](https://github.com/bhklab/damply/commit/b3bd8334ad4ce25f85fab2a7e087e2dc60277013))

- Restore and enable Codecov steps in CI workflow for coverage tracking
  ([`6c7e4ee`](https://github.com/bhklab/damply/commit/6c7e4ee59544b4f1ed06c2a3df09ccfe89cbd44b))


## v0.9.0 (2024-08-20)

### Bug Fixes

- Minor fixes
  ([`ed09859`](https://github.com/bhklab/damply/commit/ed09859ed2db399600c710efaf9b34a7e130548a))

- Minor updates
  ([`1a1d60c`](https://github.com/bhklab/damply/commit/1a1d60cabf9f3987cc4ac16a01e1cd6cc18afbd0))

### Chores

- Update
  ([`9c129ff`](https://github.com/bhklab/damply/commit/9c129ff220177921bfb1f78639f0d35129beebe0))

### Features

- Field adding
  ([`b9780c5`](https://github.com/bhklab/damply/commit/b9780c512425fecd20cbe7b04991ae9b05e93480))


## v0.8.0 (2024-08-01)

### Bug Fixes

- Add tests and fix common root
  ([`3cb4199`](https://github.com/bhklab/damply/commit/3cb4199966275374bbb8b5ab4a93e3a8ba695946))

- Merge
  ([`e6ae533`](https://github.com/bhklab/damply/commit/e6ae53385aad671164427d75edfbe1cb3c1851e4))

- Tests for whose command
  ([`f08d6c2`](https://github.com/bhklab/damply/commit/f08d6c2de2df8a79cd7320aaada18b44c5608c82))

### Chores

- Format and clean
  ([`26bfaf3`](https://github.com/bhklab/damply/commit/26bfaf3b22ed4eaa0c51ab856ff4e1459f1617fb))

### Features

- Add basic audit
  ([`e8c307e`](https://github.com/bhklab/damply/commit/e8c307e3f5e6f5133d1efeabd18f8243f30d82e5))

- Added size check
  ([`219b653`](https://github.com/bhklab/damply/commit/219b6534ba92f42e3e734924e4c2c571c16837ae))

- Init and config subcommands
  ([`578dfda`](https://github.com/bhklab/damply/commit/578dfdaa7ba73d5d865ab2c3a6eea2e2f059cf04))

- Organize cli commands
  ([`e25a966`](https://github.com/bhklab/damply/commit/e25a9664810b385404bb4f2e4ad293db9e1b15b9))


## v0.7.1 (2024-07-31)

### Bug Fixes

- Update cli tool
  ([`9ea8c5a`](https://github.com/bhklab/damply/commit/9ea8c5a9dde55366f2014027dc753f79d9955744))


## v0.7.0 (2024-07-31)

### Bug Fixes

- Fix arrangement
  ([`3e94e4a`](https://github.com/bhklab/damply/commit/3e94e4aff321a5b4fec8e388084565609294b56a))

- Gha to not use locked
  ([`1233f00`](https://github.com/bhklab/damply/commit/1233f00e3ad0e0404ab6513643d3be77c694800c))

- Lint and format and cleanup
  ([`c877847`](https://github.com/bhklab/damply/commit/c877847d18b2f9623b1c963b6f84c7fba4cfba59))

- Update gha to not use locked pixi
  ([`189294e`](https://github.com/bhklab/damply/commit/189294e4883e8fbd65f794461d1ed92e95a12476))

- Update gha to not use locked pixi, add plot to cli
  ([`255e08e`](https://github.com/bhklab/damply/commit/255e08ef8dfaa583ed8946dc41b724759409754d))

### Features

- Add damply plotting
  ([`dcc72e1`](https://github.com/bhklab/damply/commit/dcc72e1bbcd69fe2b4cdc0e9abac8a443f06ca1e))


## v0.6.0 (2024-05-31)

### Bug Fixes

- Lint
  ([`b0abdf4`](https://github.com/bhklab/damply/commit/b0abdf46b416c20f0fb148dd59fadc70761a8815))

- Lock
  ([`4168366`](https://github.com/bhklab/damply/commit/41683662fe792097f017e70013c73d38ded5bf34))

### Features

- Major refactoring of cli
  ([`5998541`](https://github.com/bhklab/damply/commit/5998541bf75be1e7d2fcf8536d1d230dae4919bb))


## v0.5.0 (2024-05-31)

### Chores

- Add tests
  ([`79044ef`](https://github.com/bhklab/damply/commit/79044effb782111c2b1cbccfc21b4a77431d9f5c))

### Features

- Add lazy loading for images in README view
  ([`7d1e053`](https://github.com/bhklab/damply/commit/7d1e053b18f63fbc8c27e6abf813b67eb7f3955d))

- Add whose and file size
  ([`04772d4`](https://github.com/bhklab/damply/commit/04772d49bb4a4ae7656dbb3bb1931a3c76ec544a))


## v0.4.1 (2024-05-31)

### Bug Fixes

- Format
  ([`e153b30`](https://github.com/bhklab/damply/commit/e153b30f32108b0a9750f1a4b0c7e0b00116c152))

- Update metadata table title in cli.py
  ([`a63c36b`](https://github.com/bhklab/damply/commit/a63c36bba26d880abf433cf06690faecb1537d3d))

- Version
  ([`ecefaaf`](https://github.com/bhklab/damply/commit/ecefaafab444f70ace8a8185240d6577fe4db0a3))

### Chores

- Update navigation links in mkdocs.yaml
  ([`931524b`](https://github.com/bhklab/damply/commit/931524b39f8ca9edb971c8a43b84dc858b4a2de8))


## v0.4.0 (2024-05-31)

### Bug Fixes

- Lint
  ([`64944d3`](https://github.com/bhklab/damply/commit/64944d3025cc20721aa5415c882b42e737daa3da))

- Refactor get_file_owner_full_name function for improved error handling and platform compatibility
  ([`f4fca58`](https://github.com/bhklab/damply/commit/f4fca58d63e4667f8c3fc60b51776a038757c669))

### Features

- Add cli whose
  ([`b15ec32`](https://github.com/bhklab/damply/commit/b15ec32b551533aab892b3b3227e2091c643dfe1))

- Update CLI help messages and add 'whose' command
  ([`620f209`](https://github.com/bhklab/damply/commit/620f209656ab91d5f8ae4e11608eaa6aef05e3f9))


## v0.3.0 (2024-05-31)

### Chores

- Delete config/.pypackage-builder-answers.yml
  ([`a04cabd`](https://github.com/bhklab/damply/commit/a04cabd468901e3b47e236a31d9eb867feea7719))

### Features

- Add cli
  ([`1e825d1`](https://github.com/bhklab/damply/commit/1e825d1e71293cb46fcb8abe6498b5a695982e39))

- Add cli tool
  ([`077e52b`](https://github.com/bhklab/damply/commit/077e52bf1e3c529685a631aee6978e59676b0165))


## v0.2.0 (2024-05-31)

### Bug Fixes

- Tests so it makes file
  ([`69d4e54`](https://github.com/bhklab/damply/commit/69d4e54ea76ef75dde242e28261ee79b60bc2093))

### Features

- Add tests and major class
  ([`569177b`](https://github.com/bhklab/damply/commit/569177b476047cadb22ae84d0eeb92ad1fb370ea))

- Refactor metadata.py for improved readability and maintainability
  ([`cf909e0`](https://github.com/bhklab/damply/commit/cf909e0f1824fdc9275171d10c3c2a87049521e7))


## v0.1.1 (2024-05-31)

### Bug Fixes

- Some pypi issues
  ([`c6f810e`](https://github.com/bhklab/damply/commit/c6f810ea4859a45b4d9f1b3432cca1f45dc29f30))


## v0.1.0 (2024-05-31)

### Bug Fixes

- Update gitignore
  ([`97e8fde`](https://github.com/bhklab/damply/commit/97e8fde80ab3a6f38f62a231ffe5fc189983fe05))

### Features

- Add docs and test
  ([`76e92ff`](https://github.com/bhklab/damply/commit/76e92ff24b5e8febb361df0f01d1d063d26ef703))

- Add github actions
  ([`85891c4`](https://github.com/bhklab/damply/commit/85891c4fcd221f3c61874a2c6cec9edc059e94af))

- First commit
  ([`8ed31c9`](https://github.com/bhklab/damply/commit/8ed31c972b3ac76f4def1b02bb50c6fee84a2172))
