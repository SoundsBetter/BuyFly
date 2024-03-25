from django.http import HttpRequest, HttpResponseBase
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponseBase:
    return render(request, "home.html")
