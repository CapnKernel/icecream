from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from icecream.models import Flavour
from icecream.forms import FlavourForm

def flavours(request):
    flavours = Flavour.objects.all()
    return render_to_response('icecream/flavours.html', {'flavours': flavours}, context_instance=RequestContext(request))

def flavour_add(request):
    if request.method == 'POST':
        form = FlavourForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "Flavour added.")

            return HttpResponseRedirect(reverse('icecream.views.flavours'))
            
        messages.error(request, "The data is not valid, so the new flavour was not added.")
    else:
        form = FlavourForm()

    return render_to_response('icecream/flavour-add.html', {'form': form}, context_instance=RequestContext(request))

def flavour_edit(request, id):
    flavour = get_object_or_404(Flavour, pk=id)
    if request.method == 'POST':
        form = FlavourForm(request.POST, instance=flavour)
        if form.is_valid():
            form.save()

            messages.success(request, "Flavour changed.")

            return HttpResponseRedirect(reverse('icecream.views.flavours'))

        messages.error(request, "The data is not valid, so the flavour was not updated.")
    else:
        form = FlavourForm(instance=flavour) # bound form, loaded with data from the db

    return render_to_response('icecream/flavour-edit.html', {'flavour': flavour, 'form': form}, context_instance=RequestContext(request))

def flavour_delete(request, id):
    # GET: Prompt for whether to delete a flavour
    # POST: Delete the address and redirect to flavours
    flavour = get_object_or_404(Flavour, pk=id)

    if request.method == 'POST':
        flavour.delete()

        messages.success(request, "Flavour deleted.")

        return HttpResponseRedirect(reverse('icecream.views.flavours'))

    return render_to_response('icecream/flavour-delete.html', {'flavour': flavour}, context_instance=RequestContext(request))
