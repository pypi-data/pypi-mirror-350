# Developer Tools - Queues

Python package containing modules implementing queue-like data
structures. This project is part of the [Developer Tools for Python][4]
**dtools.** namespace project.

- **Repositories**
  - [dtools.queues][1] project on *PyPI*
  - [Source code][2] on *GitHub*
- **Detailed documentation**
  - [Detailed API documentation][3] on *GH-Pages*

## Overview

Classic queue data structures:

- *module* dtools.queues
  - *module* fifo: First-In-First-Out Queue - FIFOQueue
  - *module* lifo: Last-In-First-Out Queue - LIFOQueue
  - *module* de: Double-Ended Queue - DEQueue

These queues allow iterators to leisurely iterate over inaccessible
copies of their current state while the queues themselves are free to
safely mutate. They are designed to be reasonably "atomic" without
introducing inordinate complexity.

All are more restrictive then the underlying circular array data
structure used to implement them. Developers can focus on the queue's
use case instead of all the "bit fiddling" required to implement
behavior, perform memory management, and handle coding edge cases.
Sometimes the real power of a data structure comes not from what it
empowers you to do, but from what it prevents you from doing to
yourself.

[1]: https://pypi.org/project/dtools.queues/
[2]: https://github.com/grscheller/dtools-queues/
[3]: https://grscheller.github.io/dtools-namespace-projects/queues/
[4]: https://github.com/grscheller/dtools-namespace-projects/blob/main/README.md
