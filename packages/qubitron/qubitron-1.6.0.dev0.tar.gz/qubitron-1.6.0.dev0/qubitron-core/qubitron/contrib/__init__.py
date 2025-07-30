# Copyright 2018 The Qubitron Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Functionality that is not part of core supported Qubitron apis.

Any contributions not ready for full production can be put in a subdirectory in
this package.
"""

from qubitron.contrib import acquaintance
from qubitron.contrib import graph_device
from qubitron.contrib import quirk
from qubitron.contrib.qcircuit import circuit_to_latex_using_qcircuit as circuit_to_latex_using_qcircuit
from qubitron.contrib import json
from qubitron.contrib.circuitdag import CircuitDag as CircuitDag, Unique as Unique
