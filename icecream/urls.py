from django.conf.urls import patterns, url

urlpatterns = patterns('icecream.views',
    # Examples:
    # url(r'^$', 'cafe.views.home', name='home'),
    url(r'^flavour/$', 'flavours'),
    url(r'^flavour/add/$', 'flavour_add'),
    url(r'^flavour/(?P<id>\d+)/$', 'flavour_edit'),
    url(r'^flavour/(?P<id>\d+)/delete/$', 'flavour_delete'),
)
