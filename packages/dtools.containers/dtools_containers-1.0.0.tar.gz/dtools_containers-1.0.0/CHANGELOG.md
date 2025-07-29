# CHANGELOG

PyPI dtools.containers project.

- Strict 3 digit semantic versioning (adopted 2025-05-19)
  - MAJOR version for incompatible API changes
  - MINOR version for backward compatible added functionality
  - PATCH version for backward compatible bug fixes

## Releases and Important Milestones

### Version 1.0.0 - PyPI release date 2025-05-TBA

- first PyPI release as dtools.containers
  - box.py -> stateful (mutable) container that can contain 0 ot 1 items
  - functional_tuple.py -> easier starting point to inherit from tuple
  - immutable_list.py -> immutable, guaranteed hashable "list"
  - maybe.py -> implements the "maybe" monad from FP
  - xor.py -> implements a left biased either monad from FP

### Adapting strict Semantic from this point on - date 2025-05-19

- [Semantic Versioning 2.0.0](https://semver.org/)
- see top of file
- previous versioning scheme used
  - first digit - major event, epoch, or paradigm shift
  - second digit - breaking API changes, major changes
  - third digit - bug fixes, API additions, docstring changes

### Version 0.27.1 - PyPI release date 2025-04-22

- replaced camelCaseNames method names with snake_case_names
- docstring changes
- pyproject.toml standardization

### Version 0.27.0 - PyPI release date 2025-04-07

- first PyPI release as dtools.tuples
  - split dtools.datastructures into
    - dtools.tuples
    - dtools.queues
- typing improvements

### Version 0.25.1 - PyPI release date 2025-01-16

- Fixed pdoc issues with new typing notation
  - updated docstrings
  - had to add TypeVars

### Version 0.25.0 - PyPI release date 2025-01-17

- First release under dtools.datastructures name

### Version 0.24.0 - PyPI release date 2024-11-18

- Changed flatMap to bind thru out project

### Version 0.23.1 - PyPI release date 2024-11-18

- Fixed bug with datastructures.tuple module
  - forgot to import std lib typing.cast into tuples.py

### Version 0.22.3.0 - Preparing for a 0.23.0 PyPI release

- renamed class FTuple -> ftuple
  - ftuple now takes 0 or 1 iterables, like list and tuple do
- created factory function for original constructor use case
  - FT\[D\](\*ds: D) -> ftuple[D]

### Version 0.22.1 - PyPI release date 2024-10-20

- removed docs from repo
- docs for all grscheller namespace projects maintained
  [here](https://grscheller.github.io/grscheller-pypi-namespace-docs/).

### Version 0.22.0 - PyPI release date 2024-10-18

- made classes in nodes module less passive with better encapsulation
- compatible with:
  - grscheller.fp >= 1.0.0 < 1.01
  - grscheller.circular-array >= 3.6.1 < 3.7

### Version 0.21.0 - PyPI release date 2024-08-20

- got back to a state maintainer is happy with
  - many dependencies needed updating first

### Version 0.20.5.1 - datastructures coming back together 2024-08-19

- works with all the current versions of fp and circular-array
- preparing for PyPI 0.21.0 release

### Version 0.20.5.0 - datastructures coming back together 2024-08-17

- updated to use grscheller.fp.nada instead of grscheller.untyped.nothing
  - made debugging tons easier
- updated to use all latest PyPI versions of dependencies
- three failed tests involving class SplitEnd
- putting off PyPI v1.0.0 release indefinitely
  - all dependencies need to be at v1.0+
  - need to work out SplitEnd bugs
  - still need to finalize design (need to use it!)
  - need to find good SplitEnd use case
  - other Stack variants like SplintEnd??? (shared data/node variants?)

### Version 0.20.2.0 - Going down a typing rabbit hole 2024-08-03

- still preparing for the 1.0.0 datastructures release
  - as I tighten up typing, I find I must do so for dependencies too
  - using `# type: ignore` is a band-aid, use `@overload` and `cast` instead
  - using `@overload` to "untype" optional parameters is the way to go
  - use `cast` only when you have knowledge beyond what the typechecker can know

### Version 0.19.0 - PyPI release date 2024-07-15

- continuing to prepare for PyPI release 1.0.0
- cleaned up docstrings for a 1.0.0 release
- changed accumulate1 to accumulate for FTuple
- considering requiring grscheller.fp as a dependency

### Version 0.18.0.0 - Beginning to prepare for PyPI release 1.0.0

- first devel version requiring circular-array 3.1.0
- still some design work to be done
- TODO: Verify flatMap family yields results in "natural" order

### Version 0.17.0.4 - Start of effort to relax None restrictions

- have begun relaxing the requirement of not storing None as a value
  - completed for queues.py
- requires grscheller.circular-array >= 3.0.3.0
- perhaps next PyPI release will be v1.0.0 ???

### Version 0.16.0.0 - Preparing to support PEP 695 generics

- Requires Python >= 3.12
- preparing to support PEP 695 generics
  - will require Python 3.12
  - will not have to import typing for Python 3.12 and beyond
  - BUT... mypy does not support PEP 695 generics yet (Pyright does)
- bumped minimum Python version to >= 3.12 in pyproject.toml
- map methods mutating objects don't play nice with typing
  - map methods now return copies
  - THEREFORE: tests need to be completely overhauled

### Version 0.14.1.1 - Preparing to add TypeVars

- tests working with grscheller.circular-array >= 3.0.0, \<3.2
  - lots of mypy complaints
  - first version using TypeVars will be 0.15.0.0

### Version 0.14.0 - PyPI release date 2024-03-09

- updated dependency on CircularArray class
  - dependencies = ["grscheller.circular-array >= 0.2.0, < 2.1"]
- minor README.md woodsmithing
- keeping project an Alpha release for now

### Version 0.13.3.1 - Preparing for another PyPI release soon

- overhauled docstrings with Markdown markup
- updated pyproject.py to drop project back to an Alpha release
  - allows more renaming flexibility
  - intending to develop more graph based data structures
- renamed class core.nodes.Tree_Node to core.node.BT_Node
  - BT for Binary Tree (data in each node of tree)
- created class core.nodes.LT_Node
  - LT for Leaf Tree (data are the leaves of the tree)
- removed deprecated reduce method from various classes
  - use foldL instead

### Version 0.13.2 - PyPI release date 2024-02-20

- Forgot to update pyproject.toml dependencies
  - dependencies = ["grscheller.circular-array >= 0.1.1, < 1.1"]

### Version 0.13.1 - PyPI Release date 2024-01-31

- FTuple now supports both slicing and indexing
- more tests for FTuple
  - slicing and indexing
  - map, foldL, accumulate methods
  - flatMap, mergeMap, exhaustMap methods
- forgot to update CHANGELOG for v0.13.0 release

### Version 0.13.0 - PyPI Release date 2024-01-30

- BREAKING API CHANGE - CircularArray class removed
- CircularArray moved to its own PyPI & GitHub repos
  - https://pypi.org/project/grscheller.circular-array/
  - https://github.com/grscheller/circular-array
- Fix various out-of-date docstrings

### Version 0.12.3 - PyPI Release date 2024-01-20

- cutting next PyPI release from development (main)
  - if experiment works, will drop release branch
  - will not include `docs/`
  - will not include `.gitignore` and `.github/`
  - will include `tests/`
  - made pytest >= 7.4 an optional test dependency

### Version 0.12.2 - PyPI Release date 2024-01-17

- fixed Stack reverse() method
  - should have caught this when I fixed FStack on last PyPI release
  - more Stack tests

### Version 0.12.1 - PyPI Release date 2024-01-15

- BUG FIX: FStack reverse() method
- added more tests

### Version 0.12.0 - PyPI Release date 2024-01-14

- Considerable future-proofing for first real Beta release

### Version 0.11.3.4 - Finally decided to make next PyPI release Beta

- Package structure mature and not subject to change beyond additions
- Will endeavor to keep top level & core module names the same
- API changes will be deprecated before removed

### Version 0.11.0 - PyPI Release date 2023-12-20

- A lot of work done on class CLArray
  - probably will change its name before the next PyPI Release
    - perhaps to "ProcessArray" or "PArray"
- Keeping this release an Alpha version
  - mostly for the freedom to rename and restructure the package

### Version 0.10.17.0+ (0.11.0-RC2) - 2023-12-17

- Second release candidate - probably will become next PyPI release
  - main now development branch, release will be release branch
  - decided to drop it back to Alpha
    - making datastructures a Beta release was premature
    - classifier "Development Status :: 3 - Alpha"
  - will cut next PyPI release with Flit from release branch
  - will need to regenerate docs on release & move to main
  - things to add in main before next release
    - will not make Maybe Nothing a singleton
    - last touched CLArray refactor
    - improve CLArray test coverage
  - Things for future PYPI releases
    - inherit FTuple from Tuple (use __new__) for performance boost
    - hold off using __slots__ until I understand them better

### Version 0.10.14.2 (0.11.0-RC1) - 2023-12-11

- First release candidate - unlikely this will be the next PyPI release
  - will cut next PyPI release with Flit from main branch
  - removed docs directory before merge (docs/ will be main only)
  - things to add in main before next release
    - make Maybe Nothing a singleton (use __new__)
    - derive FTuple from Tuple (use __new__) for performance boost
    - simplify CLArray to use a Queue instead of CircularArray & iterator
    - start using __slots__ for performance boost to data structures
      - efficiency trumps extensibility
      - prevents client code adding arbitrary attributes & methods
      - smaller size & quicker method/attribute lookups
      - big difference when dealing with huge number of data structures

### Version 0.10.14.0 - commit date 2023-12-09

- Finished massive renaming & repackaging effort
  - to help with future growth in future
  - name choices more self-documenting
  - top level modules
    - array
      - CLArray
    - queue
      - FIFOQueue (formerly SQueue)
      - LIFOQueue (LIFO version of above)
      - DoubleQueue (formerly DQueue)
    - stack
      - Stack (formerly PStack)
      - FStack
    - tuple-like
      - FTuple

### Version 0.10.11.0 - commit date 2023-11-27

- Created new datastructures class CLArray
  - more imperative version of FCLArray
    - has an iterator to swap None values instead of a default value
      - when iterator is exhausted, will swap in () for None
    - no flatMap type methods
    - map method mutates self
    - can be resized
    - returns false when CLArray contains no non-() elements
  - TODO: does not yet handle StopIteration events properly
- made package more overall "atomic"

### Version 0.10.10.0 - commit date 2023-11-26

- More or less finalized FCLArray API
  - finished overriding default flatMap, mergeMap & exhaustMap from FP
  - need mergeMap & exhaustMap versions of unit tests
  - found this data structure very interesting
    - hopefully find a use for it
  - considering a simpler CLArray version

### Version 0.10.8.0 - commit date 2023-11-18

- Bumping requires-python = ">=3.11" in pyproject.toml
  - Currently developing & testing on Python 3.11.5
  - 0.10.7.X will be used on the GitHub pypy3 branch
    - Pypy3 (7.3.13) using Python (3.10.13)
    - tests pass but are 4X slower
    - LSP almost useless due to more primitive typing module

### Version 0.10.7.0 - commit date 2023-11-18

- Overhauled __repr__ & __str__ methods for all classes
  - tests that ds == eval(repr(ds)) for all data structures ds in package
- CLArray API is in a state of flux
  - no longer stores None as a value
  - __add__ concatenates, no longer component adds
  - maybe allow zero length CLArrays?
    - would make it a monoid and not just a semigroup
    - make an immutable version too?
- Updated markdown overview documentation

### Version 0.10.1.0 - commit date 2023-11-11

- Removed flatMap methods from stateful objects
  - FLArray, DQueue, SQueue, PStack
  - kept the map method for each
- some restructuring so package will scale better in the future

### Version 0.9.1 - PyPI release date: 2023-11-09

- First Beta release of grscheller.datastructures on PyPI
- Infrastructure stable
- Existing datastructures only should need API additions
- Type annotations working extremely well
- Using Pdoc3 to generate documentation on GitHub
  - see https://grscheller.github.io/datastructures/
- All iterators conform to Python language "iterator protocol"
- Improved docstrings
- Future directions:
  - Develop some "typed" containers
  - Add sequence & transverse methods to functional subpackage classes
  - Monad transformers???
  - Need to use this package in other projects to gain insight

### Version 0.8.4.0 - commit date 2023-11-03

- new data structure FTuple added
  - wrapped tuple with a FP interface
  - initial minimal viable product

### Version 0.8.3.0 - commit date 2023-11-02

- major API breaking change
  - now two versions of Stack class
    - PStack (stateful) with push, pop, peak methods
    - FStack (immutable) with cons, tail, head methods
  - FLarray renamed FLArray
- tests now work

### Version 0.8.0.0 - commit date 2023-10-28

- API breaking changes
  - did not find everything returning self upon mutation
- Efforts for future directions
  - decided to use pdoc3 over sphinx to generate API documentation
  - need to resolve tension of package being Pythonic and Functional

### Version 0.7.5.0 - commit date 2023-10-26

- moved pytest test suite to root of the repo
  - src/grscheller/datastructures/tests -> tests/
  - seems to be the canonical location of a test suite
- instructions to run test suite in tests/__init__.py

### Version 0.7.4.0 - PyPI release date: 2023-10-25

- More mature
- More Pythonic
- Major API changes
- Still tagging it an Alpha release

### Version 0.7.0.0 - commit date 2023-10-16

- updated README.md
  - foreshadowing making a distinction between
    - objects "sharing" their data -> FP methods return copies
    - objects "contain" their data -> FP methods mutate object

### Version 0.6.9.0 - PyPI release date: 2023-10-09

- renamed core module to iterlib module
  - library just contained functions for manipulating iterators
  - TODO: use mergeIters as a guide for an iterator "zip" function
- class Stack better in alignment with:
  - Python lists
    - more natural for Stack to iterate backwards starting from head
    - removed Stack's __getitem__ method
    - both pop and push/append from end

### Version 0.2.2.2 - PyPI release date: 2023-09-04

- decided base package should have no dependencies other than
  - Python version (>=2.10 due to use of Python match statement)
  - Python standard libraries
- made pytest an optional [test] dependency
- added src/ as a top level directory as per
  - https://packaging.python.org/en/latest/tutorials/packaging-projects/
  - could not do the same for tests/ if end users are to have access

### Version 0.2.1.0 - PyPI release date: 2023-09-03

- first Version uploaded to PyPI
- https://pypi.org/project/grscheller.datastructures/
- Install from PyPI
  - $ pip install grscheller.datastructures==0.2.1.0
  - $ pip install grscheller.datastructures # for top level version
- Install from GitHub
  - $ pip install git+https://github.com/grscheller/datastructures@v0.2.1.0
- pytest made a dependency
  - useful & less confusing to developers and end users
    - good for systems I have not tested on
    - prevents another pytest from being picked up from shell $PATH
      - using a different python version
      - giving "package not found" errors
    - for CI/CD pipelines requiring unit testing

### Version 0.2.0.2 - github only release date: 2023-08-29

- First version able to be installed from GitHub with pip
- $ pip install git+https://github.com/grscheller/datastructures@v0.2.0.2

### Version 0.1.1.0 - commit date: 2023-08-27

- grscheller.datastructures moved to its own GitHub repo
- https://github.com/grscheller/datastructures
  - GitHub and PyPI user names just a happy coincidence

### Version 0.1.0.0 - initial version: 2023-08-27

- Package implementing data structures which do not throw exceptions
- Did not push to PyPI until version 0.2.1.0
- Initial Python grscheller.datastructures for 0.1.0.0 commit:
  - dqueue - implements a double sided queue class Dqueue
  - stack - implements a LIFO stack class Stack
