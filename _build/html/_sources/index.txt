.. icecream documentation master file, created by
   sphinx-quickstart on Sun Feb 24 14:31:29 2013.

Welcome to the Django icecream tutorial!
========================================

Getting started
===============

This tutorial is for those who want to learn more about Django.  If you've just finished the official Django tutorial and want to consolidate what you've learned, plus see a few more things, read away.

By using the example of an app to manage the inventory of icecream flavours in a cafe, this tutorial shows an example of how to write 'CRUD' apps: Apps that can create, read, update and delete objects.

One presentation difference is that code changes in this tutorial are presented in the form of diffs.  This shows you exactly the changes to make to the code: What lines should be removed, and what lines should be added.

If you're using Linux, or you have Cygwin installed, you can start a shell and run this command:

.. code-block:: bash

    patch -p0

Then copy-and-paste the diff into the terminal, and press Ctrl-D twice.  The patch program will automatically apply this change.

.. toctree::
   :maxdepth: 2

Tutorial
========

Creating the project
--------------------

By now you should be familiar with how to create a Django project.  Let's create a project called "cafe":

.. code-block:: bash

    django-admin.py startproject cafe

As with the original tutorial, you should be able to start the Django development server and verify that the project has been created correctly:

.. code-block:: bash

    cd cafe
    python manage.py runserver
    Validating models...

    0 errors found
    July 4, 1776 - 15:50:53
    Django version 1.4, using settings 'mysite.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Visiting http://127.0.0.1:8000/ should then display the pastel-blue Django welcome page.

Now that you've verified the project and server are working, go ahead and set up a local sqlite database:

.. code-block:: diff

    diff --git cafe-old/settings.py cafe/settings.py
    --- cafe-old/settings.py
    +++ cafe/settings.py
    @@ -11,8 +11,8 @@ MANAGERS = ADMINS
     
     DATABASES = {
         'default': {
    -        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
    -        'NAME': '',                      # Or path to database file if using sqlite3.
    +        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
    +        'NAME': 'cafe.sqlite',                      # Or path to database file if using sqlite3.
             'USER': '',                      # Not used with sqlite3.
             'PASSWORD': '',                  # Not used with sqlite3.
             'HOST': '',                      # Set to empty string for 127.0.0.1. Not used with sqlite3.

And create this initial database:

.. code-block:: bash

    python manage.py syncdb

Answer the questions, creating yourself an 
Admin setup
-----------

The admin functionality can be turned on and used even without defining any app models.  Make these changes:

.. code-block:: diff

    diff -u cafe-old/settings.py cafe/settings.py
    --- cafe-old/settings.py
    +++ cafe/settings.py
    @@ -116,7 +116,7 @@ INSTALLED_APPS = (
         'django.contrib.messages',
         'django.contrib.staticfiles',
         # Uncomment the next line to enable the admin:
    -    # 'django.contrib.admin',
    +    'django.contrib.admin',
         # Uncomment the next line to enable admin documentation:
         # 'django.contrib.admindocs',
     )
    diff -u cafe-old/urls.py cafe/urls.py
    --- cafe-old/urls.py
    +++ cafe/urls.py
    @@ -1,8 +1,8 @@
     from django.conf.urls import patterns, include, url
     
     # Uncomment the next two lines to enable the admin:
    -# from django.contrib import admin
    -# admin.autodiscover()
    +from django.contrib import admin
    +admin.autodiscover()
     
     urlpatterns = patterns('',
         # Examples:
    @@ -13,5 +13,5 @@ urlpatterns = patterns('',
         # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
     
         # Uncomment the next line to enable the admin:
    -    # url(r'^admin/', include(admin.site.urls)),
    +    url(r'^admin/', include(admin.site.urls)),
     )

Then try the admin interface here: http://127.0.0.1:8000/admin/

Making icecream
---------------

Next, create an app called "icecream".  This app could be used to track different flavours of icecream in a cafe, how much the icecream is sold for, and how much of each flavour is in stock.

.. code-block:: bash

    python manage.py startapp icecream

After this, create a model to represent each flavour:

.. code-block:: diff

    diff -u icecream-old/models.py icecream/models.py
    --- icecream-old/models.py
    +++ icecream/models.py
    @@ -1,3 +1,11 @@
     from django.db import models
     
     # Create your models here.
    +class Flavour(models.Model):
    +    name = models.CharField(max_length=40)
    +    litres = models.FloatField() # How many litres we have in the store
    +    sellprice = models.DecimalField(decimal_places=2, max_digits=5) # How much it costs per litre
    +
    +    def __unicode__(self):
    +        return self.name
    +

... and add the app to INSTALLED_APPS in the cafe/settings.py file:

.. code-block:: diff

    diff -u cafe-old/settings.py cafe/settings.py
    index 96061a2..079539d 100644
    --- cafe-old/settings.py
    +++ cafe/settings.py
    @@ -119,6 +119,7 @@ INSTALLED_APPS = (
         'django.contrib.admin',
         # Uncomment the next line to enable admin documentation:
         # 'django.contrib.admindocs',
    +    'icecream',
     )
     
     # A sample logging configuration. The only tangible logging

Playing with flavours
---------------------

Let's have a look at the SQL statements to generate this model.  Run this:

.. code-block:: bash

    python manage.py sqlall icecream

You should see this:

.. code-block:: sql

    BEGIN;
    CREATE TABLE "icecream_flavour" (
        "id" integer NOT NULL PRIMARY KEY,
        "name" varchar(40) NOT NULL,
        "litres" real NOT NULL,
        "sellprice" decimal NOT NULL
    )
    ;
    COMMIT;

Now create the table, and enter the database shell:

.. code-block:: bash

    python manage.py syncdb
    python manage.py dbshell
    
You can now look at the schema, and enter a test flavour:

.. code-block:: sql

    .tables
    .schema icecream_flavour
    insert into icecream_flavour values(1, "Chocolate", "70", "55");
    .exit

Cool!  Now we can play with the model instances from within Django.  Run ``python manage.py shell``::

    >>> from icecream.models import Flavour
    >>> print Flavour.objects.all()
    [<Flavour: Chocolate>]
    >>> print Flavour.objects.all()[0]
    Chocolate
    >>> choc = Flavour.objects.get(id=1)
    >>> print choc
    Chocolate
    >>> print choc.litres
    70.0
    >>> choc.litres = 80
    >>> choc.save()
    >>> print choc.litres
    80
    >>> lemon = Flavour(name="Lemon", litres=40, sellprice=40)
    >>> lemon.save()
    >>> print Flavour.objects.all().count()
    2
    >>> print Flavour.objects.all()
    [<Flavour: Chocolate>, <Flavour: Lemon>]
    >>> exit()

Flavours in admin
-----------------

We can show the Flavour model in the admin interface:

.. code-block:: diff

    diff -u icecream-old/admin.py icecream/admin.py
    --- /dev/null
    +++ icecream/admin.py
    @@ -0,0 +1,4 @@
    +from django.contrib import admin
    +from icecream.models import Flavour
    +
    +admin.site.register(Flavour)

Try viewing the admin interface now.  You should see the Flavour model in the Icecream app.

Click on ``Flavours``.  Hmm, wouldn't it be better if we could display something more than just the flavour name?  Let's add some fields:

.. code-block:: diff

    diff -u icecream-old/admin.py icecream/admin.py
    --- icecream-old/admin.py
    +++ icecream/admin.py
    @@ -1,4 +1,9 @@
     from django.contrib import admin
     from icecream.models import Flavour
     
    -admin.site.register(Flavour)
    +# Override fields and ordering of fields
    +class FlavourAdmin(admin.ModelAdmin):
    +    fields = ['name', 'litres', 'sellprice']
    +    list_display = ('name', 'litres', 'sellprice')
    +
    +admin.site.register(Flavour, FlavourAdmin)

Try the admin interface now.  Enjoy the extra fields!

CRUD is Create, Read, Update and Delete
---------------------------------------

The basic operations on data are to create something, to be able to view it, to edit it, and to delete it.  Django's ORM model system can do these just fine, but the tutorial is missing some details about Django's way of doing this in web apps.  Our demo is going to show how all these operations can be done.

One note about GET and POST.  As well as a different way to pass data from the web client to the server, it's a common pattern in Django to be able to make both GET and POST requests to the same URL, but the meaning of these requests is somewhat different:

 - GET requests are for requests which don't change anything.  Within the view for a CRUD-type operation, a GET request is often used to send the data the operation relates to, back to the web browser for the user to review.  It shouldn't matter how many times a request is made.
 
 - POST requests are for requests which change something.  For views of CRUD operations, a POST request is often used to actually *do* the CRUD operation.  (If there are multiple actions that could be done with a view, often some sort of "action" parameter is passed back to the view, so the view knows which action to take).
 
   As mentioned in the official tutorial, standard practice is to redirect a successful POST request to a GET.  That can prevent lots of problems with browsers trying to replay old operations when pages are refreshed.

URL and view design
-------------------

Often the first step when coding a Django app is to plan our URLs and views.  For each of the CRUD operations on our Flavour models, here are some URLs and view names:

=========== ========================== =================================
Operation   URL                        view
----------- -------------------------- ---------------------------------
Read (list) ``^flavour/$``             ``icecream.views.flavours``
Create      ``^flavour/add/$``         ``icecream.views.flavour_add``
Read/update ``^flavour/<id>/$``        ``icecream.views.flavour_edit``
Delete      ``^flavour/<id>/delete/$`` ``icecream.views.flavour_delete``
=========== ========================== =================================

Note that we're offering two kinds of read: A list of all flavours, and a page for each flavour which shows flavour details, as well as lets us edit those details.

For each of these operations on our flavours, let's add a URL, and a stubbed out view:

.. code-block:: diff

    diff -u cafe-old/urls.py cafe/urls.py
    --- cafe-old/urls.py
    +++ cafe/urls.py
    @@ -7,7 +7,7 @@ admin.autodiscover()
     urlpatterns = patterns('',
         # Examples:
         # url(r'^$', 'cafe.views.home', name='home'),
    -    # url(r'^cafe/', include('cafe.foo.urls')),
    +    url(r'^icecream/', include('icecream.urls')),
     
         # Uncomment the admin/doc line below to enable admin documentation:
         # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    diff -u icecream-old/urls.py icecream/urls.py
    --- /dev/null
    +++ icecream/urls.py
    @@ -0,0 +1,10 @@
    +from django.conf.urls import patterns, url
    +
    +urlpatterns = patterns('icecream.views',
    +    # Examples:
    +    # url(r'^$', 'cafe.views.home', name='home'),
    +    url(r'^flavour/$', 'flavours'),
    +    url(r'^flavour/add/$', 'flavour_add'),
    +    url(r'^flavour/(?P<id>\d+)/$', 'flavour_edit'),
    +    url(r'^flavour/(?P<id>\d+)/delete/$', 'flavour_delete'),
    +)
    diff -u icecream-old/views.py icecream/views.py
    --- icecream-old/views.py
    +++ icecream/views.py
    @@ -1 +1,15 @@
    -# Create your views here.
    +from django.shortcuts import Http404
    +
    +from icecream.models import Flavour
    +
    +def flavours(request):
    +    raise Http404
    +
    +def flavour_add(request):
    +    raise Http404
    +
    +def flavour_edit(request, id):
    +    raise Http404
    +
    +def flavour_delete(request, id):
    +    raise Http404

When accessed, each view will throw an Http404 exception.  Note that this looks different to the HTTP 404 error when we browse to a URL that's not listed in our urlconf.

Here's a list of URLs to try.  Do they do what you expect?

 - http://127.0.0.1:8000/icecream/
 - http://127.0.0.1:8000/icecream/taste/
 - http://127.0.0.1:8000/icecream/flavour/
 - http://127.0.0.1:8000/icecream/flavour/choc/
 - http://127.0.0.1:8000/icecream/flavour/1/
 - http://127.0.0.1:8000/icecream/flavour/add/
 - http://127.0.0.1:8000/icecream/flavour/1/delete/

Show a list of flavours
-----------------------

Let's add some view code to show the list of flavours:

.. code-block:: diff

    diff -u icecream-old/views.py icecream/views.py
    --- icecream-old/views.py
    +++ icecream/views.py
    @@ -1,9 +1,11 @@
    +from django.shortcuts import render_to_response
     from django.shortcuts import Http404
     
     from icecream.models import Flavour
     
     def flavours(request):
    -    raise Http404
    +    flavours = Flavour.objects.all()
    +    return render_to_response('icecream/flavours.html', {'flavours': flavours})
     
     def flavour_add(request):
         raise Http404

Let's give this a spin at http://127.0.0.1:8000/icecream/flavour/:

Oh no, there's no template!  Let's add one:

.. code-block:: diff

    diff -u cafe-old/settings.py cafe/settings.py
    --- cafe-old/settings.py
    +++ cafe/settings.py
    @@ -106,6 +106,7 @@ TEMPLATE_DIRS = (
         # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
         # Always use forward slashes, even on Windows.
         # Don't forget to use absolute paths, not relative paths.
    +    'templates',
     )
     
     INSTALLED_APPS = (
    diff -u templates-old/icecream/flavours.html templates/icecream/flavours.html
    --- /dev/null
    +++ templates/icecream/flavours.html
    @@ -0,0 +1,5 @@
    +<html>
    +<body>
    +  <p>{{ flavours }}</p>
    +</body>
    +</html>

Now http://127.0.0.1:8000/icecream/flavour/ works.  Spend a moment to view the HTML source in your browser.

.. admonition:: Do we really need an absolute path?

    Note that the ``settings.py`` file says "Don't forget to use absolute paths, not relative paths".  I've asked in the #django IRC channel, and it seems the only reason for using absolute paths is to guard against Django being run with an improperly set current directory.  However in general, relative paths like ``templates`` work just fine, and helps out a lot when you have multiple copies of your project, such as a development copy and a deployment copy.

Template Inheritance
--------------------

Let's break up this template into two parts, a base part (in ``templates/base.html``) for things that all our web pages will share, and a part that's specific to this view (``templates/icecream/flavours.html``):

.. code-block:: diff

    diff -u templates-old/base.html templates/base.html
    --- /dev/null
    +++ templates/base.html
    @@ -0,0 +1,14 @@
    +<!DOCTYPE HTML PUBLIC "-//W3C/DTD HTML 4.01//EN">
    +<html lang="en">
    +  <head>
    +    <title>{% block title %}icecream.com: Nirvana for icecream lovers{% endblock %}</title>
    +  </head>
    +  <body>
    +    <h1>{% block header %}Nirvana for icecream lovers{% endblock %}</h1>
    +    {% block content %}{% endblock %}
    +    {% block footer %}
    +    <hr>
    +    <p>Don't you just love icecream?</p>
    +    {% endblock %}
    +  </body>
    +</html>
    diff -u templates-old/icecream/flavours.html templates/icecream/flavours.html
    --- templates-old/icecream/flavours.html
    +++ templates/icecream/flavours.html
    @@ -1,5 +1,10 @@
    -<html>
    -<body>
    -  <p>{{ flavours }}</p>
    -</body>
    -</html>
    +{% extends "base.html" %}
    +
    +{% block header %}All the flavours{% endblock %}
    +
    +{% block content %}
    +<p>A list of flavours:</p>
    +
    +<p>{{ flavours }}</p>
    +
    +{% endblock %}

Notice how ``base.html`` has ``title``, ``header``, ``content`` and ``footer`` blocks, and that ``icecream/flavours.html`` overrides the values of the ``title`` and ``header`` blocks, provides a body to fill in the empty ``content`` block, but doesn't override the ``footer`` block.

Fields in templates
-------------------

At the moment our flavours page shows just flavour names.  It does this because the ``__unicode__`` helper method in the Flavours model returns the flavour name.  What about if we want to show more of the model in our template?

.. code-block:: diff

    diff -u templates-old/icecream/flavours.html templates/icecream/flavours.html
    --- templates-old/icecream/flavours.html
    +++ templates/icecream/flavours.html
    @@ -5,6 +5,10 @@
     {% block content %}
     <p>A list of flavours:</p>
     
    -<p>{{ flavours }}</p>
    +<ul>
    +  {% for flavour in flavours %}
    +  <li>{{ flavour.id }}: {{ flavour.name }}, {{ flavour.litres }}, {{ flavour.sellprice }}</li>
    +  {% endfor %}
    +</ul>
     
     {% endblock %}

In addition to displaying the values of the model fields, we also have a for loop which iterates over the flavours, displaying them one line at a time in a list.

Conditionals in templates
-------------------------

The code in the previous section works fine except in the case where there are no flavours.  If that were to happen, we should tell our user what's going on!

.. code-block:: diff

    diff -u templates-old/icecream/flavours.html templates/icecream/flavours.html
    --- templates-old/icecream/flavours.html
    +++ templates/icecream/flavours.html
    @@ -5,10 +5,14 @@
     {% block content %}
     <p>A list of flavours:</p>
     
    -<ul>
    -  {% for flavour in flavours %}
    -  <li>{{ flavour.id }}: {{ flavour.name }}, {{ flavour.litres }}, {{ flavour.sellprice }}</li>
    -  {% endfor %}
    -</ul>
    +{% if flavours %}
    +  <ul>
    +    {% for flavour in flavours %}
    +    <li>{{ flavour.id }}: {{ flavour.name }}, {{ flavour.litres }}, {{ flavour.sellprice }}</li>
    +    {% endfor %}
    +  </ul>
    +{% else %}
    +  <p>Quick, better add some flavours before customers arrive!</p>
    +{% endif %}
     
     {% endblock %}

If there are no flavours, we now tell our user what's going on.

Adding an 'Add' link
--------------------

In the case where there are no flavours (or more are needed), how can the user add them?  One way is by using the admin interface.  The other way is to improve our app to do it.

Let's give them an "Add" link:

.. code-block:: diff

    diff -u templates-old/icecream/flavours.html templates/icecream/flavours.html
    --- templates-old/icecream/flavours.html
    +++ templates/icecream/flavours.html
    @@ -15,4 +15,6 @@
       <p>Quick, better add some flavours before customers arrive!</p>
     {% endif %}
     
    +<p><a href="http://localhost:8000/icecream/flavour/add/">Add</a> a new flavour.</p>
    +
     {% endblock %}

You can click on the 'Add' link, but you'll get a 404 error message, because that's all our ``flavour_add`` view knows what to do.

This is the first step to adding the "create" part of CRUD.

Using the ``url`` tag
---------------------

The problem with the previous change is that it's hardwired to a particular address.  If we were to change the urlconf to have flavour addition on a different URL, or we deployed this app on another port or machine, then this link would stop working.  In order to prevent this, we can use the ``url`` template tag to generate the URL from the name of the view.  (If we had named the url pattern, we could also use this name).

.. code-block:: diff

    diff -u templates-old/icecream/flavours.html templates/icecream/flavours.html
    --- templates-old/icecream/flavours.html
    +++ templates/icecream/flavours.html
    @@ -1,4 +1,5 @@
     {% extends "base.html" %}
    +{% load url from future %}
     
     {% block header %}All the flavours{% endblock %}
     
    @@ -15,6 +16,6 @@
       <p>Quick, better add some flavours before customers arrive!</p>
     {% endif %}
     
    -<p><a href="http://localhost:8000/icecream/flavour/add/">Add</a> a new flavour.</p>
    +<p><a href="{% url 'icecream.views.flavour_add' %}">Add</a> a new flavour.</p>
     
     {% endblock %}

Adding an "Add" form and view
-----------------------------

I
Now that our flavour adding link is in place, let's work on the view to handle adding a flavour, and the template to display a form to accept the flavour details:

.. code-block:: diff

    diff -u icecream-old/views.py icecream/views.py
    --- icecream-old/views.py
    +++ icecream/views.py
    @@ -8,7 +8,7 @@ def flavours(request):
         return render_to_response('icecream/flavours.html', {'flavours': flavours})
     
     def flavour_add(request):
    -    raise Http404
    +    return render_to_response('icecream/flavour-add.html')
     
     def flavour_edit(request, id):
         raise Http404
    diff -u templates-old/icecream/flavour-add.html templates/icecream/flavour-add.html
    --- /dev/null
    +++ templates/icecream/flavour-add.html
    @@ -0,0 +1,14 @@
    +{% extends "base.html" %}
    +{% block header %}All the flavours - Add a flavour{% endblock %}
    +{% block content %}
    +<p>Add a flavour:</p>
    +
    +<form method="POST">
    +  <p>Name: <input type="text" name="name" value="" /></p>
    +  <p>Litres: <input type="text" name="litres" value="" /></p>
    +  <p>Selling price: <input type="text" name="sellprice" value="" /></p>
    +  <p><input type="submit" value="Add" /></p>
    +</form>
    +
    +<p><a href="..">Back</a></p>
    +{% endblock %}

Clicking on http://127.0.0.1:8000/icecream/flavour/add no longer gives a 404.  A nice form comes up, and we can enter new flavour details, click on "Add" and... *uh-oh*, a warning that the verification done as part of CSRF attack prevention has failed.

CSRF and adding flavours
------------------------

Django can help prevent against CSRF attacks, but it needs our help.  We need to add ``{{ csrf_token }}`` to the body of the form.  This is a variable with a magic value that will be sent back to the server when we submit the form.  We also need to convert our ``request`` argument into a ``RequestContext``, and pass this to ``render_to_response()`` as the ``context_instance`` kwarg.

This change also adds code to create a new model instance from the form data, and save it to the database.

.. code-block:: diff

    diff -u templates-old/icecream/flavour-add.html templates/icecream/flavour-add.html
    --- templates-old/icecream/flavour-add.html
    +++ templates/icecream/flavour-add.html
    @@ -4,6 +4,7 @@
     <p>Add a flavour:</p>
     
     <form method="POST">
    +  {% csrf_token %}
       <p>Name: <input type="text" name="name" value="" /></p>
       <p>Litres: <input type="text" name="litres" value="" /></p>
       <p>Selling price: <input type="text" name="sellprice" value="" /></p>
    diff -u icecream-old/views.py icecream/views.py
    --- icecream-old/views.py
    +++ icecream/views.py
    @@ -1,5 +1,8 @@
     from django.shortcuts import render_to_response
     from django.shortcuts import Http404
    +from django.template import RequestContext
    +from django.http import HttpResponseRedirect
    +from django.core.urlresolvers import reverse
     
     from icecream.models import Flavour
     
    @@ -8,7 +11,17 @@ def flavours(request):
         return render_to_response('icecream/flavours.html', {'flavours': flavours})
     
     def flavour_add(request):
    -    return render_to_response('icecream/flavour-add.html')
    +    if request.method == 'POST':
    +        flavour = Flavour()
    +        flavour.name = request.POST['name']
    +        flavour.litres = request.POST['litres']
    +        flavour.sellprice = request.POST['sellprice']
    +
    +        flavour.save()
    +
    +        return HttpResponseRedirect(reverse('icecream.views.flavours')) # Redirect after POST
    +
    +    return render_to_response('icecream/flavour-add.html', {}, context_instance=RequestContext(request))
     
     def flavour_edit(request, id):
         raise Http404

If this view is called as the result of a GET request, we render and return the flavour form.  However if this view is called as the result of a POST form, we create a new ``Flavour`` instance, set the field values from the POST data, then save it to the database.  Finally, we redirect the user back to the main flavours page.  Similar to the ``url`` template tag, we use the ``reverse`` function to avoid hard-coding a URL into the redirection.

Does adding flavours work now?  And what about if you enter invalid data, such as "xyz" for litres?  At present, our code doesn't do any field validation.  We'll add that later.

Adding delete
-------------

The next CRUD operation to look at is delete.  In some ways this is similar to adding: We're using both GET and POST requests, with the GET request displaying a confirmation message, and the POST request triggering flavour deletion:

.. code-block:: diff

    diff -u icecream-old/views.py icecream/views.py
    --- icecream-old/views.py
    +++ icecream/views.py
    @@ -1,4 +1,4 @@
    -from django.shortcuts import render_to_response
    +from django.shortcuts import render_to_response, get_object_or_404
     from django.shortcuts import Http404
     from django.template import RequestContext
     from django.http import HttpResponseRedirect
    @@ -27,4 +27,13 @@ def flavour_edit(request, id):
         raise Http404
     
     def flavour_delete(request, id):
    -    raise Http404
    +    # GET: Prompt for whether to delete a flavour
    +    # POST: Delete the address and redirect to flavours
    +    flavour = get_object_or_404(Flavour, pk=id)
    +
    +    if request.method == 'POST':
    +        flavour.delete()
    +
    +        return HttpResponseRedirect(reverse('icecream.views.flavours'))
    +
    +    return render_to_response('icecream/flavour-delete.html', {'flavour': flavour}, context_instance=RequestContext(request))
    diff -u templates-old/icecream/flavour-delete.html templates/icecream/flavour-delete.html
    --- /dev/null
    +++ templates/icecream/flavour-delete.html
    @@ -0,0 +1,17 @@
    +{% extends "base.html" %}
    +{% block header %}All the flavours - Delete a flavour{% endblock %}
    +{% block content %}
    +<p>Delete a flavour:</p>
    +
    +<p>{{ flavour }}:</p>
    +
    +<p> Really delete?</p>
    +
    +<form method="POST">
    +  {% csrf_token %}
    +  <input type="submit" value="Delete" />
    +</form>
    +
    +<p><a href="..">Back</a></p>
    +{% endblock %}
    +

This time however, the operation uses the ``get_object_or_404()`` helper function to find the model instance to delete (for POST requests), and to send to the form (for GET requests).

.. admonition:: Primary key names

    Relational database tables usually have a primary key column.  It often contains an integer which uniquely identifies the rows in the table.  If your model definition doesn't specify a primary key, a primary key called ``id`` will be created for you.  So in general, primary keys will be called ``id``.  When using ``get_object_or_404()``, it's tempting to look up the model instance using ``id``, however we can't always guarantee that ``id`` exists.  For this reason, we use ``pk``, for "primary key".  Django will map ``pk`` onto the primary key field for the model.

At the moment, we don't have a way of clicking to the delete view.  We'll add that next.  For the moment, you can get the page by entering the URL by hand, for example, http://127.0.0.1/icecream/flavours/1/delete

Try it out.  Does it work?

Editing flavours
----------------

Now onto the final CRUD operation: updating.  (Since we've now got code for all four of our views, we can remove the Http404 exception).

.. code-block:: diff

    diff -u icecream-old/views.py icecream/views.py
    --- icecream-old/views.py
    +++ icecream/views.py
    @@ -1,5 +1,4 @@
     from django.shortcuts import render_to_response, get_object_or_404
    -from django.shortcuts import Http404
     from django.template import RequestContext
     from django.http import HttpResponseRedirect
     from django.core.urlresolvers import reverse
    @@ -24,7 +23,16 @@ def flavour_add(request):
         return render_to_response('icecream/flavour-add.html', {}, context_instance=RequestContext(request))
     
     def flavour_edit(request, id):
    -    raise Http404
    +    flavour = get_object_or_404(Flavour, pk=id)
    +    if request.method == 'POST':
    +        flavour.name = request.POST['name']
    +        flavour.litres = request.POST['litres']
    +        flavour.sellprice = request.POST['sellprice']
    +        flavour.save()
    +
    +        return HttpResponseRedirect(reverse('icecream.views.flavours'))
    +
    +    return render_to_response('icecream/flavour-edit.html', {'flavour': flavour}, context_instance=RequestContext(request))
     
     def flavour_delete(request, id):
         # GET: Prompt for whether to delete a flavour
    diff -u templates-old/icecream/flavour-edit.html templates/icecream/flavour-edit.html
    --- /dev/null
    +++ templates/icecream/flavour-edit.html
    @@ -0,0 +1,19 @@
    +{% extends "base.html" %}
    +{% load url from future %}
    +{% block header %}All the flavours - Edit a flavour{% endblock %}
    +{% block content %}
    +<p>Edit a flavour:</p>
    +
    +<form method="POST">
    +  {% csrf_token %}
    +  <p>Name: <input type="text" name="name" value="{{ flavour.name }}" /></p>
    +  <p>Litres: <input type="text" name="litres" value="{{ flavour.litres }}" /></p>
    +  <p>Selling price: <input type="text" name="sellprice" value="{{ flavour.sellprice }}" /></p>
    +  <p><input type="submit" value="Update" /></p>
    +</form>
    +
    +<p><a href="{% url 'icecream.views.flavour_delete' flavour.id %}">Delete</a></p>
    +
    +<p><a href="..">Back</a></p>
    +{% endblock %}
    +
    diff -u templates-old/icecream/flavours.html templates/icecream/flavours.html
    --- templates-old/icecream/flavours.html
    +++ templates/icecream/flavours.html
    @@ -9,7 +9,7 @@
     {% if flavours %}
       <ul>
         {% for flavour in flavours %}
    -    <li>{{ flavour.id }}: {{ flavour.name }}, {{ flavour.litres }}, {{ flavour.sellprice }}</li>
    +    <li><a href="{% url 'icecream.views.flavour_edit' flavour.id %}">{{ flavour.name }}</a>: {{ flavour.litres }}, {{ flavour.sellprice }}</li>
         {% endfor %}
       </ul>
     {% else %}

You should now be able to modify and save the details of each flavour.

This code is somewhat similar to adding and deleting flavours: For a GET request, we fetch the right model instance, and send it to the template for populating the form.  For a POST request, we fetch the right model instance, take the values from the ``request.POST`` dictionary, and plug them into the instance.  Finally we save the model instance, and redirect back to the main flavours page.

Using Django's forms
--------------------

It's a bit tedious typing the details of a model into every form.  Let's upgrade the code to use Django's ``ModelForm`` form support:

.. code-block:: diff

    diff -u icecream-old/forms.py icecream/forms.py
    --- /dev/null
    +++ icecream/forms.py
    @@ -0,0 +1,6 @@
    +from django.forms import ModelForm
    +from icecream.models import Flavour
    +
    +class FlavourForm(ModelForm):
    +    class Meta:
    +        model = Flavour
    diff -u icecream-old/views.py icecream/views.py
    --- icecream-old/views.py
    +++ icecream/views.py
    @@ -4,6 +4,7 @@ from django.http import HttpResponseRedirect
     from django.core.urlresolvers import reverse
     
     from icecream.models import Flavour
    +from icecream.forms import FlavourForm
     
     def flavours(request):
         flavours = Flavour.objects.all()
    @@ -11,28 +12,28 @@ def flavours(request):
     
     def flavour_add(request):
         if request.method == 'POST':
    -        flavour = Flavour()
    -        flavour.name = request.POST['name']
    -        flavour.litres = request.POST['litres']
    -        flavour.sellprice = request.POST['sellprice']
    +        form = FlavourForm(request.POST)
    +        if form.is_valid():
    +            form.save()
     
    -        flavour.save()
    +            return HttpResponseRedirect(reverse('icecream.views.flavours'))
    +    else:
    +        form = FlavourForm()
     
    -        return HttpResponseRedirect(reverse('icecream.views.flavours')) # Redirect after POST
    -
    -    return render_to_response('icecream/flavour-add.html', {}, context_instance=RequestContext(request))
    +    return render_to_response('icecream/flavour-add.html', {'form': form}, context_instance=RequestContext(request))
     
     def flavour_edit(request, id):
         flavour = get_object_or_404(Flavour, pk=id)
         if request.method == 'POST':
    -        flavour.name = request.POST['name']
    -        flavour.litres = request.POST['litres']
    -        flavour.sellprice = request.POST['sellprice']
    -        flavour.save()
    +        form = FlavourForm(request.POST, instance=flavour)
    +        if form.is_valid():
    +            form.save()
     
    -        return HttpResponseRedirect(reverse('icecream.views.flavours'))
    +            return HttpResponseRedirect(reverse('icecream.views.flavours'))
    +    else:
    +        form = FlavourForm(instance=flavour) # bound form, loaded with data from the db
     
    -    return render_to_response('icecream/flavour-edit.html', {'flavour': flavour}, context_instance=RequestContext(request))
    +    return render_to_response('icecream/flavour-edit.html', {'flavour': flavour, 'form': form}, context_instance=RequestContext(request))
     
     def flavour_delete(request, id):
         # GET: Prompt for whether to delete a flavour
    diff -u templates-old/icecream/flavour-add.html templates/icecream/flavour-add.html
    --- templates-old/icecream/flavour-add.html
    +++ templates/icecream/flavour-add.html
    @@ -5,9 +5,7 @@
     
     <form method="POST">
       {% csrf_token %}
    -  <p>Name: <input type="text" name="name" value="" /></p>
    -  <p>Litres: <input type="text" name="litres" value="" /></p>
    -  <p>Selling price: <input type="text" name="sellprice" value="" /></p>
    +  {{ form.as_p }}
       <p><input type="submit" value="Add" /></p>
     </form>
     
    diff -u templates-old/icecream/flavour-edit.html templates/icecream/flavour-edit.html
    --- templates-old/icecream/flavour-edit.html
    +++ templates/icecream/flavour-edit.html
    @@ -6,9 +6,7 @@
     
     <form method="POST">
       {% csrf_token %}
    -  <p>Name: <input type="text" name="name" value="{{ flavour.name }}" /></p>
    -  <p>Litres: <input type="text" name="litres" value="{{ flavour.litres }}" /></p>
    -  <p>Selling price: <input type="text" name="sellprice" value="{{ flavour.sellprice }}" /></p>
    +  {{ form.as_p }}
       <p><input type="submit" value="Update" /></p>
     </form>
     
A ``ModelForm`` is a subclass of Form that automates many aspects of forms:

 - The form fields are auto-pulled from the model.
 
 - The form fields can be populated by a model instance.
 
 - A model instance can be updated from form fields.
 
 - Data validation is done against the types of fields in the model.
 
Like the ``Form`` class, the form can be rendered in the template using ``{{ form.as_p }}``.

How does the ModelForm know which Model to use?  In ``forms.py`` we define FlavourForm as a subclass of ModelForm, then we define an inner class called Meta, and give that class an attribute called model, which we initialise to Flavour:

.. code-block:: py

    class FlavourForm(ModelForm):
        class Meta:
            model = Flavour

One thing missing from the official Django tutorial is an explanation of how the form initially gets its values from the model instance, and how the model instance can be updated from the POST data.  The secret is the ``instance`` argument to the FlavourForm constructor.

Let's look at the three cases where FlavourForm is instantiated:

 - The first case is in the ``flavour_add()`` function:
 
   .. code-block:: py

       form = FlavourForm(request.POST)

   There is no ``initial`` argument, but the constructor is passed a dictionary of POST data.  In this case, a new form is created with the form fields populated from the POST data.  Not only that, but it also creates a new internal model instance.  Calling the form's ``save()`` function also calls the model instance's ``save()`` method.  This is useful when you want to create a new instance from form data, but the form data should be cleaned and validated first.
   
 - The second case is where the constructor is passed an ``instance`` argument but no POST data dictionary, such as in ``flavour_edit()``:
 
   .. code-block:: py

       form = FlavourForm(instance=flavour)

   In this case, the form's fields are initialised from the ``instance`` model instance.  The form and fields can then be passed to the template for display.
   
 - The third case is where the constructor is passed a dictionary of POST data, *and* an ``instance`` argument:
 
   .. code-block:: py

       form = FlavourForm(request.POST, instance=flavour)

   In this case, the form remembers the model instance, and updates that model instance's fields from the POST data.  This form can then be saved, which also saves the model instance.

Take careful note of the structure of the ``flavour_edit()`` function, as it's a very common pattern.  Basically, we're trying to handle four different scenarios:

GET or POST request, but with an invalid object (for example, no object with the given id):

    Throw a 404 exception; *or*
     
GET request:

    Retrieve model instance, create form using that instance, then pass the form to the template for rendering; *or*
     
POST request, with valid object, but invalid data:
 
    Retrieve the model instance, and create the form using that instance, but take the data from the POST dictionary.  Then pass the form to the template for rendering.  This allows the user to correct data they already typed; *or*
     
POST request, with valid object and data:
 
    Retrieve the model instance, and create the form using that instance.  Then update the fields of that instance using the POST dictionary.  Finally, save the form, which in turn saves the updated data in the model instance.

This pattern shows the most graceful way of handling these four cases.

Multiple actions
----------------

Having a view respond to both GET and POST requests isn't the only way of writing Django views, but it's a common way.  It conveniently groups the marshalling of information (GET request action) with the processing of that information (POST request action).  It may be though that a given web page presents several possible actions to the user.  If this GET/POST pattern is used, then it may be necessary for the POST part of the view to handle several separate actions.  This is usually done by having the form pass back some kind of ``action`` variable which the POST handler can look at and act on.  One way of rewriting ``flavour_edit()`` to handle multiple actions would be to replace the ``form.save()`` code with something that checked the value of ``request.POST['action']``, and executed code conditionally depending on that value.

Validation
----------

One benefit of using Django's forms over rolling our own is that Django can perform some validation automatically.  For example, since ``Flavour.litres`` is a ``FloatField``, entering a string into this form field would cause ``form.is_valid()`` to return FALSE, which prevents this invalid data from being saved to the database.  Not only that, ``is_valid()`` also marks fields that have invalid data, so that when the form is rendered, an error message is displayed next to fields with invalid data.

This kind of validation can only help catch type errors in model fields - it knows nothing about what values make sense to your application.  However you can add validation to your form code to do such validation.  For more information, see Django's forms documentation.

Field Help
----------

Our app now supports all four CRUD operations, and displays model data fields in forms.  But it would be better to give our users some advice about how the fields are used.  Let's change our code to provide some help text to the user:

.. code-block:: diff

    diff -u icecream-old/models.py icecream/models.py
    --- icecream-old/models.py
    +++ icecream/models.py
    @@ -3,8 +3,8 @@ from django.db import models
     # Create your models here.
     class Flavour(models.Model):
         name = models.CharField(max_length=40)
    -    litres = models.FloatField() # How many litres we have in the store
    -    sellprice = models.DecimalField(decimal_places=2, max_digits=5) # How much it costs per litre
    +    litres = models.FloatField(help_text="How many litres do we have in the store?") 
    +    sellprice = models.DecimalField(decimal_places=2, max_digits=5, help_text="How much per litre?") # 
     
         def __unicode__(self):
             return self.name

Now the page to add a page should also show some field help.

This text is also shown to users when they use the admin interface.  Try adding a flavour!

Plural nouns
------------

Let's say our shop is having a promotion: Half price for your favourite flavour!  To support this, we need to create a model for people and what kind of icecream they like:

.. code-block:: diff

    diff -u icecream-old/models.py icecream/models.py
    --- icecream-old/models.py
    +++ icecream/models.py
    @@ -9,3 +9,9 @@ class Flavour(models.Model):
         def __unicode__(self):
             return self.name
     
    +class Person(models.Model):
    +    name = models.CharField(max_length=60)
    +    favourite_flavour = models.ForeignKey(Flavour)
    +
    +    def __unicode__(self):
    +        return self.name
    diff -u icecream-old/admin.py icecream/admin.py
    --- icecream-old/admin.py
    +++ icecream/admin.py
    @@ -1,9 +1,14 @@
     from django.contrib import admin
    -from icecream.models import Flavour
    +from icecream.models import Flavour, Person
     
     # Override fields and ordering of fields
     class FlavourAdmin(admin.ModelAdmin):
         fields = ['name', 'litres', 'sellprice']
         list_display = ('name', 'litres', 'sellprice')
     
    +class PersonAdmin(admin.ModelAdmin):
    +    fields = ['name', 'favourite_flavour']
    +    list_display = ('name', 'favourite_flavour')
    +
     admin.site.register(Flavour, FlavourAdmin)
    +admin.site.register(Person, PersonAdmin)

Well that's fine, but then the admin interface starts talking about "Persons" instead of "People".  To correct this, we need to teach Django what the plural of Person is:

.. code-block:: diff

    diff -u icecream-old/models.py icecream/models.py
    --- icecream-old/models.py
    +++ icecream/models.py
    @@ -15,3 +15,6 @@ class Person(models.Model):
     
         def __unicode__(self):
             return self.name
    +
    +    class Meta:
    +        verbose_name_plural = "People"

Now try adding a person to the database.  What happens?  Ahh, DatabaseError, because we forgot to create the table.  Run this shell command to create the ``icecream_person`` table:

.. code-block:: bash

    python manage.py syncdb
    
People editing now works fine!

Displaying result messages
--------------------------

Three of the CRUD operations (create, update and delete) change data.  Sometimes our attempts might succeed, and sometimes they might fail.  Let's give our users a way of knowing whether something worked or not.


.. code-block:: diff

    diff -u icecream-old/views.py icecream/views.py
    --- icecream-old/views.py
    +++ icecream/views.py
    @@ -2,13 +2,14 @@ from django.shortcuts import render_to_response, get_object_or_404
     from django.template import RequestContext
     from django.http import HttpResponseRedirect
     from django.core.urlresolvers import reverse
    +from django.contrib import messages
     
     from icecream.models import Flavour
     from icecream.forms import FlavourForm
     
     def flavours(request):
         flavours = Flavour.objects.all()
    -    return render_to_response('icecream/flavours.html', {'flavours': flavours})
    +    return render_to_response('icecream/flavours.html', {'flavours': flavours}, context_instance=RequestContext(request))
     
     def flavour_add(request):
         if request.method == 'POST':
    @@ -16,7 +17,11 @@ def flavour_add(request):
             if form.is_valid():
                 form.save()
     
    +            messages.success(request, "Flavour added.")
    +
                 return HttpResponseRedirect(reverse('icecream.views.flavours'))
    +            
    +        messages.error(request, "The data is not valid, so the new flavour was not added.")
         else:
             form = FlavourForm()
     
    @@ -29,7 +34,11 @@ def flavour_edit(request, id):
             if form.is_valid():
                 form.save()
     
    +            messages.success(request, "Flavour changed.")
    +
                 return HttpResponseRedirect(reverse('icecream.views.flavours'))
    +
    +        messages.error(request, "The data is not valid, so the flavour was not updated.")
         else:
             form = FlavourForm(instance=flavour) # bound form, loaded with data from the db
     
    @@ -43,6 +52,8 @@ def flavour_delete(request, id):
         if request.method == 'POST':
             flavour.delete()
     
    +        messages.success(request, "Flavour deleted.")
    +
             return HttpResponseRedirect(reverse('icecream.views.flavours'))
     
         return render_to_response('icecream/flavour-delete.html', {'flavour': flavour}, context_instance=RequestContext(request))
    diff -u templates-old/base.html templates/base.html
    --- templates-old/base.html
    +++ templates/base.html
    @@ -4,6 +4,14 @@
         <title>{% block title %}icecream.com: Nirvana for icecream lovers{% endblock %}</title>
       </head>
       <body>
    +    {% if messages %}
    +      <h2>Messages</h2>
    +      <ul class="messages">
    +        {% for message in messages %}
    +          <li><i>{{ message }}</i></li>
    +        {% endfor %}
    +      </ul>
    +    {% endif %}
         <h1>{% block header %}Nirvana for icecream lovers{% endblock %}</h1>
         {% block content %}{% endblock %}
         {% block footer %}

One advantage of template inheritance is that this gives us one place where we can take care of displaying messages.

Summary
=======

Django gives us:

 - A cross-platform, cross-database way of writing web-based CRUD apps, and
 - A free admin interface for staff

In general, the plan for writing a Django app goes:

 - Define models
 - Make a URL plan
 - Map URLs to views
 - Write views, map to templates
 - Write templates

This also applies to adding functionality to existing apps.

And Django has hundreds of other plugins, such as:

 - Database schema migrations
 - Security and authentication

Thanks for following this tutorial!

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

