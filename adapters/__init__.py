import os.path
import sys
from utils import green

class BaseAdapter(object):
    def __init__(self, model_klass, overwrite=False):
        self.model_klass = model_klass
        self.overwrite = overwrite

    def get_plural_filename_for_klass(self, model_klass):
        raise NotImplementedError

    def get_filename_for_klass(self, model_klass):
        raise NotImplementedError

    def python_values_for_class(self, model_klass):
        raise NotImplementedError

    def do_transform(self, model_klass):
        raise NotImplementedError

    def pre_transform(self, iterations):
        pass

    def post_transform(self, iterations):
        pass

    def post_process(self):
        """
        Runs after the file is closed,
        i.e. an external command
        """
        pass

    def transform_model_array(self, n, filename=None):
        if filename:
            self.filename = filename
        else:
            self.filename = self.get_plural_filename_for_klass(self.model_klass)
        self.file = open(self.filename)

        # Generate the output
        self.pre_transform(n)
        for i in range(n):
            # Set a counter variable we can use if we need to
            self.model_index = i
            # Generate python values for the class
            obj = self.python_values_for_class(self.model_klass)
            # Run the transformation, returns string output
            transformed = self.do_transform(obj)
            if i < n - 1:
                transformed += ',\n'
            self.file.write(transformed)
        self.post_transform(n)
        self.file.write('\n')
        self.file.close()
        self.post_process()
        print '%s generated %s' % (green('--'), self.filename)

    def transform_model(self, filename=None):
        if filename:
            self.filename = filename
        else:
            self.filename = self.get_filename_for_klass(self.model_klass)
        # If the filename exists, prompt to overwrite
        if not self.overwrite:
            if os.path.isfile(self.filename):
                char = raw_input('File "%s" exists. Overwrite? [Y]/n: ' % self.filename)
                if char != 'Y' and char != '':
                    sys.exit(0)
        self.file = open(self.filename, 'w')

        # Generate the output
        self.pre_transform(1)
        # Generate python values for the class
        obj = self.python_values_for_class(self.model_klass)
        # Run the transformation, returns string output
        transformed = self.do_transform(obj)
        self.file.write(transformed)
        self.post_transform(1)
        self.file.write('\n')
        self.file.close()
        self.post_process()
        print '%s generated %s' % (green('--'), self.filename)


class BaseFactoryAdapter(BaseAdapter):
    """
    Some adapters, like `JSON` support the use of factories
    For others, like `objc` the notion of a factory doesn't make sense
    """
    def get_factory_for_model(self, model_klass):
        """
        Simple, if the class is called `MyClass`, looks for `MyClassFactory`
        """
        return self.factories.get('%sFactory' % model_klass.__name__, None)

    def get_default_factory(self):
        return self.factories.get('DefaultFactory', None)

    def transform_model_array(self, n, filename=None, factories=None):
        self.factories = factories
        return super(BaseFactoryAdapter, self).transform_model_array(n, filename)

    def transform_model(self, filename=None, factories=None):
        self.factories = factories
        return super(BaseFactoryAdapter, self).transform_model(filename)

    def python_values_for_class(self, model_klass):
        """
        Returns a python dict containing the fields
        and values populated from the relevant factories
        for the specified type
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

        import ipdb
        ipdb.set_trace()

        # Does this model inherit from a class that we also need to process?
        superclass = model_klass.__bases__[0]
        if superclass.__name__ != 'Model':
            obj.update(self.python_values_for_class(superclass))

        return obj
