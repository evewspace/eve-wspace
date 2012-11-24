from POS.models import *
from Map.models import System
from core.models import Type
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from datetime import datetime
import pytz
import eveapai
from API import utils as handler
