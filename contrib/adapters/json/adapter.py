"""
JSON adapter
  Takes a `Model` class and it's attendant `Field` classes
  and creates a JSON representation of it,
  using factories if provided
"""
import simplejson as json
from adapters.base import BaseFactoryAdapter

class Adapter(BaseFactoryAdapter):
    file_extension = 'json'

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
        Any work required to finish the
        output file
        """
        if iterations > 1:
            return ']'
