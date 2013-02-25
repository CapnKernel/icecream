from django.shortcuts import Http404

from icecream.models import Flavour

def flavours(request):
    raise Http404

def flavour_add(request):
    raise Http404

def flavour_edit(request, id):
    raise Http404

def flavour_delete(request, id):
    raise Http404
