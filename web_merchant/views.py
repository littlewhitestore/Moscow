# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse 
from django.views import View 

class Home(View):
    
    def get(self, request):
        return render(request, 'home.html') 
