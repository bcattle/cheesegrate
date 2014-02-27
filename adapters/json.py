"""
JSON adapter
Takes a `Model` class and it's attendant `Field` classes
and creates a JSON representation of it
"""
from . import BaseAdapter
import simplejson as json

class Adapter(BaseAdapter):

    def get_plural_filename_for_klass(self, model_klass):
        if hasattr(model_klass.Meta, 'name_plural'):
            return '%s.json' % model_klass.Meta.name_plural.lower()
        else:
            return '%ss.json' % model_klass.__name__.lower()

    def get_filename_for_klass(self, model_klass):
        # JSON is "lowercase name .json"
        return '%s.json' % model_klass.__name__.lower()

    # The transformation
    def _do_transform(self, model_klass):
        pass

        import ipdb
        ipdb.set_trace()

        # Returns the transformed object
        return {}

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

    def post_process(self):
        # Indent
        pass