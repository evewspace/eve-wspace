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
        ("API_ALLOW_CHARACTER_KEY", "0"),
        ("API_ALLOW_EXPIRING_KEY", "0"),
        ("SSO_ENABLED", "False"),
        ("SSO_SECRET_KEY", ""),
        ("SSO_CLIENT_ID", ""),
        ("SSO_BASE_URL", ""),
        ("SSO_SCOPE", "esi-location.read_location.v1 esi-location.read_ship_type.v1 characterLocationRead"),
        ("SSO_USER_AGENT", "EVE W-space Instance"),
        ("SSO_LOGIN_ENABLED", "False"),
        ("SSO_DEACTIVATE_ACCOUNTS", "False"),
        ("SSO_DEFAULT_GROUP", ""),
        ]

load_defaults = partial(load_defaults, defaults)
