from utils import decamel, red, green, yellow, blue, magenta, cyan, white

# class ModelList(list):
#     def model_names(self):
#         return [model.name for model in self]
#
#     def __repr__(self):
#         """
#         Print the models in a aligned table,
#         sorted by subclass, then name
#         """
#         model_names = self.model_names()
#         model_superclasses = [model.superclass for model in self]
#         model_files =


class Model(object):
    def __init__(self, name, filename, superclass):
        self.name = name
        self.filename = filename
        self.superclass = superclass
        self.fields = []

    def get_str(self, models_by_name=None, print_name=True):
        s = ''
        if print_name:
            s = '%s : %s \t<%s>' % (red(self.name.ljust(20)), green(self.superclass.ljust(15)),
                                    blue(self.filename))
        for field in self.fields:
            s += '\n%s' % field.__repr__()

        if self.superclass != 'MTLModel' and models_by_name:
            # Also print the fields of the superclass
            s += '\n%s' % models_by_name[self.superclass].get_str(models_by_name=models_by_name,
                                                                  print_name=False)
        return s


class ModelField(object):
    def __init__(self, ftype, name):
        self.ftype = ftype
        self.name = name

    def __repr__(self):
        return '\t%s : %s %s' % (blue(self.name.ljust(15)), cyan(self.ftype.ljust(30)),
                                 decamel(self.name))
