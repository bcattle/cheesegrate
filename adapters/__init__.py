
class BaseAdapter(object):
    def __init__(self, model_klass, factories=None):
        self.model_klass = model_klass
        self.factories = factories

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
            # Set a cpunter variable we can use if we need to
            self.model_index = i
            # Run the transformation, returns string output
            transformed = self._do_transform(self.model_klass)
            if i < n - 1:
                transformed += ',\n'
            self.file.write(transformed)
        self.post_transform(n)
        self.file.close()
        self.post_process()

    def transform_model(self, filename=None):
        if filename:
            self.filename = filename
        else:
            self.filename = self.get_filename_for_klass(self.model_klass)
        self.file = open(self.filename)

        # Generate the output
        self.pre_transform(1)
        # Run the transformation
        transformed = self._do_transform(self.model_klass)
        self.file.write(transformed)
        self.post_transform(1)
        self.file.close()
        self.post_process()
