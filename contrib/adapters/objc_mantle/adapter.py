"""
Objective-C Mantle adapter
  Generates Obj-C data model classes
  that use the Mantle framework
  <https://github.com/MantleFramework/Mantle/>
"""
import datetime
from utils import to_camel
from adapters.base import BaseAdapter, ChainAdapter
from settings import *
from contrib.adapters.objc_mantle.fields import FIELD_PROPERTIES, \
    FIELD_VALUE_TRANSFORMERS
from jinja2 import Environment, PackageLoader


# class Adapter(ChainAdapter):
#     adapters = [HeaderAdapter, ImplementationAdapter]


# class ImplementationAdapter(BaseAdapter):
class Adapter(BaseAdapter):
    """
    Generates the .m file
    """
    def get_filename_for_klass(self, model_klass):
        return '%s%s.m' % (OBJC_CLASS_PREFIX, model_klass.__name__)

    # The transformation
    def transform_klass(self, model_klass):
        """
        Transforms the model type into an
        output string to save the file
        """
        # Jinja2 setup
        env = Environment(loader=PackageLoader('contrib.adapters.objc_mantle'),
                          lstrip_blocks=True, trim_blocks=True)

        # Template vars
        superclass = model_klass.__bases__[0]
        superclass_name = superclass.__name__
        # Is klass a Model, or did it inherit from something else?
        superclass_is_model = superclass_name is 'Model'

        fields = []
        value_transformers = []
        for field_name, field in model_klass._fields.items():
            fields.append((to_camel(field_name), field_name))
            if field.__class__ in FIELD_VALUE_TRANSFORMERS:
                value_transformers.append({
                    'objc_field': to_camel(field_name),
                    'body': FIELD_VALUE_TRANSFORMERS[field.__class__],
                })

        # Run the template
        header_template = env.get_template('implementation.txt')
        out = header_template.render(filename=self.get_filename_for_klass(model_klass),
                                     app=APP, author=AUTHOR,
                                     today=datetime.date.today().strftime('%x'),
                                     this_year=datetime.date.today().year,
                                     company=COMPANY,
                                     superclass_is_model=superclass_is_model,
                                     superclass=superclass_name,
                                     class_name=model_klass.__name__,
                                     fields=fields,
                                     value_transformers=value_transformers)

        # Returns string to write to file
        return out

    # Hooks

    def post_process(self):
        # Indent
        pass



class HeaderAdapter(BaseAdapter):
    def get_filename_for_klass(self, model_klass):
        return '%s%s.h' % (OBJC_CLASS_PREFIX, model_klass.__name__)

    # The transformation
    def transform_klass(self, model_klass):
        """
        Transforms the model type into an
        output string to save the file
        """
        # Jinja2 setup
        env = Environment(loader=PackageLoader('contrib.adapters.objc_mantle'),
                          lstrip_blocks=True, trim_blocks=True)

        # Template vars
        superclass = model_klass.__bases__[0]
        superclass_name = superclass.__name__
        # Is klass a Model, or did it inherit from something else?
        superclass_is_model = superclass_name is 'Model'

        fields = []
        for field_name, field in model_klass._fields.items():
            fields.append('%s%s;' % (FIELD_PROPERTIES[field.__class__], to_camel(field_name)))

        # Run the template
        header_template = env.get_template('header.txt')
        out = header_template.render(filename=self.get_filename_for_klass(model_klass),
                                     app=APP, author=AUTHOR,
                                     today=datetime.date.today().strftime('%x'),
                                     this_year=datetime.date.today().year,
                                     company=COMPANY,
                                     superclass_is_model=superclass_is_model,
                                     superclass=superclass_name,
                                     class_name=model_klass.__name__,
                                     fields=fields)

        # Returns string to write to file
        return out

    # Hooks

    def post_process(self):
        # Indent
        pass

