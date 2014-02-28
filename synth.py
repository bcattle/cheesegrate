#!/usr/bin/env python
import argparse
import pkgutil
import importlib
import os

# Load the list of adapters
adapters = [pkg[1] for pkg in pkgutil.iter_modules(path=['adapters'])]

# Add arguments for those adapters
parser = argparse.ArgumentParser(description='Generates different representations of our data models')
parser.add_argument('adapter',  choices=adapters, help='Run a specified adapter')
parser.add_argument('path', help='The classpath to the model(s) of interest, e.g. phone_models.User')
parser.add_argument('factory_path', nargs='?', default='',      # <- makes it optional
                    help='The classpath to a factory or factories for the models (if applicable)')
parser.add_argument('-o', '--output_path', nargs=1, help='Directory or filename send output to')
parser.add_argument('-f', '--force', action='store_true', help='Force overwrite')

parsed_args = parser.parse_args()

# Import the adapter they asked for
adapter_module = importlib.import_module('adapters.%s' % parsed_args.adapter)
Adapter = adapter_module.Adapter

def get_class_or_module_for_classpath(classpath):
    """
    For a `classpath` like modules.stuff, import as a module
    for a `classpath` like modules.MyClass, import the class

    Returns: module, class

    """
    module_and_maybe_class = classpath.rsplit('.', 1)
    if module_and_maybe_class[-1].isupper():
        # It is a class.
        # Import the module and pull the class from it
        module, class_name = module_and_maybe_class
        model_module = importlib.import_module(module)
        model_klass = getattr(model_module, class_name)

        # Return
        return model_module, model_klass

    else:
        # It's a module path only, import it
        model_module = importlib.import_module(classpath)
        return model_module, None


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
        adapter = Adapter(model_klass, overwrite=parsed_args.force)
        # Call adapter.transform_model or adapter.transform_model_array
        adapter.transform_model(filename=None, factories=factories)

else:
    # The user specified a specific class
    # Run the adapter
    adapter = Adapter(model_klass, overwrite=parsed_args.force)
    adapter.transform_model(filename=None, factories=factories)

