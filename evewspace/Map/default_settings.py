#   Eve W-Space
#   Copyright 2014 Andrew Austin and contributors
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from core.utils import load_defaults
from functools import partial

defaults = [
    ("MAP_PVP_THRESHOLD", "0"),
    ("MAP_NPC_THRESHOLD", "10"),
    ("MAP_SCAN_WARNING", "3"),
    ("MAP_INTEREST_TIME", "15"),
    ("MAP_ESCALATION_BURN", "3"),
    ("MAP_ADVANCED_LOGGING", "1"),
    ("MAP_ZEN_MODE", "0"),
    ("MAP_PILOT_LIST", "0"),
    ("MAP_DETAILS_COMBINED", "0"),
    ("MAP_RENDER_WH_TAGS", "1"),
    ("MAP_SCALING_FACTOR", "1"),
    ("MAP_HIGHLIGHT_ACTIVE", "1"),
    ("MAP_AUTO_REFRESH", "1"),
    ("MAP_KSPACE_MAPPING", "0"),
    ("MAP_SILENT_MAPPING", "0"),
    ("MAP_RENDER_COLLAPSED", "0"),
    ("MAP_AUTODELETE_SIGS", "1"),
    ("MAP_AUTODELETE_DAYS", "14"),
]

load_defaults = partial(load_defaults, defaults)
