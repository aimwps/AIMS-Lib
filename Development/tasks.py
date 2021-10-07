from django.shortcuts import render, get_object_or_404
from .models import Aim, Behaviour, StepTracker, StepTrackerLog, StepTrackerCustomFrequency
from Members.models import MemberProfile
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from datetime import datetime, timedelta
from django.db.models import Q
from dateutil.relativedelta import relativedelta
