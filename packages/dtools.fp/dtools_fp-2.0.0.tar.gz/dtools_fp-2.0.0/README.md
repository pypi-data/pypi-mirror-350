# Developer Tools - Pythonic functional programming

Functional programming tools which endeavor to be Pythonic. This project
is part of the [Developer Tools for Python][4] **dtools** namespace
project.

- **Repositories**
  - [dtools.fp][1] project on *PyPI*
  - [Source code][2] on *GitHub*
- Detailed documentation for dtools.fp
  - [Detailed API documentation][3] on *GH-Pages*

## Overview

- Benefits of FP
  - improved composability
  - avoid hard to refactor exception driven code paths
  - data sharing becomes trivial when immutability leveraged

The dtools.fp package consists of 4 modules.

______________________________________________________________________

### Functions as first class objects

  - dtools.fp.function
    - utilities to manipulate and partially apply functions

______________________________________________________________________

### Lazy function evaluation

- dtools.fp.lazy
  - lazy (non-strict) function evaluation

______________________________________________________________________

### Singletons

- dtools.fp.singletons
  - 3 singleton classes representing
    - a missing value (actually missing, not potentially missing)
    - a sentinel value
    - a failed calculation

______________________________________________________________________

### State monad implementation

- dtools.fp.state
  - pure FP handling of state (the state monad)

______________________________________________________________________

[1]: https://pypi.org/project/dtools.fp/
[2]: https://github.com/grscheller/dtools-fp/
[3]: https://grscheller.github.io/dtools-namespace-projects/fp/
[4]: https://github.com/grscheller/dtools-namespace-projects/blob/main/README.md
