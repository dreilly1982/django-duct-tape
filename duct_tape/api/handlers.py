'''
Yanked from django, so that I could have a properly formatted message to use in a piston handler
'''

from piston.utils import rc

from django.db.models.manager import Manager
from django.db.models.query import QuerySet

def _get_queryset(klass):
    """
    Returns a QuerySet from a Model, Manager, or QuerySet. Created to make
    get_object_or_404 and get_list_or_404 more DRY.
    """
    if isinstance(klass, QuerySet):
        return klass
    elif isinstance(klass, Manager):
        manager = klass
    else:
        manager = klass._default_manager
    return manager.all()

def get_object_or_404(klass, *args, **kwargs):
    """
    Uses get() to return an object, or raises a Http404 exception if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        resp = rc.NOT_FOUND
        resp.write('No %s matches the given query.' % queryset.model._meta.object_name)
        return resp

def get_list_or_404(klass, *args, **kwargs):
    """
    Uses filter() to return a list of objects, or raise a Http404 exception if
    the list is empty.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the filter() query.
    """
    queryset = _get_queryset(klass)
    obj_list = list(queryset.filter(*args, **kwargs))
    if not obj_list:
        resp = rc.NOT_FOUND
        resp.write('No %s matches the given query.' % queryset.model._meta.object_name)
        return resp

    return obj_list      

# helper baseclass

from piston.handler import BaseHandler as PistonBaseHandler

class BaseHandler(PistonBaseHandler):
    def read(self,request,pk=None):
        print "BASE GET"
        print "BASE pk:%s:" % pk
        # on GET
        if pk:
            return get_object_or_404(self.model,pk=pk)
        else:
            return self.model.objects.all()

    def create(self,request):
        # on POST
        pass

    def update(self,request,pk):
        # on PUT
        pass

    def delete(self,request,pk):
        # on DELETE
        pass