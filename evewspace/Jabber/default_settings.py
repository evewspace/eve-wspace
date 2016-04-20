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
import random
import string

defaults = [
        ("JABBER_FROM_JID", "announce@localhost"),
        ("JABBER_FROM_PASSWORD", ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(15))),
        ("JABBER_LOCAL_SPACE_CHAR", "_"),
        ("JABBER_LOCAL_DOMAIN", "localhost"),
        ("JABBER_LOCAL_ENABLED", "0"),
        ]

load_defaults = partial(load_defaults, defaults)
