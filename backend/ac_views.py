from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from . import forms
from .models import Waiter, Tenant, Manager, ACAdministrator, AC
from datetime import date
