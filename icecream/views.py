from django.shortcuts import render_to_response
from django.shortcuts import Http404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from icecream.models import Flavour

def flavours(request):
    flavours = Flavour.objects.all()
    return render_to_response('icecream/flavours.html', {'flavours': flavours})

def flavour_add(request):
    if request.method == 'POST':
        flavour = Flavour()
        flavour.name = request.POST['name']
        flavour.litres = request.POST['litres']
        flavour.sellprice = request.POST['sellprice']

        flavour.save()

        return HttpResponseRedirect(reverse('icecream.views.flavours')) # Redirect after POST

    return render_to_response('icecream/flavour-add.html', {}, context_instance=RequestContext(request))

def flavour_edit(request, id):
    raise Http404

def flavour_delete(request, id):
    raise Http404
