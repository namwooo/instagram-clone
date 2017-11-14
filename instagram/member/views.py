from typing import NamedTuple

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from config import settings
from .forms import SignUpForm, LoginForm

from django.contrib.auth import get_user_model, logout as django_logout, login as django_login

User = get_user_model()



