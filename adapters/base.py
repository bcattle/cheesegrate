import os.path
import sys
from utils import green, decamel

class BaseAdapter(object):
    file_extension = None

    def __init__(self, overwrite=False):
        self.overwrite = overwrite

    def get_plural_filename_for_klass(self, model_klass):
        if self.file_extension:
            if hasattr(model_klass.Meta, 'name_plural'):
                return '%s.%s' % (model_klass.Meta.name_plural.lower(),
                                  self.file_extension)
            else:
                return '%ss.%s' % (model_klass.__name__.lower(),
                                   self.file_extension)
        else:
            raise NotImplementedError

    def get_filename_for_klass(self, model_klass):
        if self.file_extension:
            return '%s.%s' % (decamel(model_klass.__name__),
                              self.file_extension)
        else:
            raise NotImplementedError

    def transform_klass(self, model_klass):
        raise NotImplementedError

    def pre_transform(self, iterations):
        """
        Generate any header information
        required for the output file
        """
        pass

    def post_transform(self, iterations):
        """
        Do any work required to finish the
        output file
        """
        pass

    def post_process(self):
        """
        Runs after the file is closed,
        i.e. an external command
        """
        pass

    def transform_model(self, model_klass, filename=None, **kwargs):
        if filename:
            self.filename = filename
        else:
            self.filename = self.get_filename_for_klass(model_klass)
        # If the filename exists, prompt to overwrite
        if not self.overwrite:
            if os.path.isfile(self.filename):
                char = raw_input('File "%s" exists. Overwrite? [Y]/n: ' % self.filename)
                if char != 'Y' and char != '':
                    sys.exit(0)
        self.file = open(self.filename, 'w')

        # Generate the output
        self.pre_transform(1)
        # Run the transformation, returns string output
        transformed = self.transform_klass(model_klass)
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

    def transform_obj(self, obj):
        raise NotImplementedError

    # def get_factory_for_field
    def transform_model_array(self, model_klass, n, filename=None, factories=None):
        self.factories = factories

        if filename:
            self.filename = filename
        else:
            self.filename = self.get_plural_filename_for_klass(model_klass)
        self.file = open(self.filename)

        # Generate the output
        self.pre_transform(n)
        for i in range(n):
            # Set a counter variable we can use if we need to
            self.model_index = i
            # Generate python values for the class
            obj = self.python_obj_for_klass(model_klass)
            # Run the transformation, returns string output
            transformed = self.transform_obj(obj)
            if i < n - 1:
                transformed += ',\n'
            self.file.write(transformed)
        self.post_transform(n)
        self.file.write('\n')
        self.file.close()
        self.post_process()
        print '%s generated %s' % (green('--'), self.filename)

    def transform_model(self, model_klass, filename=None, factories=None):
        self.factories = factories

        if filename:
            self.filename = filename
        else:
            self.filename = self.get_filename_for_klass(model_klass)
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
        obj = self.python_obj_for_klass(model_klass)
        # Run the transformation, returns string output
        transformed = self.transform_obj(obj)
        self.file.write(transformed)
        self.post_transform(1)
        self.file.write('\n')
        self.file.close()
        self.post_process()
        print '%s generated %s' % (green('--'), self.filename)

    def python_obj_for_klass(self, model_klass):
        """
        Returns a python dict containing the fields
        and values populated from the relevant factories
        for the specified type

        This takes model_klass as a parameter so we can query superclasses
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
                    obj[field_name] = factory._fields[field_name](self, model_klass)

            # If not, is there a default factory?
            elif default_factory:
                # Does this field *name* have a default?
                if field_name in default_factory._fields:
                    obj[field_name] = default_factory._fields[field_name](self, model_klass)

                # Does this field *type* have a default?
                elif hasattr(default_factory, 'type_defaults') and \
                        field_type_name in default_factory.type_defaults:
                    obj[field_name] = default_factory.type_defaults[field_type_name](self, model_klass)

            else:
                # If not, query the field to get the blank value
                obj[field_name] = field.blank_value()

        # Does this model inherit from a class that we also need to process?
        superclass = model_klass.__bases__[0]
        if superclass.__name__ != 'Model':
            obj.update(self.python_obj_for_klass(superclass))

        return obj


class ChainAdapter(BaseAdapter):
    """
    Runs a series of adapters serially
    """
    pass
