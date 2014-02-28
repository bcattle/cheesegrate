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
    def _do_transform(self, model_klass):
        """
        We have a model class and maybe a factory in
        in `self.factory`

        Find a matching factory (if any) and run it
        if there is no factory,
        generate a blank representation of the field
        """
        # Find factory and default factory
        factory = self.get_factory_for_model(model_klass)
        default_factory = self.get_default_factory()

        obj = {}
        for field_name, field in model_klass._fields.items():

            field_type_name = field.__class__.__name__

            if factory:
                # Does the model factory define this field?
                if field_name in factory._fields:
                    # Get the value
                    obj[field_name] = factory._fields[field_name]()

            # If not, is there a default factory?
            elif default_factory:
                # Does this field *name* have a default?
                if field_name in default_factory._fields:
                    obj[field_name] = default_factory._fields[field_name]()

            # Does this field *type* have a default?
            elif hasattr(default_factory, 'type_defaults') and \
                    field_type_name in default_factory.type_defaults:
                obj[field_name] = default_factory.type_defaults[field_type_name]()

            else:
                # If not, query the field to get the blank value
                obj[field_name] = field.blank_value()

        # We now have a dict of values, convert to JSON and return
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
