# Copyright 2024-2025 Geoffrey R. Scheller
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

"""
### Developer Tools - splitends

Package implementing a singularly linked LIFO queue called a SplitEnd. These
data structures can safely share data nodes between themselves.

- *class* dtools.splitends.splitend.SplitEnd: Mutable stack (LIFO)
  - which allow for data sharing between different instances
  - each splitend sees itself as a singularly linked list
    - from the "end" of the hair to its "root"
  - multiple instances can form bush like data structures
    - like follicles of hair with split ends
- *class* dtools.splitends.splitend_node.SENode
  - data nodes for SplitEnd stacks

"""

__author__ = 'Geoffrey R. Scheller'
__copyright__ = 'Copyright (c) 2023-2025 Geoffrey R. Scheller'
__license__ = 'Apache License 2.0'
