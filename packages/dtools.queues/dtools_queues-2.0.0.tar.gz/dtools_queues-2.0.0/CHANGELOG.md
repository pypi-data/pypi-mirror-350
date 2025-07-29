# CHANGELOG

- Strict 3 digit semantic versioning (adopted 2025-05-19)
  - MAJOR version for incompatible API changes
  - MINOR version for backward compatible added functionality
  - PATCH version for backward compatible bug fixes

## Releases and Important Milestones

### Adapting strict Semantic from this point on - date 2025-05-19

- [Semantic Versioning 2.0.0](https://semver.org/)
- see top of file
- previous versioning scheme used
  - first digit - major event, epoch, or paradigm shift
  - second digit - breaking API changes, major changes
  - third digit - bug fixes, API additions

### Version 1.0.0 - PyPI release date 2025-04-22

- Removed splitends module to its own repo
- docstring changes
- pyproject.toml standardization

### Version 0.27.0 - PyPI release date 2025-04-07

- first PyPI release as dtools.queues
  - split dtools.datastructures into
    - dtools.queues
    - dtools.tuples
- typing improvements

### Version 0.25.1 - PyPI release date 2025-01-16

- Fixed pdoc issues with new typing notation
  - updated docstrings
  - had to add TypeVars

### Version 0.25.0 - PyPI release date 2025-01-17

- First release under dtools.datastructures name

### Version 0.24.0 - PyPI release date 2024-11-18

- Changed flatMap to bind thru out project

### Version 0.22.1 - PyPI release date 2024-10-20

- removed docs from repo
- docs for all grscheller namespace projects maintained
  [here](https://grscheller.github.io/grscheller-pypi-namespace-docs/).

### Version 0.21.0 - PyPI release date 2024-08-20

- got back to a state maintainer is happy with
  - many dependencies needed updating first

### Version 0.20.5.1 - datastructures coming back together 2024-08-19

- works with all the current versions of fp and circular-array
- preparing for PyPI 0.21.0 release

### Version 0.20.2.0 - Going down a typing rabbit hole 2024-08-03

- updated to use grscheller.circular-array version 3.3.0 (3.2.3.0)
- updated to use grscheller.fp version 0.3.0 (0.2.3.0)
- removed grscheller.circular-array dependency from datastructures.SplitEnd
- still preparing for the 1.0.0 datastructures release
  - as I tighten up typing, I find I must do so for dependencies too
  - using `# type: ignore` is a band-aid, use `@overload` and `cast` instead
  - using `@overload` to "untype" optional parameters is the way to go
  - use `cast` only when you have knowledge beyond what the typechecker can know

### Version 0.19.0 - PyPI release date 2024-07-15

- continuing to prepare for PyPI release 1.0.0
- cleaned up docstrings for a 1.0.0 release
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

### Version 0.12.0 - PyPI Release date 2024-01-14

- Considerable future-proofing for first real Beta release

### Version 0.11.3.4 - Finally decided to make next PyPI release Beta

- Package structure mature and not subject to change beyond additions
- Will endeavor to keep top level & core module names the same
- API changes will be deprecated before removed

### Version 0.10.14.0 - commit date 2023-12-09

- Finished massive renaming & repackaging effort
  - to help with future growth
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

### Version 0.10.9 - PyPI release date 2023-11-21

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
  - Need to use this package in other projects to gain insight

### Version 0.8.6.0 - PyPI release date: 2023-11-05

- Finally got queue.py & stack.py inheritance sorted out
- LSP with Pyright working quite well
- Goals for next PyPI release:
  - combine methods
    - tail and tailOr
    - cons and consOr
    - head and headOr

### Version 0.8.3.0 - commit date 2023-11-02

- major API breaking change
  - Dqueue renamed DQueue
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

### Version 0.7.2.0 - commit date 2023-10-18

- Queue & Dqueue no longer return Maybe objects
  - Neither store None as a value
  - Now safe to return None for non-existent values
    - like popping or peaking from an empty queue or dqueue

### Version 0.7.0.0 - commit date 2023-10-16

- added Queue data structure representing a FIFO queue
- renamed two Dqueue methods
  - headR -> peakLastIn
  - headL -> peakNextOut
- went ahead and removed Stack head method
  - fair since I still labeling releases as alpha releases
  - the API is still a work in progress
- updated README.md
  - foreshadowing making a distinction between
    - objects "sharing" their data -> FP methods return copies
    - objects "contain" their data -> FP methods mutate object
  - added info on class Queue

### Version 0.6.9.0 - PyPI release date: 2023-10-09

- renamed core module to iterlib module
  - library just contained functions for manipulating iterators
  - TODO: use mergeIters as a guide for an iterator "zip" function
- class Stack better in alignment with:
  - Python lists
    - more natural for Stack to iterate backwards starting from head
    - removed Stack's __getitem__ method
    - both pop and push/append from end
  - Dqueue which wraps a Circle instance
    - also Dqueue does not have a __getitem__ method
  - Circle which implements a circular array with a Python List

### Version 0.6.8.6 - commit date: 2023-10-08

- 3 new methods for class Circle and Dqueue
  - mapSelf, flatMapSelf, mergeMapSelf
    - these correspond to map, flatMap, mergeMap
    - except they act on the class objects themselves, not new instances
- not worth the maintenance effort maintaining two version of Dqueue
  - one returning new instances
  - the other modifying the object in place

### Version 0.6.8.3 - commit date: 2023-10-06

- class Carray renamed to Circle
  - implements a circular array based on a Python List
  - resizes itself as needed
  - will handle None values being pushed and popped from it
  - implemented in the grscheller.datastructures.circle module
    - in the src/grscheller/datastructures/circle.py file
  - O(1) pushing/popping to/from either end
  - O(1) length determination
  - O(1) indexing for setting and getting values.
- Dqueue implemented with Circle class instead of List class directly
- Ensured that None is never pushed to Stack & Dqueue objects

### Version 0.6.3.2 - commit date: 2023-09-30

- Improved comments and type annotations
- Removed isEmpty method from Dqueue class
- Both Dqueue & Stack objects evaluate true when non-empty
- Beginning preparations for the next PyPI release
  - Want to make next PyPI release a Beta release
  - Need to improve test suite first

### Version 0.6.2.0 - commit date: 2023-09-25

- removed isEmpty method from Stack class

### Version 0.6.1.0 - commit date: 2023-09-25

- Maybe get() and getOrElse() API changes
- getting a better handle on type annotation
  - work-in-progress
  - erroneous LSP error messages greatly reduced

### Version 0.5.2.1 - PyPI release date: 2023-09-24

- data structures now support a much more FP style for Python
  - introduces the use of type annotations for this effort
  - much better test coverage

### Version 0.3.0.2 - PyPI release date: 2023-09-09

- updated class Dqueue
  - added __eq__ method
  - added equality tests to tests/test_dqueue.py
- improved docstrings

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

- First version to be installed from GitHub with pip
- $ pip install git+https://github.com/grscheller/datastructures@v0.2.0.2

### Version 0.2.0.0 - commit date: 2023-08-29

- BREAKING API CHANGE!!!
- Dqueue pushL & pushR methods now return references to self
  - These methods used to return the data being pushed
  - Now able to "." chain push methods together
- Updated tests - before making API changes
- First version to be "released" on GitHub

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
