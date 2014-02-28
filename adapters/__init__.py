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

    def _do_transform(self, model_klass):
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
            # Run the transformation, returns string output
            transformed = self._do_transform(self.model_klass)
            if i < n - 1:
                transformed += ',\n'
            self.file.write(transformed)
        self.post_transform(n)
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
        # Run the transformation
        transformed = self._do_transform(self.model_klass)
        self.file.write(transformed)
        self.post_transform(1)
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

