#!/usr/bin/env python
"""
Dumps all models in a directory
By looking for classes that inherit from MTLModel,
    or from something that does.
"""
import sys
import os
import glob
import re

model_pattern = re.compile(r'^[\s]*@interface[\s]+([\w]+)[\s]*:[\s]*([\w]+)')
field_pattern = re.compile(r'@property[\s]*\(.*\)[\s]*([\w]+)[\s]*\**([\w]+);')


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

# https://raw.github.com/fabric/fabric/master/fabric/colors.py
def _wrap_with(code):
    def inner(text, bold=False):
        c = code
        if bold:
            c = "1;%s" % c
        return "\033[%sm%s\033[0m" % (c, text)
    return inner

red = _wrap_with('31')
green = _wrap_with('32')
yellow = _wrap_with('33')
blue = _wrap_with('34')
magenta = _wrap_with('35')
cyan = _wrap_with('36')
white = _wrap_with('37')


def decamel(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


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

path = '.'
if len(sys.argv) > 1:
    path = sys.argv[1]


def scan_files(path, model_classes=None):
    os.chdir(path)

    # A dict:   models['model name'] = 'model file'
    model_classes = model_classes or []
    model_classes.append('MTLModel')
    models = []

    for header in glob.glob('*.h'):
        for line in open(header):
            model_match = model_pattern.search(line)
            if model_match:
                # This class inherits from a model if the second match group
                # is `MTLModel` or a model subclass
                superclass_name = model_match.groups()[1]
                if superclass_name in model_classes:
                    class_name = model_match.groups()[0]
                    models.append(Model(name=class_name, filename=header, superclass=superclass_name))
                    model_classes.append(class_name)
                    break
    return models


# Scan for models
# We run it twice because we might have caught a base class the first time
models = scan_files(path)
models = scan_files(path, [model.name for model in models])


# For each model, load all the fields

for model in models:
    for line in open(model.filename):
        field_match = field_pattern.search(line)
        if field_match:
            field_type, field_name = field_match.groups()
            model.fields.append(ModelField(field_type, field_name))

models_by_name = {model.name: model for model in models}

print '\nFound models\n'
for model in models:
    print model.get_str(models_by_name=models_by_name)
    print '\n'

