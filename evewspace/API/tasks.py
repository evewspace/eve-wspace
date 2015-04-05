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

from celery import task
from API.models import APIKey, MemberAPIKey
from django.core.cache import cache
from django.contrib.auth import get_user_model
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

User = get_user_model()

@task()
def update_char_data():
    #Get all users
    user_list = User.objects.all()
    for user in user_list:
        #Get all API keys of a user and validate them
        for key in user.api_keys.all():
            key.validate()
