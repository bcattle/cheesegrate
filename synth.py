#!/usr/bin/env python
import argparse
# import pkgutil
import importlib
import os
import sys
from utils import get_class_or_module_for_classpath, get_subpackages

# Load the list of adapters
import contrib.adapters
adapters = get_subpackages(contrib.adapters)

# Add arguments for those adapters
parser = argparse.ArgumentParser(description='Generates different representations of our data models')
parser.add_argument('adapter',  choices=adapters, help='Run a specified adapter')
parser.add_argument('path', help='The classpath to the model(s) of interest, e.g. phone_models.User')
parser.add_argument('factory_path', nargs='?', default='',      # <- makes it optional
                    help='The classpath to a factory or factories for the models (if applicable)')
parser.add_argument('-o', '--output_path', nargs=1, help='Directory or filename send output to')
parser.add_argument('-f', '--force', action='store_true', help='Force overwrite')
parser.add_argument('--help-adapters', action='store_true', help='Display documentation of each available adapter')

parsed_args = parser.parse_args()

# Show the adap[ter documentation if they asked for it
if parsed_args.help_adapters:
    pass
    sys.exit(0)

# Import the adapter they asked for
adapter_module = importlib.import_module('contrib.adapters.%s.adapter' % parsed_args.adapter)
Adapter = adapter_module.Adapter


# Did they ask for a factory or factories?
factories = None
if parsed_args.factory_path:
    factory_module, factory_klass = get_class_or_module_for_classpath(parsed_args.factory_path)
    if factory_klass is None:
        # They specified a module
        # Load the factories which were registered by the metaclass
        from factory.base import _factories
        factories = _factories
    else:
        # They specified a single class
        factories = {factory_klass.__name__: factory_klass}


# Switch to the output directory
# TODO: could also be an output *file*
if parsed_args.output_path:
    os.chdir(os.path.abspath(parsed_args.output_path))


# Import the models' classpath
model_module, model_klass = get_class_or_module_for_classpath(parsed_args.path)
if model_klass is None:
    # The user specified a module
    # Since it was imported, the full list
    # of modules is now stored in `base`!
    from models.base import _models

    # Run the adapter on each class
    for name, model_klass in _models.items():
        adapter = Adapter(overwrite=parsed_args.force)
        # Call adapter.transform_model or adapter.transform_model_array
        adapter.transform_model(model_klass, filename=None, factories=factories)

else:
    # The user specified a specific class
    # Run the adapter
    adapter = Adapter(overwrite=parsed_args.force)
    adapter.transform_model(model_klass, filename=None, factories=factories)

