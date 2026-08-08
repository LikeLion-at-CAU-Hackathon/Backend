from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import *

@require_http_methods(["GET"])
def get_product(request, id):
    return Response({
        "message": "Backend Connected!"
    })