"""
JSON adapter
  Takes a `Model` class and it's attendant `Field` classes
  and creates a JSON representation of it,
  using factories if provided
"""
import simplejson as json
from . import BaseFactoryAdapter
from utils import decamel

class Adapter(BaseFactoryAdapter):

    def get_plural_filename_for_klass(self, model_klass):
        if hasattr(model_klass.Meta, 'name_plural'):
            return '%s.json' % model_klass.Meta.name_plural.lower()
        else:
            return '%ss.json' % model_klass.__name__.lower()

    def get_filename_for_klass(self, model_klass):
        # JSON is "lowercase name .json"
        return '%s.json' % decamel(model_klass.__name__)

    # The transformation
    def do_transform(self, obj):
        """
        Transform a python object of values
        to JSON
        """
        json_obj = json.dumps(obj, indent=4)
        # Return the transformed object
        return json_obj

    # Hooks

    def pre_transform(self, iterations):
        """
        Generate any header information
        required for the output file
        """
        if iterations > 1:
            return '['

    def post_transform(self, iterations):
        """
        Do any work required to finish the
        output file
        """
        if iterations > 1:
            return ']'
