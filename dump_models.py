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
import datetime
import uuid
import random
import argparse
from parsed_models import Model, ModelField


model_pattern = re.compile(r'^[\s]*@interface[\s]+([\w]+)[\s]*:[\s]*([\w]+)')
field_pattern = re.compile(r'@property[\s]*\(.*\)[\s]*([\w]+)[\s]*\**([\w]+);')

json_types = {
    # Maps the objc string to a python (soon to be JSON) object
    'NSArray': [],
    'NSString': '',
    'NSDate': '',
    'NSNumber': 1,
    'float': 65.1,
    'BOOL': True,
    'UInt32': 10,
    'NSURL': 'http://example.com/',
}

special_fields = {
    # Maps field names to functions that create them
    'createdAt': lambda: datetime.datetime.utcnow().isoformat("T") + "Z",
    'updatedAt': lambda: datetime.datetime.utcnow().isoformat("T") + "Z",
    'id': lambda: str(uuid.uuid4()),
    'isFollowed': lambda: False,
    'upVotes': random.randint(0, 1000),
    'downVotes': random.randint(0, 250),
}


# Example command lines --
# models.py list .
# models.py generate . ISUser -n 10 -o users.json

parser = argparse.ArgumentParser(description='Generates and displays data models')
parser.add_argument('action', help='"list" or "generate"')
parser.add_argument('path', help='The path to search')
parser.add_argument('-n', help='The number of models to generate', default=1)
parser.add_argument('-o', help='The name of the output file to generate', default='')


path = '.'
if len(sys.argv) > 1:
    path = os.path.abspath(sys.argv[1])


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

