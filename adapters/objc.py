from . import BaseAdapter

class Adapter(BaseAdapter):
    def get_filename_for_klass(self, model_klass):
        # TODO: needs to make .h and .m files
        return '%s.h' % model_klass.__name__.lower()

    # The transformation
    def _do_transform(self, model_klass):
        pass

        # Returns the transformed object
        return {}

    # Hooks

    def pre_transform(self, iterations):
        """
        Generate any header information
        required for the output file
        """
        pass

        return ''

    def post_transform(self, iterations):
        """
        Do any work required to finish the
        output file
        """
        pass

        return ''

    def post_process(self):
        # Indent
        pass