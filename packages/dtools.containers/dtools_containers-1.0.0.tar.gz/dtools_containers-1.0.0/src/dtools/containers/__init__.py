# Copyright 2023-2025 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""### Developer Tools - Container-like data structures

- *module* `dtools.containers`: Container-like data structures
  - *module* `box`: stateful container holding at most one object
  - *module* `functional_tuple`: directly inherited from the `tuple` builtin 
    - gives `tuple` FP interface
    - designed to be further inherited from
  - *module* `immutable_list`: 
    - hashable
      - hashability will be enforced at runtime
        - should also be enforced with typing tooling (not yet fully tested)
  - *module* `maybe`: implements the "maybe" (also called "optional") monad
    - class representing a possibly missing value
  - *module* `xor`: implements a left biased "either" monad
    - class representing either a "left" or "right" value, but not both
      - these values can be the same or different types
      - the "left" value is taken to be the "happy path"

"""

__author__ = 'Geoffrey R. Scheller'
__copyright__ = 'Copyright (c) 2023-2025 Geoffrey R. Scheller'
__license__ = 'Apache License 2.0'
