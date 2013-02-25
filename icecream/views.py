from django.shortcuts import render_to_response
from django.shortcuts import Http404

from icecream.models import Flavour

def flavours(request):
    flavours = Flavour.objects.all()
    return render_to_response('icecream/flavours.html', {'flavours': flavours})

def flavour_add(request):
    return render_to_response('icecream/flavour-add.html')

def flavour_edit(request, id):
    raise Http404

def flavour_delete(request, id):
    raise Http404
